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

# Collect the iris for the IOF related ontologies 
iof_iris = {}
onto_prefix = ''
new_doctype = REXML::DocType.new(doc.doctype.clone)
doc.doctype.each do |ent|
  if ent.value.start_with?('https://spec.industrialontologies.org/ontology/')
    iof_iris[ent.name] = ent.value
    onto_prefix = ent.name if ent.value == ontology_iri
    root.delete_namespace(ent.name)
  else
    new_doctype.add(ent.clone)
  end
end
doc.add(new_doctype)

# Determine if there are any named individuals
ind = REXML::Entity.new('iof-ind', 'https://spec.industrialontologies.org/ontology/individual/')
doc.doctype.add(ind)

const = REXML::Entity.new('iof-const', 'https://spec.industrialontologies.org/ontology/construct/')
doc.doctype.add(const)

av = REXML::Entity.new('iof-av', 'https://spec.industrialontologies.org/ontology/annotation/')
doc.doctype.add(av)

puts doc.doctype.to_s
puts "Updating namespace declarations..."

root.add_namespace(const.name, const.value)
root.add_namespace(ind.name, ind.value)
root.add_namespace(av.name, av.value)

puts "Updating the IOF ontology maturity level..."
# Update the maturity of the ontology use the individual IRI
ontology.each_element("iof-av:maturity") do |maturity|
  maturity.attributes["rdf:resource"] = maturity.attributes["rdf:resource"].sub('annotation', 'individual')
end

puts "Adding rdfs:isDefinedBy to entities..."

root.each_element("//owl:Class | /rdf:RDF/owl:ObjectProperty | /rdf:RDF/owl:DatatypeProperty | /rdf:RDF/owl:NamedIndividual | /rdf:RDF/owl:AnnotationProperty") do |elem|
  about = elem.attributes['rdf:about']
  puts "Checking #{elem.name} IRI: #{about}"
  if about && about.start_with?('&iof-')
    if elem.name == 'NamedIndividual'
      iri = about.sub(onto_prefix, 'iof-ind')
      puts " * Updating NamedIndividual IRI: #{about} to #{iri}"
      elem.attributes['rdf:about'] = iri
    end
    puts " * Adding rdfs:isDefinedBy to #{elem.name} IRI: #{about}"
    defined_by = REXML::Element.new('rdfs:isDefinedBy', elem)
    defined_by.text = ontology_iri
    defined_by.add_attribute('rdf:datatype', 'http://www.w3.org/2001/XMLSchema#anyURI')
  end
end

new_onto = ""
doc.write(output: new_onto, indent: -1, transitive: false)

mappings = iof_iris.map do |prefix, iri| 
  if iri == 'https://spec.industrialontologies.org/ontology/core/meta/AnnotationVocabulary/'
    [prefix, 'iof-av'] if prefix != 'iof-av'
  else
    [prefix, 'iof-const']
  end
end.compact

mappings.each do |old_prefix, new_prefix|
  puts "Replacing prefix #{old_prefix} with #{new_prefix}"
  new_onto.gsub!(/#{old_prefix}/, new_prefix)
end

# Write the modified XML back to the file
File.open(File.basename(ontology_file, '.rdf') + '_new.rdf', 'w') do |file|
  file.write(new_onto)
end