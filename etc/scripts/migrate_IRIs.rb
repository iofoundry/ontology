require 'rexml/document'

if ARGV.length != 1
  puts "Usage: migrate_IRIs.rb <path to xml file>"
  exit
end

ontology_file = ARGV[0]

context = { raw: :all }
doc = REXML::Document.new(File.read(ontology_file), context)

# find the IRI for the ontology
ontologies = doc.root.get_elements("//owl:Ontology")
if ontologies.length != 1
  puts "Error: Expected exactly one owl:Ontology element, found #{ontologies.length}"
  exit
end

ontology = ontologies.first
ontology_iri = ontology.attributes["rdf:about"]
puts "Ontology IRI: #{ontology_iri}"

# Clean up the entities by replace the prefixes with the new IRIs
puts "Changing entity IRIs..."
core = doc.doctype.find { |e| e.value == ontology_iri }
core.replace_with(REXML::Entity.new(core.name, 'https://spec.industrialontologies.org/ontology/construct/'))

av = doc.doctype.find { |e| e.value == 'https://spec.industrialontologies.org/ontology/core/meta/AnnotationVocabulary/' }
av.replace_with(REXML::Entity.new(av.name, 'https://spec.industrialontologies.org/ontology/annotation/'))

new_doctype = REXML::DocType.new(doc.doctype.clone)
doc.doctype.each do |ent|
  new_doctype.add(ent.clone)
end
doc.add(new_doctype)

puts doc.doctype.to_s

puts "Updating namespace declarations..."

root = doc.root

root.add_namespace(core.name, 'https://spec.industrialontologies.org/ontology/construct/')
root.add_namespace(av.name, 'https://spec.industrialontologies.org/ontology/annotation/')

puts "Adding rdfs:isDefinedBy to entities..."

root.each_element("//owl:Class | //owl:ObjectProperty | //owl:DatatypeProperty | //owl:NamedIndividual") do |elem|
  about = elem.attributes['rdf:about']
  if about && about.start_with?('https://spec.industrialontologies.org/ontology/')
    puts "Adding rdfs:isDefinedBy to #{elem.name} IRI: #{about}"
    defined_by = REXML::Element.new('rdfs:isDefinedBy', elem)
    defined_by.text = ontology_iri
    defined_by.add_attribute('rdf:datatype', 'http://www.w3.org/2001/XMLSchema#anyURI')
  end
end

# Write the modified XML back to the file
File.open("Core2.rdf", 'w') do |file|
  doc.write(output: file, indent: -1, transitive: false)
end