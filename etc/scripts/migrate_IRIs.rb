require 'rexml/document'

if ARGV.length != 1
  puts "Usage: migrate_IRIs.rb <path to xml file>"
  exit
end

ontology_file = ARGV[0]

context = { raw: :all }
doc = REXML::Document.new(File.read(ontology_file), context)
root = doc.root

# find the IRI for the ontology
ontologies = root.get_elements("//owl:Ontology")
if ontologies.length != 1
  puts "Error: Expected exactly one owl:Ontology element, found #{ontologies.length}"
  exit
end

ontology = ontologies.first
ontology_iri = ontology.attributes["rdf:about"]
puts "Ontology IRI: #{ontology_iri}"

# Determine if there are any named individuals
ind = REXML::Entity.new('iof-ind', 'https://spec.industrialontologies.org/ontology/individual/')
doc.doctype.add(ind)

# Clean up the entities by replace the prefixes with the new IRIs
puts "Changing entity IRIs..."
if ontology_iri != 'https://spec.industrialontologies.org/ontology/core/meta/AnnotationVocabulary/'
  core = doc.doctype.find { |e| e.value == ontology_iri }
  core.replace_with(REXML::Entity.new(core.name, 'https://spec.industrialontologies.org/ontology/construct/'))
end

av = doc.doctype.find { |e| e.value == 'https://spec.industrialontologies.org/ontology/core/meta/AnnotationVocabulary/' }
av.replace_with(REXML::Entity.new(av.name, 'https://spec.industrialontologies.org/ontology/annotation/'))

new_doctype = REXML::DocType.new(doc.doctype.clone)
doc.doctype.each do |ent|
  new_doctype.add(ent.clone)
end
doc.add(new_doctype)

puts doc.doctype.to_s

puts "Updating namespace declarations..."

root.add_namespace(core.name, 'https://spec.industrialontologies.org/ontology/construct/') if core
root.add_namespace(ind.name, ind.value) if ind
root.add_namespace(av.name, 'https://spec.industrialontologies.org/ontology/annotation/')

puts "Updating the IOF ontology maturity level..."
# Update the maturity of the ontology use the individual IRI
ontology.each_element("iof-av:maturity") do |maturity|
  maturity.attributes["rdf:resource"] = maturity.attributes["rdf:resource"].sub('annotation', 'individual')
end

puts "Adding rdfs:isDefinedBy to entities..."

root.each_element("//owl:Class | /rdf:RDF/owl:ObjectProperty | /rdf:RDF/owl:DatatypeProperty | /rdf:RDF/owl:NamedIndividual | /rdf:RDF/owl:AnnotationProperty") do |elem|
  about = elem.attributes['rdf:about']
  if about && about.start_with?('https://spec.industrialontologies.org/ontology/')
    if elem.name == 'NamedIndividual'
      iri = about.sub('annotation', 'individual')
      puts "* Updating NamedIndividual IRI: #{about} to #{iri}"
      elem.attributes['rdf:about'] = iri
    end
    puts "Adding rdfs:isDefinedBy to #{elem.name} IRI: #{about}"
    defined_by = REXML::Element.new('rdfs:isDefinedBy', elem)
    defined_by.text = ontology_iri
    defined_by.add_attribute('rdf:datatype', 'http://www.w3.org/2001/XMLSchema#anyURI')
  end
end

# Write the modified XML back to the file
File.open(File.basename(ontology_file, '.rdf') + '_new.rdf', 'w') do |file|
  doc.write(output: file, indent: -1, transitive: false)
end