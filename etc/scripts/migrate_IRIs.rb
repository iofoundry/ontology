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

# Collect the iris for the IOF related ontologies and create the new doctype with non-IOF entities. We will also 
# remove the old IOF namespaces from the root element.
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

iri_pattern = iof_iris.map { |prefix, iri| "\\&#{prefix};" }.join('|')
p iri_pattern

# Add new IOF entities for construct, individual, and annotation vocabulary
ind = REXML::Entity.new('iof-ind', 'https://spec.industrialontologies.org/ontology/individual/')
doc.doctype.add(ind)

const = REXML::Entity.new('iof-const', 'https://spec.industrialontologies.org/ontology/construct/')
doc.doctype.add(const)

av = REXML::Entity.new('iof-av', 'https://spec.industrialontologies.org/ontology/annotation/')
doc.doctype.add(av)

puts doc.doctype.to_s
puts "Updating namespace declarations..."

# Add the new namespaces to the root element
root.add_namespace(const.name, const.value)
root.add_namespace(ind.name, ind.value)
root.add_namespace(av.name, av.value)

puts "Updating the IOF ontology maturity level..."
# Update the maturity of the ontology use the individual IRI
ontology.each_element("iof-av:maturity") do |maturity|
  maturity.attributes["rdf:resource"] = maturity.attributes["rdf:resource"].sub('annotation', 'individual')
end

puts "Adding rdfs:isDefinedBy to entities..."

# Add the rdfs:isDefinedBy annotation to all entities with an IRI starting with &iof-
root.each_element("/rdf:RDF/owl:Class | /rdf:RDF/owl:ObjectProperty | /rdf:RDF/owl:DatatypeProperty | /rdf:RDF/owl:NamedIndividual | /rdf:RDF/owl:AnnotationProperty") do |elem|
  about = elem.attributes['rdf:about']
  puts "Checking #{elem.name} IRI: #{about}"
  if about && (about =~ /#{iri_pattern}/ or about.start_with?('https://spec.industrialontologies.org/ontology/'))
    # We handle NamedIndividuals differently because they share the same IRI prefix as the constructs
    puts " * Found IOF IRI to update: #{about}"
    if elem.name == 'NamedIndividual'
      iri = about.sub(/#{iri_pattern};([A-Za-z0-9]+)/, 'https://spec.industrialontologies.org/ontology/individual/\1')
      puts " * Updating NamedIndividual IRI: #{about} to #{iri}"
      elem.attributes['rdf:about'] = iri

      # Changed the resources referenced in the named individuals
      elem.each_element_with_attribute("rdf:resource") do |sub|
        resource = sub.attributes['rdf:resource']
        if resource && (resource.start_with?('https://spec.industrialontologies.org/ontology/') or resource =~ /#{iri_pattern}/)
          if sub.name == 'type'
            rep = 'https://spec.industrialontologies.org/ontology/construct/\2'
          else
            rep = 'https://spec.industrialontologies.org/ontology/individual/\2'
          end
          new_resource = resource.sub(%r{(#{iri_pattern}|https://spec.industrialontologies.org/ontology/[a-z/]+/[A-Za-z]+/)([A-Za-z0-9]+)$}, 
            rep)
          puts "   * Updating #{sub.prefix} : #{sub.name} resource #{resource} to #{new_resource}"
          if iof_iris.key?(sub.prefix)
            puts "     - Changing prefix #{sub.prefix} to iof-const"
            sub.name = "iof-const:#{sub.name}"
          end
          p sub
          sub.attributes['rdf:resource'] = new_resource
        end
      end
    elsif about.start_with?('https://spec.industrialontologies.org/ontology/') or about =~ /#{iri_pattern}/
      if about.include?('/individual/') 
        rep = 'https://spec.industrialontologies.org/ontology/individual/\2' 
      else 
        rep = 'https://spec.industrialontologies.org/ontology/construct/\2' 
      end
      iri = about.sub(%r{(#{iri_pattern}|https://spec.industrialontologies.org/ontology/[a-z/]+/[A-Za-z]+/)([A-Za-z]+)$}, rep)
      puts "   * Updating IRI: #{about} to #{iri}"
      elem.attributes['rdf:about'] = iri
    end
    puts " * Adding rdfs:isDefinedBy to #{elem.name} IRI: #{about}"
    REXML::Text.new("  ", true, elem)
    defined_by = REXML::Element.new('rdfs:isDefinedBy', elem)
    defined_by.text = ontology_iri
    defined_by.add_attribute('rdf:datatype', 'http://www.w3.org/2001/XMLSchema#anyURI')
    REXML::Text.new("\n  ", true, elem)
  end
end

# Replace iof-av:replacedBy annotations to point to the new IRI
root.each_element("//iof-av:replacedBy") do |replaced_by|
  iri = replaced_by.text
  new_iri = iri.sub(%r{https://spec.industrialontologies.org/ontology/[a-z/]+/[A-Za-z]+/([A-Za-z]+)$}, 'https://spec.industrialontologies.org/ontology/construct/\1')
  puts "  * iof-av:replacedBy: replacing #{iri} with new IRI #{new_iri}"
  replaced_by.text = new_iri
end

# Check for all resource references for onProperty, someValuesFrom, allValuesFrom, and equivalentClass
puts "\nUpdating resource references..."
root.each_element("//rdfs:subClassOf |//owl:onProperty | //owl:someValuesFrom | //owl:allValuesFrom | //owl:equivalentClass | //rdfs:domain | //rdfs:range | //owl:inverseOf | //owl:annotatedSource") do |elem|
  resource = elem.attributes['rdf:resource']
  if resource && (resource.start_with?('https://spec.industrialontologies.org/ontology/') or resource =~ /#{iri_pattern}/)
    new_resource = resource.sub(%r{(#{iri_pattern}|https://spec.industrialontologies.org/ontology/[a-z/]+/[A-Za-z]+/)([A-Za-z]+)$}, 'https://spec.industrialontologies.org/ontology/construct/\2')
    puts "  * Updating #{elem.name} resource #{resource} to #{new_resource}"
    elem.attributes['rdf:resource'] = new_resource
  end
end

# Check for all resource references for onProperty, someValuesFrom, allValuesFrom, and equivalentClass
puts "\nUpdating resource references..."
root.each_element("//rdf:Description") do |elem|
  resource = elem.attributes['rdf:about']
  if resource && (resource.start_with?('https://spec.industrialontologies.org/ontology/') or resource =~ /#{iri_pattern}/)
    new_resource = resource.sub(%r{(#{iri_pattern}|https://spec.industrialontologies.org/ontology/[a-z/]+/[A-Za-z]+/)([A-Za-z]+)$}, 'https://spec.industrialontologies.org/ontology/construct/\2')
    puts "  * Updating #{elem.name} about #{resource} to #{new_resource}"
    elem.attributes['rdf:about'] = new_resource
  end
end

# Write the modified XML back to the file
output_file = File.dirname(ontology_file) + '/' + File.basename(ontology_file, '.rdf') + '_new.rdf'
File.open(output_file, 'w') do |file|
  doc.write(output: file, indent: -1, transitive: false)
end

exec("serialize #{output_file}")