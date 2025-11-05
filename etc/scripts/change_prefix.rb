Dir['**/*.rdf'].each do |file|
  text = File.read(file)
  new_text = text.gsub('iof-const', 'iof-constr')
  if text != new_text
    File.open(file, 'w') { |f| f.write(new_text) }
    puts "Updated prefixes in #{file}"
  end
end
