require 'rexml/document'

if ARGV.length != 1
  puts "Usage: change_prefix.rb <version>"
  exit
end

version = ARGV[0]

puts "Changing prefix 'iof-const' to 'iof-constr'..."

Dir['**/*.rdf'].each do |file|
  next if file.include?('cache')
  text = File.read(file)
  if !text.include?('iof-constr')    
    new_text = text.gsub('iof-const', 'iof-constr')
    if text != new_text
      File.open(file, 'w') { |f| f.write(new_text) }
      puts "Updated prefixes in #{file}"
    end
  else
    puts "File #{file} already uses 'iof-constr' prefix, skipping."
  end
end

puts "\nUpdate versionIRIs to version #{version}..."

# Fix the versionIRI to have the correct version number
Dir['**/*.rdf'].each do |file|
  context = { raw: :all }
  doc = REXML::Document.new(File.read(file), context)
  root = doc.root

  # find the IRI for the ontology
  ontologies = root.get_elements("//owl:Ontology")
  if ontologies.length != 1
    puts "Error: Expected exactly one owl:Ontology element, found #{ontologies.length}"
    next
  end

  ontology = ontologies.first
  ontology_iri = ontology.attributes["rdf:about"]
  next if !ontology_iri.start_with?('https://spec.industrialontologies.org/ontology/')

  puts "Ontology IRI: #{ontology_iri}"
  new_iri = ontology_iri.sub(%r{^(https://spec.industrialontologies.org/ontology/)(.+)}, "\\1#{version}/\\2")

  version_iri = ontology.get_elements("owl:versionIRI").first
  if version_iri and iri = version_iri.attributes["rdf:resource"]
    puts "  Current versionIRI: #{iri}"
    puts "  New versionIRI: #{new_iri}"
    version_iri.attributes["rdf:resource"] = new_iri
  else
    puts "  No versionIRI found adding."
    puts "  New versionIRI: #{new_iri}"
    version_iri = REXML::Element.new("owl:versionIRI")
    version_iri.attributes["rdf:resource"] = new_iri
    ontology.add_element(version_iri)
  end

# Add copyright annotation if not present
  copyright = ontology.get_elements("iof-av:copyright").first
  if not copyright
    puts "  Adding copyright annotation."
    copyright = REXML::Element.new("iof-av:copyright")
    ontology.add_element(copyright)
  end
  copyright.text = "Copyright (c) 2022, 2023, 2024, 2025 Open Applications Group"

  File.open(file, 'w') do |file|
    doc.write(output: file, indent: -1, transitive: false)
  end
end