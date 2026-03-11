# IOF Annotation Principles

## Overview

The IOF AnnotationVocabulary (AV) OWL file (`AnnotationVocabulary`) is the normative source for IOF annotation properties. It includes a superset of the annotation properties discussed in this document along with the metadata about them. This document's purpose is to provide the requirements and instructions for authors of IOF ontologies. The AV should be imported into IOF ontologies under development to make these annotation properties available; however, since the IOF Core imports IOF AV, using AV requires no explicit `owl:imports` statement.

All approved ontologies **MUST** adhere to the following annotation requirements for all constructs.

## RFC 2119 Keywords

The following rules **MUST** be followed when using this document; these are taken from [IETF RFC 2119](https://www.ietf.org/rfc/rfc2119.txt) (simplified):

- **MUST** — This word means that the definition is an absolute requirement of the specification.
- **MUST NOT** — This phrase means that the definition is an absolute prohibition of the specification.
- **SHOULD** — This word means that there may exist valid reasons in particular circumstances to ignore a particular item, but the full implications **MUST** be understood and carefully weighed before choosing a different course.
- **SHOULD NOT** — This phrase means that there may exist valid reasons in particular circumstances when the particular behavior is acceptable or even useful, but the full implications should be understood and the case carefully weighed before implementing any behavior described with this label.
- **MAY** — This word means that an item is truly optional.

---

## Summary of Annotation Requirements

### For every ontology file

- **MUST** provide non-versioned ontology IRI
- **MUST** provide version IRI (`owl:versionIRI`) when released
- **MUST** provide label
- **MUST** provide title
- **MUST** provide abstract
- **MUST** provide copyright
- **MUST** provide license
- **MUST** provide maturity annotation
- **MUST** provide `versionInfo`
- **MUST** provide `changeNotes` for each release

### For all constructs

- **MUST** provide label
- **MUST** provide natural language definition

### For classes

If `iof-av:isPrimitive` is set to `true`:
- **MUST** provide `iof-av:primitiveRationale`
- **MAY** provide first-order logic axioms and semi-formal natural language axioms

If `iof-av:isPrimitive` is set to `false` or not specified:
- **MUST** provide `iof-av:firstOrderLogicDefinition`
- **MUST** provide `iof-av:semiFormalNaturalLanguageDefinition`

### For properties

- **MAY** provide first-order logic axioms and semi-formal natural language axioms
- **SHOULD** provide example

---

## Language Requirements

In cases where a text annotation is needed, an American English language version of that annotation is required and **MUST** use the American English language tag (`xml:lang="en"`). Spelling in American English annotations **MUST** conform to an American dictionary, such as Merriam-Webster. Additional annotations covering the same material but expressed in a different natural language are allowed as long as they incorporate the proper language tag. Text annotations that include a language tag have a default datatype of `rdf:langString`. By definition from the RDFS 1.1 specification, one **MUST NOT** include an explicit datatype when adding an annotation.

---

## Ontology-Level Annotations

The following is an example of the ontology annotations from Core (as seen in the "Active Ontology" tab in Protégé):

```xml
<owl:Ontology rdf:about="https://spec.industrialontologies.org/ontology/core/Core/">
    <rdfs:label xml:lang="en">Core Ontology</rdfs:label>
    <dcterms:abstract>The IOF Core Ontology contains terms and concepts found to be common
    across multiple domains of industry and represents an OWL implementation of them. The
    ontology itself utilizes the Basic Formal Ontology or BFO as a philosophical foundation
    but also imports terms from various domain-independent or "mid-level" ontologies. The
    purpose of the ontology is to serve or is intended to serve as a core for IOF's
    domain-specific ontologies, with a goal being to ensure consistency and interoperability
    across the suite of ontologies the IOF publishes.</dcterms:abstract>
    <dcterms:creator xml:lang="en">IOF Core Working Group</dcterms:creator>
    <dcterms:license rdf:datatype="xsd:anyURI">http://opensource.org/licenses/MIT</dcterms:license>
    <dcterms:publisher xml:lang="en">Industrial Ontology Foundry</dcterms:publisher>
    <dcterms:title>Industrial Ontology Foundry (IOF) Core Ontology</dcterms:title>
    <!-- ... -->
</owl:Ontology>
```

---

## Annotation Properties

### Label — `rdfs:label`

- Each construct **MUST** have at least one natural language label:
  - Exactly one American English language label **MUST** be provided and language-tagged
  - Labels **MUST** be unique across all IOF ontologies and **SHOULD** be unique across all imported non-IOF ontologies in a given natural language
  - Labels for other natural languages **MAY** be provided, but if so they must be language-tagged
- Data property labels **MUST** be a verb phrase starting with `is` for boolean (true/false) or `has` for any other data type
  - Example: `is transferable`
  - Data property labels **SHOULD** end with `value`, e.g. `has numeric value`
- Label text **MUST** be given in lowercase with spaces between words
  - **Exception:** proper names **MUST** use initial upper-case
  - **Exception:** words like DNA that are capitalised in the Oxford English Dictionary **MUST** remain in uppercase
- Acronyms **MUST NOT** be used for label values
  - **Exception:** words like RADAR and DNA with dictionary definitions **MAY** be used
  - Acronyms not found in dictionaries may be provided as an alternative label using `iof-av:acronym`

> **Note:** The IOF annotation vocabulary does not include an annotation property for preferred label. An annotation directly asserted as `rdfs:label` in IOF OWL content is treated as the preferred label.

Alternative (non-preferred) labels **MAY** also be provided using:

| Property | Use |
|---|---|
| `iof-av:synonym` | Alternative labels that are not abbreviations |
| `iof-av:abbreviation` | Shortened alternative labels other than acronyms |
| `iof-av:acronym` | Shortened labels composed of one letter from each word of the preferred label (acronyms) not found in a dictionary |

---

### Natural Language Definition — `iof-av:naturalLanguageDefinition`

Definition: plain text for industry practitioner understanding.

- Exactly one natural language definition **MUST** be given for any construct (both primitive and non-primitive)
- The definition **MUST** adhere to ISO 704 rules and requirements for terminology:
  - For non-primitive constructs, the definition **MUST NOT** be circular
  - For primitive constructs, the definition **SHOULD NOT** be circular
  - The definition **MUST** be substitutable in a sentence where the term appears
  - The definition **MUST NOT** begin with an article (`The`, `A`, or `An`)
  - One **SHOULD** avoid jargon and domain-specific terminology
- It **MUST** be understandable by a practitioner in the industrial domain:
  - **MUST NOT** use specialised ontological terminology (e.g. perdurant, endurant, continuant)
  - Ontological construct labels **MUST** be provided in parenthesis — example: `role held by (bearer of) a material entity …`
  - **MUST NOT** use special formatting for properties or classes referenced in the definition:
    - **MUST NOT** use upper camel case capitalisation
    - **MUST NOT** use apostrophes to contain terms as a parenthetical — e.g. `'part-of'`, `'Information Content Entity'`, `InformationContentEntity` are all wrong
  - **MUST NOT** contain acronyms or abbreviations (unless approved by the Architecture TG)
- If the definition is taken from another source, `dcterms:source` or one of its sub-properties **MUST** cite the original reference

**Examples:**

- `shipment preparation process`: planned process in which some material entities are prepared to be transported together to a receiver's location
- `postal address`: designation of a location (site) to which mail is delivered

---

### Primitive Term Annotations

#### Is Primitive — `iof-av:isPrimitive`

Definition: boolean flag indicating that necessary and sufficient conditions are not provided at this time.

- **MUST** be present if the term does not have necessary and sufficient conditions; value **MUST** be set to `true` (W3C boolean)
- **MUST** only apply to classes
- If necessary and sufficient conditions are present, the annotation **MAY** be provided with value `false`
- **MUST** default to `false`
- If possible, terms **SHOULD** have necessary and sufficient conditions

> **Note:** `iof-av:elucidation` **MUST NOT** be used and is deprecated.

**Examples:**

- `person`: `true`
- `shipment preparation process`: `true`

#### Primitive Rationale — `iof-av:primitiveRationale`

Definition: reason why the necessary and sufficient conditions were not or could not be provided at this time.

- **MUST** only apply to classes
- **MUST** be provided when `isPrimitive` is set to `true`
- **MUST** explain why necessary and sufficient conditions are not possible
- **SHOULD** indicate what is missing if additional work is required

**Examples:**

- `person`: insufficient constructs to create necessary and sufficient conditions
- `shipment preparation process`: shipment preparation process often includes at least one picking, internal movement, packaging, marking, weighing, or loading process, but since those processes are not added to the ontology yet, it is not possible to generate necessary and sufficient conditions at this time for this entity

---

## Logical Annotations

Definitions and axioms in first-order logic must be kept separate from each other. The definition of a term `x` is designed to be the shortest and logically simplest specification of necessary and sufficient conditions for being an instance of `x`. The axioms specify additional characteristics which hold for all such instances.

### Variable Rules

The following rules **MUST** be followed when using variables in a first-order logic axiom or definition:

- **MUST NOT** nest variables in single quotes (e.g. `'instance i'`, `'continuant c'`)
- **MUST** use lower case variables for particulars (individuals/instances) of a universal
- Multiple first-order logic axioms **MUST** be considered as a combined set using the `∧` (conjunction operator)
- Variables **SHOULD** use the first letter of a construct's label when possible
- Variables **MUST** only be one letter
- **MUST** append numeric suffixes (`x1`, `x2`) or primes (`x'`, `x''`) for multiple instances of the same construct
- **MUST** reserve `t`, `t'`, etc. for temporal regions
- **MUST** only use `r`, `r'`, `s`, `s'`, etc. for spatial and spatiotemporal regions
- **MUST** only use `R`, `R'`, etc. for relations
- **MUST NOT** use the character `a` or `A`

### FOL Syntax Rules

References to classes and properties **MUST** use the label, transformed as follows:
- Class labels → `UpperCamelCase` (spaces removed)
- Property labels → `lowerCamelCase` (spaces removed)

**Examples:**

| Label | FOL form |
|---|---|
| `material entity` | `MaterialEntity` |
| `has part at some time` | `hasPartAtSomeTime` |

All terms external to the current ontology **MUST** use a prefix. All prefixes referenced **MUST** be declared in the ontology prefixes.

The syntax **MUST** adhere to standard first-order logic (see [lecture notes](https://www.cs.ox.ac.uk/people/james.worrell/lecture9-2015.pdf)) and **MUST** only use the following symbols:

| Symbol | Meaning | UTF-8 |
|---|---|---|
| `∧` | Conjunction | U+2227 |
| `∨` | Disjunction | U+2228 |
| `¬` | Negation | U+00AC |
| `∃` | Existential Quantification | U+2203 |
| `∀` | Universal Quantification | U+2200 |
| `→` | Implication / Conditional | U+2192 |
| `↔` | Equivalence / Bi-Implication | U+2194 |
| `( )` | Left/Right Parentheses | U+0028 / U+0029 |
| `[ ]` | Left/Right Square Brackets | U+005B / U+005D |
| `{ }` | Left/Right Braces | U+007B / U+007D |

**Example:**

```text
product:
  obo:Continuant(c) ∧ ¬(obo:SpecificallyDependentContinuant(c) ∨ Person(c) ∨ Organization(c))
  ∧ ∃r (ProductRole(r) ∧ obo:hasRole(c, r))
```

---

### First-Order Logic Definition — `iof-av:firstOrderLogicDefinition`

Definition: formal definition of a construct using predicate logic semantics.

- **MUST** occur exactly once if the term is not primitive (`isPrimitive` is `false`)
- **MUST** provide individually necessary and sufficient conditions

---

### Semi-Formal Natural Language Definition — `iof-av:semiFormalNaturalLanguageDefinition`

Definition: transitional definition expressing the first-order logic definition using semantics understandable by an ontologically knowledgeable domain practitioner without predicate logic semantics.

- **MUST** be provided if the term is not primitive (`isPrimitive` is `false`)
- **MUST** only occur once
- Variables **SHOULD** be removed if they do not need to be referenced later in the expression

**Rules for necessary and sufficient conditions:**

- **SHOULD** use `every instance of '{term}' is defined as exactly an instance of {conditions}` for necessary and sufficient conditions

**Example:**

```text
FOL:   Agent(x) ↔ (Person(x) ∨ GroupOfAgents(x) ∨ EngineeredSystem(x)) ∧ ∃y (AgentRole(y) ∧ hasRole(x,y))

SFNL:  every instance of 'agent' is defined as exactly an instance of 'person', 'group of agents',
       or 'engineered system' that 'has role' some 'agent role'
```

**Syntax rules:**

- A construct label **MUST** be used with its exact syntax preserved
- Quotes (`'`) **MUST** surround all labels
- The words `"is a"` **MUST NOT** be used without qualification:
  - Use `"is a subclass of"` for subclass relationships
  - Use `"is an instance of"` for instance-of relationships
- Variables **SHOULD** be used where needed
- All natural language definition rules **MUST** apply otherwise

**Examples:**

- `'product'`: every instance of `'product'` is defined as exactly an instance of (`'continuant'` and not `'person'` and not `'organization'` and not `'specifically dependent continuant'`) that `'bears'` some `'product role'`
- `'agent'`: every instance of `'agent'` is defined as exactly an instance of `'person'`, `'group of agents'`, or `'engineered system'` that `'has role'` some `'agent role'`

---

### First-Order Logic Axiom — `iof-av:firstOrderLogicAxiom`

Definition: axiom of a construct using predicate logic semantics.

- **MAY** be provided for primitive or non-primitive constructs
- A construct **MAY** have more than one first-order logic axiom annotation
- Axiom values **MUST** adhere to first-order logic definition syntax
- Multiple axioms **MUST** be considered as a combined set using the `∧` operator
- If there is more than one axiom, each **MUST** use a prefix `LA<n>:` where `<n>` is a monotonically increasing number starting at 1

**Example:**

```text
iof-av:firstOrderLogicAxiom: "LA1: BusinessFunction(x) → Function(x) ∧ ∃o,∃i(Organization(o) ∧
  ObjectiveSpecification(i) ∧ functionOf(x,o) ∧ genericallyDependsOnAtSomeTime(i,o) ∧
  prescribedBy(x,i)) ∧ ∀y(hasRealization(x,y) → BusinessProcess(y))"

iof-av:firstOrderLogicAxiom: "LA2: Function(x) ∧ ∃o,∃i,∃p(Organization(o) ∧
  ObjectiveSpecification(i) ∧ BusinessProcess(p) ∧ functionOf(x,o) ∧
  genericallyDependsOnAtSomeTime(i,o) ∧ prescribedBy(x,i) ∧ hasRealization(x,p)) →
  BusinessFunction(x)"
```

---

### Semi-Formal Natural Language Axiom — `iof-av:semiFormalNaturalLanguageAxiom`

Definition: transitional definition expressing a first-order logic axiom using semantics understandable by an ontologically knowledgeable domain practitioner without predicate logic semantics.

- **MAY** be provided if the term is primitive (`isPrimitive` is `true`)
- A construct **MAY** include more than one
- **MUST** adhere to semi-formal natural language definition syntax
- If there is more than one axiom, each **MUST** use the same `LA<n>:` prefix as the corresponding FOL axiom

**Patterns for axioms:**

- **SHOULD** use `if ... then ...` for necessary or sufficient axioms (implication pattern)
- **SHOULD** use `some type of` for a universal pattern
- **SHOULD** use `whenever` when representing a multi-place temporal expression

**Complete example with multiple axioms:**

```text
iof-av:firstOrderLogicAxiom "LA1: Assembly(x) → MaterialArtifact(x) ∧ ∃c,∃c'(MaterialComponent(c)
  ∧ MaterialComponent(c') ∧ componentPartOfAtAllTimes(c,x) ∧ componentPartOfAtAllTimes(c',x)
  ∧ ¬(c=c' ∨ componentPartOfAtAllTimes(c,c') ∨ componentPartOfAtAllTimes(c',c)))"

iof-av:semiFormalNaturalLanguageAxiom "LA1: if x is an 'assembly' then x is a 'material artifact'
  and there are at least two distinct 'material components' that are 'component part of at all times' x"

iof-av:firstOrderLogicAxiom "LA2: MaterialArtifact(x) ∧ ∃p(AssemblyProcess(p)
  ∧ isSpecifiedOutputOf(x,p)) → Assembly(x)"

iof-av:semiFormalNaturalLanguageAxiom "LA2: material artifact x that 'is specified output of'
  some 'assembly process' p implies x is an 'assembly'"
```

---

## Example Annotations — `skos:example`

Definition: supplies an example of the use of a concept [skos].

- **MUST** provide a correct use of the construct in a domain context
- Constructs **SHOULD** include an example

**Example:**

```turtle
ex:organizationsOfScienceAndCulture skos:example "academies of science, general museums, world fairs"
```

---

## Source Annotations

### Is Defined By — `rdfs:isDefinedBy`

Definition: indicates a resource defining the subject resource. This property may be used to indicate an RDF vocabulary in which a resource is described. The IRI of the ontology where the construct is defined or curated.

> **Note:** Individuals **MUST** also be annotated with `rdfs:isDefinedBy`.

### Was Defined By — `iof-av:wasDefinedBy`

Definition: identifies the occurrence time and former location for a construct, annotation, or individual.

- **MUST** have two sub-annotations: `iof-av:wasMovedFrom` and `iof-av:wasMovedOn`

#### `iof-av:wasMovedFrom`
Definition: part of a `wasDefinedBy` annotation indicating the previous ontology a construct was located in.
Type: `xsd:anyURI`

#### `iof-av:wasMovedOn`
Definition: part of a `wasDefinedBy` annotation indicating the date and time a construct's location was changed.
Type: `xsd:dateTime`

### See Also — `rdfs:seeAlso`

Definition: indicates a resource that might provide additional information about the subject resource [rdfs].

- The reference **MUST** be a concise reference to the related documentation
- The reference **SHOULD** be a URL if possible, otherwise a brief description

### Replaced By — `iof-av:replacedBy`

Definition: reference to the IRI of the target of a deprecated construct.

- The value **MUST** be an IRI referencing the target construct

---

## Addressing Citations

A source is a related resource from which the described resource is derived. A source annotation **SHOULD** be attached to the element where the influence of the source manifests (an entire construct or a specific annotation such as a natural language definition). A source annotation **SHOULD** be concise, in the form of a URL, bibliographic citation, or other standard description.

| Property | Definition |
|---|---|
| `iof-av:directSource` | Definitive source of the subject resource |
| `iof-av:adaptedFrom` | Source for the resource that was modified to create the subject resource |

---

## Removed or Renamed Constructs

In cases where a construct is removed or renamed, it **MUST** be marked as `owl:deprecated`. The following annotations **MUST** be used:

- `owl:deprecated` annotation **MUST** have the value `true`
- All axioms **MUST** be removed, except the subclass axiom **SHOULD** be preserved
- If the local name changes, `iof-av:replacedBy` **MUST** be added containing the IRI of the new local name
- All construct annotations except `owl:deprecated` and `iof-av:replacedBy` **MUST** be removed
- `skos:changeNote` **MUST** record the rationale for the deprecation, the version IRI in which it was deprecated, and a change note associated with the deprecated element

**For changes to the local name:**

- The user **MAY** add `owl:equivalentClass` or `owl:equivalentProperty` referencing the destination construct IRI
- `owl:sameAs` **MAY** be used for nominals as appropriate
- The user **SHOULD** change their ontology to use the new constructs

---

## Notes

### Comment — `rdfs:comment`

`rdfs:comment` **MUST NOT** be used. Use one of the following instead:

| Property | Use |
|---|---|
| `iof-av:explanatoryNote` | Supplemental information to clarify or describe the construct |
| `iof-av:usageNote` | Describes how to use the term in particular situations |
| `skos:scopeNote` | Additional domain contextualisation on the use of the term |
| `skos:changeNote` | Records changes; **MUST** include a Jira issue reference and brief description |

**`iof-av:explanatoryNote` example:**

> "Item is another term semantically close to Product. But it is more general because the Item may not be sellable. It is an overloaded term used by information systems to capture catalog information about real and sort of unreal (e.g., product family or option class) materials the enterprise concerns with."

**`iof-av:usageNote` example:**

> "This is how the Supplying Relation class may be used to convey who supplies what to who. `SupplierRole(sr1)` and `BuyerRole(br1)` and `Product(p1)` and `SupplyingRelation(s1)` and `specificallyDependsOn(s1, sr1)` and `specificallyDependsOn(br1, s1)` and `specificallyDependsOn(p1,s1)`"

---

## Synonyms and Abbreviations

General rule: synonyms and abbreviations **MUST** include a language tag (`xml:lang`).

| Property | Definition | Use |
|---|---|---|
| `iof-av:synonym` | Alternate label that may help users discover the construct | **MAY** be used for alternate terms; if context-specific, **SHOULD** be supplemented with `skos:scopeNote` |
| `iof-av:symbol` | Terse designation (abbreviation) for the construct | **SHOULD** be used when a commonly used abbreviation exists, such as chemical symbols or units of measure (e.g. `m`, `C`) |
| `iof-av:abbreviation` | Alternate short label for the element | **SHOULD** be used when there is an alternate short label; **MUST** use `symbol` if the abbreviation is a chemical or unit of measure |
| `iof-av:acronym` | Specialised abbreviation composed of one letter from each word of the preferred label | **SHOULD** be used when there is a commonly accepted acronym (e.g. `PLM`, `CAD`) |

---

## Maturity

Maturity designates an ontology's development status and how it integrates into the development and release process.

| Value | Meaning |
|---|---|
| `iof-av:Released` | The ontology is a normative part of the IOF ontologies. Once released, the non-versioned IRI **MUST** refer to an ontology with maturity `Released`. A released ontology **MUST NOT** depend on any provisional ontology. Release notes **MUST** be provided for any changes. |
| `iof-av:Provisional` | The ontology is under development and may contain errors or omissions. Provisional ontologies are subject to change. |

A maturity annotation encompasses an entire ontology; all constructs, axioms, and annotations in that file share the same maturity.

### Maturity — `iof-av:maturity`

Definition: annotation property used to indicate the development status of an ontology.

- Each IOF ontology **MUST** have exactly one maturity annotation with a value of type `iof-av:MaturityLevel`

---

## Ontology-Level Annotation Properties

The following annotations apply to an entire IOF ontology and not to individual constructs.

| Property | Requirement | Definition |
|---|---|---|
| `iof-av:copyright` | **MUST** | Originator's and authorised entity's exclusive legal right to print, distribute, and publish material |
| `dcterms:license` | **MUST** | Legal document giving official permission to do something with the resource |
| `dcterms:abstract` | **MUST** | A summary of the resource |
| `iof-av:maturity` | **MUST** | Default maturity level of the ontology |
| `owl:versionInfo` | **MUST** | Release version number; value **MUST** be the numeric version component (YYYYNN) of the release version IRI |

---

## Prefixes and Namespaces

This document identifies each annotation property using an abbreviated form of its full IRI with the structure `<prefix>:<local name>`, where the prefix represents the namespace IRI and the local name is the identifier for the resource within that namespace. The full IRI is the concatenation of the local name to the namespace IRI — for example, `skos:scopeNote` represents `http://www.w3.org/2004/02/skos/core#scopeNote`.

| Prefix | Namespace |
|---|---|
| `iof-av:` | `https://spec.industrialontologies.org/ontology/core/meta/AnnotationVocabulary/` |
| `rdfs:` | `http://www.w3.org/2000/01/rdf-schema#` |
| `owl:` | `http://www.w3.org/2002/07/owl#` |
| `dcterms:` | `http://purl.org/dc/terms/` |
| `skos:` | `http://www.w3.org/2004/02/skos/core#` |
| `xsd:` | `http://www.w3.org/2001/XMLSchema#` |
| `obo:` | `http://purl.obolibrary.org/obo/` |
