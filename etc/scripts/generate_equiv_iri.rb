
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

ontology_file = ARGV[0]
version = ARGV[1]

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

doc.doctype.each do |ent|
  doctype_clone.add(ent.clone)
end

equiv_root = REXML::Element.new('rdf:RDF')

rdf_ns = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#'
rdf_prefix = nil
owl_ns = 'http://www.w3.org/2002/07/owl#'
owl_prefix = nil
root.namespaces.each do |prefix, uri|
  equiv_root.add_namespace(prefix, uri)
  rdf_prefix = prefix if uri == rdf_ns
  owl_prefix = prefix if uri == owl_ns
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
equiv_ont = REXML::Element.new("#{owl_prefix}:Ontology")
equiv_ont.add_attribute("#{rdf_prefix}:about", equiv_iri)
equiv_ont.add_element("#{owl_prefix}:imports", { "#{rdf_prefix}:resource" => ontology_iri })

equiv_root.add_element(equiv_ont)

root.each_element("//owl:Ontology") do |ont|
  ["dcterms:title", "dcterms:license", "dcterms:publisher", 
  "iof-av:copyright", "iof-av:maturity"].each do |tag|
    ont.each_element(tag) do |elem|
      if elem.text && !elem.text.strip.empty?
        e = elem.clone
        e.text = elem.text.strip
        equiv_ont.add_element(e)
      end
    end
  end
  ont.each_element("rdfs:label") do |elem|
    if elem.text && !elem.text.strip.empty?
      e = elem.clone
      e.text = "#{elem.text.strip} Replacements"
      equiv_ont.add_element(e)
    end
  end
end

{ "/#{rdf_prefix}:RDF/#{owl_prefix}:Class" => ["Class", 'equivalentClass'],
  "/#{rdf_prefix}:RDF/#{owl_prefix}:ObjectProperty" => ["ObjectProperty", 'equivalentProperty'],
  "/#{rdf_prefix}:RDF/#{owl_prefix}:DatatypeProperty" => ["DatatypeProperty", 'equivalentProperty'],
  "/#{rdf_prefix}:RDF/#{owl_prefix}:AnnotationProperty" => ["AnnotationProperty", 'equivalentProperty'],
  "/#{rdf_prefix}:RDF/#{owl_prefix}:NamedIndividual" => ["NamedIndividual", 'sameAs'] }.each do |xpath, equiv_tags|
  root.each_element(xpath) do |elem|
    iri = elem.attributes["rdf:about"]
    next if iri.nil? || iri.empty?
    puts "Processing #{elem.name}: #{iri}"

    name = iri.split('/').last

    desc = REXML::Element.new("#{owl_prefix}:#{equiv_tags[0]}")
    desc.add_attribute("#{rdf_prefix}:about", "#{ontology_iri}#{name}")

    equiv = REXML::Element.new("#{owl_prefix}:#{equiv_tags[1]}")
    equiv.add_attribute("#{rdf_prefix}:resource", iri)

    dep = REXML::Element.new("#{owl_prefix}:deprecated")
    dep.add_attribute("#{rdf_prefix}:datatype", 'http://www.w3.org/2001/XMLSchema#boolean')
    dep.text = 'true'

    desc.add_element(equiv)
    desc.add_element(dep)
    equiv_root.add_element(desc)
  end
end

equiv_doc.add_element(equiv_root)
path = "migration/#{version}"
FileUtils.mkdir_p(path) unless Dir.exist?(path)
file = "migration/#{version}/#{File.basename(ontology_file, '.rdf')}Replacements.rdf"
File.open(file, "w") do |f|
  equiv_doc.write(output: f, indent: 2, transitive: false)
end