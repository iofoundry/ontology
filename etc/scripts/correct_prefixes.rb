
prefixes = [ 
  ["http://purl.obolibrary.org/obo/", 'bfo'],
  ["http://purl.org/dc/elements/1.1/", 'dc'],
  ["http://purl.org/dc/terms/", 'dcterms'],
  ["http://www.w3.org/2002/07/owl#", 'owl'],
  ["http://www.w3.org/1999/02/22-rdf-syntax-ns#", 'rdf'],
  ["http://www.w3.org/2000/01/rdf-schema#", 'rdfs'],
  ["http://www.w3.org/2004/02/skos/core#", 'skos'],
  ["http://www.w3.org/2001/XMLSchema#", 'xsd']
]

puts "Normalizing common prefixes for external ontologies"

Dir['**/*.rdf'].each do |file|  
  next if file.include?('cache')

  puts "Processing file: #{file}"
  text = File.read(file)

  changed = false
  prefixes.each do |uri, prefix|
    if text =~ %r{xmlns:([A-Za-z\-_]+)=["']#{uri}["']} and $1 != prefix
      old_prefix = $1
      puts "  Found prefix #{old_prefix} for #{uri}, changing to #{prefix}"              
      puts "    Changing entity, namespace, and other occurrences..."
      text = text.gsub(%r{<!ENTITY[ ]+#{old_prefix} }, "<!ENTITY #{prefix} ").
        gsub(%r{xmlns:#{old_prefix}=}, "xmlns:#{prefix}=").
        gsub(/#{old_prefix}:([A-Za-z_])/, "#{prefix}:\\1").
        gsub(/&#{old_prefix};/, "&#{prefix};")
      changed = true
    end

    # Check if the prefix appears more than once in the file (indicating multiple declarations)
    prefix_count = text.scan(/xmlns:#{prefix}=/).size
    if prefix_count > 1
      puts "  Warning: Prefix #{prefix} appears #{prefix_count} times in #{file}. Please check for duplicate declarations."
    end
  end

  if changed
    File.open(file, 'w') { |f| f.write(text) }
    puts "  ** Updated prefixes in #{file}"
  end
end
