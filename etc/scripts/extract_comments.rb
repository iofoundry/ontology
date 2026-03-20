
require 'octokit'
require 'json'

if ARGV.length < 1
  puts "Usage: ruby extract_comments.rb <pull_request_number>"
  exit 1
end

if ENV['GITHUB_TOKEN'].nil? || ENV['GITHUB_TOKEN'].empty?
  puts "Error: GITHUB_TOKEN environment variable is not set"
  exit 1
end

pr_number = ARGV[0].to_i

octokit = Octokit::Client.new(access_token: ENV['GITHUB_TOKEN'])
octokit.auto_paginate = true

commits = Hash.new { |hash, key| hash[key] = [] }
octokit.pull_request_commits('iofoundry/ontology', pr_number).each do |commit|
  commit['commit']['message'].scan(/#discussion_r([0-9]+)/).each do |match|
    discussion = match[0].to_i
    commits[discussion] << commit
  end
end

query = <<~GRAPHQL
  query($owner: String!, $repo: String!, $pr: Int!, $cursor: String) {
    repository(owner: $owner, name: $repo) {
      pullRequest(number: $pr) {
        reviewThreads(first: 100, after: $cursor) {
          pageInfo {
            hasNextPage
            endCursor
          }
          nodes {
            id
            isResolved
            isOutdated
            resolvedBy {
              login
            }
            comments(first: 1) {
              nodes {
                body
                databaseId
              }
            }
          }
        }
      }
    }
  }
GRAPHQL
cursor = nil
resolutions = Hash.new
loop do
  response = octokit.post('/graphql', {
    query: query,
    variables: { owner: 'iofoundry', repo: 'ontology', pr: pr_number, cursor: cursor }
  }.to_json)
  threads = response['data']['repository']['pullRequest']['reviewThreads']
  threads['nodes'].each do |thread|
    if thread['isResolved']
      #puts "Resolved by #{thread['resolvedBy']['login']} in for comment #{thread['comments']['nodes'][0]['databaseId']}"
      resolutions[thread['comments']['nodes'][0]['databaseId']] = thread['resolvedBy']['login']
    end
  end
  break unless threads['pageInfo']['hasNextPage']
  cursor = threads['pageInfo']['endCursor']
end

File.open('comments.md', 'w') do |file|
  comments = octokit.pull_request_comments('iofoundry/ontology', pr_number, per_page: 100)
  comments_by_id = Hash[*comments.map do |comment|
    comment['replies'] = []
    comment['commits'] = commits[comment['id']]
    comment['resolved'] = resolutions[comment['id']]
    [comment['id'], comment]
  end.flatten]
  comments.each do |comment|
    if comment['in_reply_to_id']
      parent = comments_by_id[comment['in_reply_to_id']]
      parent['replies'] << comment if parent
      comments_by_id.delete(comment['id'])
    end
  end
  comments_by_resolved = comments_by_id.values.group_by { |comment| comment['resolved'] ? 'Resolved' : 'Unresolved' }
  comments_by_resolved.each do |status, comments_by_status|
    file.puts "# #{status} Comments\n\n"
    comments_by_path = comments_by_status.group_by { |comment| comment['path'] }.sort_by { |path, _| path }
    comments_by_path.each do |path, comments|
      file.puts "## Comments on #{path}\n\n"
      comments.each do |comment|
        file.puts "### Comment by #{comment['user']['login']} on #{comment['created_at']}"
        if comment['resolved']
          file.puts "> **Resolved by #{comment['resolved']}**"
        end
        file.puts <<EOT

#{comment['body']}

[View on GitHub](#{comment['html_url']})
EOT

        if comment['replies'] and !comment['replies'].empty?
          file.puts "#### Replies"
          comment['replies'].each do |reply|
            file.puts <<EOT
##### Reply by #{reply['user']['login']} on #{reply['created_at']}

#{reply['body']}
EOT
          end
        end

        if comment['commits'] and !comment['commits'].empty?
          file.puts "#### Commits"
          comment['commits'].each do |commit|
            file.puts <<EOT
##### Commit [#{commit['sha'][0..7]}](#{commit['commit']['url']}) by #{commit['commit']['author']['name']} on #{commit['commit']['author']['date']}

#{commit['commit']['message']}
EOT
          end
        end

        if comment['diff_hunk'] and !comment['diff_hunk'].empty?
          hunk = comment['diff_hunk'].split("\n").last(20).join("\n")
          file.puts <<EOT
#### Context

```diff
#{hunk}
```
EOT
        end

        file.puts "\n---\n\n"
      end
      file.puts "\n---\n\n"
    end
  end
end
