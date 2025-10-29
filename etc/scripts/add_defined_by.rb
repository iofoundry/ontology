require 'rexml/document'

if ARGV.length != 1
  puts "Usage: migrate_IRIs.rb <path to rdf file>"
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

root.each_element("/rdf:RDF/owl:Class | /rdf:RDF/owl:ObjectProperty | /rdf:RDF/owl:DatatypeProperty | /rdf:RDF/owl:NamedIndividual | /rdf:RDF/owl:AnnotationProperty") do |elem|
  about = elem.attributes['rdf:about']
  if about && (about.start_with?('&iof-') or about.start_with?('https://spec.industrialontologies.org/ontology/'))
    if elem.get_elements('rdfs:isDefinedBy').empty?
      puts " * Adding rdfs:isDefinedBy to #{elem.name} IRI: #{about}"
      REXML::Text.new("  ", true, elem)
      defined_by = REXML::Element.new('rdfs:isDefinedBy', elem)
      defined_by.text = ontology_iri
      defined_by.add_attribute('rdf:datatype', 'http://www.w3.org/2001/XMLSchema#anyURI')
      REXML::Text.new("\n  ", true, elem)
    end
  end
end

File.open(ontology_file, 'w') do |file|
  doc.write(output: file, indent: -1, transitive: false)
end
