
# For each class in the ontology, generate an owl:equivalentClass triple to link to each of the old IRIs
# Example:
# <rdf:Description rdf:about="...">
#	  <owl:equivalentClass rdf:resource="..."/>
#	</rdf:Description>

require 'rexml/document'
require 'uri'
require 'fileutils'

if ARGV.length != 2
  puts "Usage: migrate_IRIs.rb <path to rdf file> <version>"
  exit
end

ontology_file, version = ARGV

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

# Collect the iris for the IOF related ontologies and create the new doctype with non-IOF entities. We will also 
# remove the old IOF namespaces from the root element.

# Create a new RDF file with the 
equiv_doc = REXML::Document.new
equiv_doc.add(REXML::XMLDecl.new('1.0', 'UTF-8'))
equiv_doc.add(doctype_clone = REXML::DocType.new(doc.doctype.clone))

NS = {
 "http://purl.org/dc/terms/" => :dc,
 "http://www.w3.org/2002/07/owl#" => :owl,
 "http://www.w3.org/1999/02/22-rdf-syntax-ns#" => :rdf,
 "http://www.w3.org/2000/01/rdf-schema#" => :rdfs,
 "http://www.w3.org/2004/02/skos/core#" => :skos,
 "http://www.w3.org/2001/XMLSchema#" => :xsd,
 "https://spec.industrialontologies.org/ontology/annotation/" => :iof_av,
 "https://spec.industrialontologies.org/ontology/construct/" => :iof_const,
 "https://spec.industrialontologies.org/ontology/individual/" => :iof_ind
}

doc.doctype.each do |ent|
  doctype_clone.add(ent.clone)
end

equiv_root = REXML::Element.new('rdf:RDF')
PR = {}

root.namespaces.each do |prefix, uri|
  next if prefix == 'xmlns'
  if NS.key?(uri)
    PR[NS[uri]] = prefix
    equiv_root.add_namespace(prefix, uri)
  end
end

{ 
  'iof-oldav' => 'https://spec.industrialontologies.org/ontology/core/meta/AnnotationVocabulary/',
  'iof-oldcore' => 'https://spec.industrialontologies.org/ontology/core/Core/'
}.each do |prefix, uri|
  equiv_root.add_namespace(prefix, uri)
  doctype_clone.add(REXML::Entity.new(prefix, uri))
end

if ontology_iri !~ %r{^https://spec.industrialontologies.org/ontology/core/}
  prefix = 'iof-oldont'
  equiv_root.add_namespace(prefix, ontology_iri)
  doctype_clone.add(REXML::Entity.new(prefix, ontology_iri))
end

uri = URI.parse(ontology_iri)
equiv_iri = "#{uri.origin}/migration/#{version}/#{uri.path.split('/').last}/"

# Add an ontology declaration to the new equivalence file
equiv_ont = equiv_root.add_element("#{PR[:owl]}:Ontology", { "#{PR[:rdf]}:about" => equiv_iri })
equiv_ont.add_element("#{PR[:owl]}:imports", { "#{PR[:rdf]}:resource" => ontology_iri })

root.each_element("//#{PR[:owl]}:Ontology") do |ont|
  ["#{PR[:dc]}:title", "#{PR[:dc]}:license", "#{PR[:dc]}:publisher", 
  "#{PR[:iof_av]}:copyright", "#{PR[:iof_av]}:maturity"].each do |tag|
    ont.each_element(tag) do |elem|
      if elem.text && !elem.text.strip.empty?
        equiv_ont.add_element(elem.clone).text = elem.text
      end
    end
  end
  ont.each_element("#{PR[:rdfs]}:label") do |elem|
    if elem.text && !elem.text.strip.empty?
      equiv_ont.add_element(elem.clone).text = "#{elem.text.strip} Replacements"
    end
  end
end

{ "/#{PR[:rdf]}:RDF/#{PR[:owl]}:Class" => "#{PR[:owl]}:equivalentClass",
  "/#{PR[:rdf]}:RDF/#{PR[:owl]}:ObjectProperty" => "#{PR[:owl]}:equivalentProperty",
  "/#{PR[:rdf]}:RDF/#{PR[:owl]}:DatatypeProperty" => "#{PR[:owl]}:equivalentProperty",
  "/#{PR[:rdf]}:RDF/#{PR[:owl]}:AnnotationProperty" => "#{PR[:iof_av]}:replacedBy",
  "/#{PR[:rdf]}:RDF/#{PR[:owl]}:NamedIndividual" => "#{PR[:owl]}:sameAs" }.each do |xpath, equiv_tag|
  root.each_element(xpath) do |elem|
    type = "#{elem.prefix}:#{elem.name}"
    iri = elem.attributes["rdf:about"]
    next if iri.nil? || iri.empty? || iri !~ %r{^https://spec.industrialontologies.org/ontology/}
    puts "Processing #{elem.name}: #{iri}"

    name = iri.split('/').last
    node = equiv_root.add_element(type, { "#{PR[:rdf]}:about" => "#{ontology_iri}#{name}" })

    equiv = node.add_element(equiv_tag)
    if equiv_tag == "#{PR[:iof_av]}:replacedBy"
      equiv.add_attribute("#{PR[:rdf]}:datatype", 'http://www.w3.org/2001/XMLSchema#anyURI')
      equiv.text = iri
    else
      equiv.add_attribute("#{PR[:rdf]}:resource", iri)
    end

    node.add_element("#{PR[:owl]}:deprecated", 
      { "#{PR[:rdf]}:datatype" => 'http://www.w3.org/2001/XMLSchema#boolean' }).
      text = 'true'
  end
end

equiv_doc.add_element(equiv_root)
path = "migration/#{version}"
FileUtils.mkdir_p(path) unless Dir.exist?(path)
file = "migration/#{version}/#{File.basename(ontology_file, '.rdf')}Replacements.rdf"
File.open(file, "w") do |f|
  equiv_doc.write(output: f, indent: 2, transitive: false)
end