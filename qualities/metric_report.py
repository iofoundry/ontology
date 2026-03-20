#!/usr/bin/env python3
"""
Readable Metric Report Script for Ontology Modules with Detailed Documentation

This script scans a specified directory for ontology files (.owl, .ttl, .rdf) and computes a
variety of metrics using rdflib. The metrics include:
  - Counts for classes, properties, labels, comments, and owl:imports.
  - Hierarchy metrics (maximum/average depth and breadth based on rdfs:subClassOf relationships).
  - Graph connectivity metrics (average and maximum node degree using networkx, if available).
  - AdaptedFrom sources are aggregated by namespace.
  - Optional logical consistency checking via Owlready2.
  - Transitive subclass counts for specified IRIs (i.e. all subclasses in the hierarchy, not just direct children).

Each section of the Markdown report includes natural language documentation to explain how the metrics were computed.
Usage:
    python metric_report.py --directory path/to/ontologies \
                            --subclass-iri http://example.org/ClassA http://example.org/ClassB \
                            --reason
The report is written to report.md (by default).
"""

import os
import glob
import argparse
from collections import defaultdict
from rdflib import Graph, RDF, RDFS, OWL, URIRef, Namespace

# Define the adaptedFrom annotation property
ADAPTED_FROM_IRI = URIRef("https://spec.industrialontologies.org/ontology/core/meta/AnnotationVocabulary/adaptedFrom")
# File extensions for ontology files
ONTOLOGY_EXTENSIONS = ["*.owl", "*.ttl", "*.rdf"]

# Define the Dublin Core Terms namespace for abstract retrieval
DCTERMS = Namespace("http://purl.org/dc/terms/")

def gather_file_list(directory):
    """Collect ontology files in the specified directory."""
    files = []
    for ext in ONTOLOGY_EXTENSIONS:
        files.extend(glob.glob(os.path.join(directory, ext)))
    return files

def compute_class_hierarchy_metrics(g, classes):
    """
    Compute hierarchy metrics:
      - Maximum and average depth: The longest and average chain length
        found in rdfs:subClassOf relationships.
      - Maximum and average breadth: The maximum and average number of direct subclasses per class.
    """
    memo_depth = {}

    def get_class_depth(cls, seen=None):
        if seen is None:
            seen = set()
        if cls in memo_depth:
            return memo_depth[cls]
        if cls in seen:
            return 0  # Prevent cycles.
        seen.add(cls)
        parent_depths = []
        for parent in g.objects(cls, RDFS.subClassOf):
            if isinstance(parent, URIRef):
                d = get_class_depth(parent, seen)
                parent_depths.append(d)
        seen.remove(cls)
        depth = 1 + max(parent_depths) if parent_depths else 1
        memo_depth[cls] = depth
        return depth

    depths = [get_class_depth(cls) for cls in classes]
    max_depth = max(depths) if depths else 0
    avg_depth = sum(depths) / len(depths) if depths else 0

    breadths = [len(list(g.subjects(RDFS.subClassOf, cls))) for cls in classes]
    max_breadth = max(breadths) if breadths else 0
    avg_breadth = sum(breadths) / len(breadths) if breadths else 0

    return max_depth, avg_depth, max_breadth, avg_breadth

def compute_graph_connectivity(g):
    """
    Build an undirected graph from the ontology triples using networkx (if installed)
    and compute graph connectivity metrics:
      - Average Node Degree: Average number of connections per node.
      - Maximum Node Degree: Highest number of connections for any node.
    These metrics provide insight into the overall interconnectedness of the ontology.
    """
    try:
        import networkx as nx
    except ImportError:
        return None, None
    G = nx.Graph()
    for s, p, o in g:
        G.add_node(s)
        G.add_node(o)
        G.add_edge(s, o)
    if G.number_of_nodes() > 0:
        degrees = dict(G.degree())
        avg_degree = sum(degrees.values()) / G.number_of_nodes()
        max_degree = max(degrees.values())
    else:
        avg_degree = 0
        max_degree = 0
    return avg_degree, max_degree

def check_consistency(file_path):
    """
    Perform a rudimentary logical consistency check using Owlready2 (if available).
    Returns "Consistent" if no issues are detected or an error message otherwise.
    """
    try:
        from owlready2 import get_ontology, sync_reasoner
    except ImportError:
        return "Owlready2 not installed; consistency check skipped"
    try:
        onto = get_ontology(file_path).load()
        with onto:
            sync_reasoner()
        return "Consistent"
    except Exception as e:
        return f"Inconsistent: {e}"

def aggregate_adapted_from(adapted_from_dict):
    """
    Aggregate adaptedFrom IRIs by namespace.
    The namespace is determined as the portion of the URI before the last '/' or '#' character.
    Returns a dictionary mapping namespaces to cumulative counts.
    """
    namespace_counts = defaultdict(int)
    for iri, count in adapted_from_dict.items():
        if '/' in iri:
            ns, sep, _ = iri.rpartition('/')
            ns = ns + sep  # Include the separator in the namespace.
        elif '#' in iri:
            ns, sep, _ = iri.rpartition('#')
            ns = ns + sep
        else:
            ns = iri
        namespace_counts[ns] += count
    return dict(namespace_counts)

def get_ontology_abstract(g):
    """
    Attempt to retrieve the ontology abstract using dcterms:abstract.
    Returns the first abstract found (if any), otherwise returns None.
    """
    for ontology in g.subjects(RDF.type, OWL.Ontology):
        abstract = g.value(ontology, DCTERMS.abstract)
        if abstract:
            return str(abstract)
    return None

def collect_transitive_subclasses(g, superclass, visited=None):
    """
    Recursively collect all transitive subclasses of the given superclass in graph g.
    Returns a set of all subclasses (direct and indirect).
    """
    if visited is None:
        visited = set()
    for sub in g.subjects(RDFS.subClassOf, superclass):
        if sub not in visited:
            visited.add(sub)
            collect_transitive_subclasses(g, sub, visited)
    return visited

def compute_metrics_for_module(file_path, subclass_counter_required, do_reasoning=False):
    """
    Compute metrics for a single ontology module. Metrics include:
      - Counts for classes, properties, rdfs:label, rdfs:comment, and owl:imports.
      - Aggregated adaptedFrom information.
      - Hierarchy metrics (max/avg depth and breadth based on rdfs:subClassOf relationships).
      - Graph connectivity metrics (average and maximum node degree).
      - Optional logical consistency status via Owlready2.
      - The ontology abstract (using dcterms:abstract), if available.
    """
    g = Graph()
    try:
        g.parse(file_path)
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return None

    classes = set(g.subjects(RDF.type, OWL.Class))
    classes.update(set(g.subjects(RDF.type, RDFS.Class)))
    class_count = len(classes)

    properties = set(g.subjects(RDF.type, RDF.Property))
    properties.update(set(g.subjects(RDF.type, OWL.AnnotationProperty)))
    property_count = len(properties)

    adapted_from_metrics = defaultdict(int)
    for _, _, src in g.triples((None, ADAPTED_FROM_IRI, None)):
        adapted_from_metrics[str(src)] += 1

    label_count = len(list(g.triples((None, RDFS.label, None))))
    comment_count = len(list(g.triples((None, RDFS.comment, None))))
    import_count = len(list(g.triples((None, OWL.imports, None))))

    max_depth = avg_depth = max_breadth = avg_breadth = 0
    if classes:
        max_depth, avg_depth, max_breadth, avg_breadth = compute_class_hierarchy_metrics(g, classes)

    avg_degree, max_degree = compute_graph_connectivity(g)
    consistency = None
    if do_reasoning:
        consistency = check_consistency(file_path)

    ontology_abstract = get_ontology_abstract(g)

    metrics = {
        "class_count": class_count,
        "property_count": property_count,
        "label_count": label_count,
        "comment_count": comment_count,
        "import_count": import_count,
        "adapted_from": dict(adapted_from_metrics),
        "max_depth": max_depth,
        "avg_depth": avg_depth,
        "max_breadth": max_breadth,
        "avg_breadth": avg_breadth,
        "avg_degree": avg_degree,
        "max_degree": max_degree,
        "consistency": consistency,
        "ontology_abstract": ontology_abstract,
        "graph": g
    }
    return metrics

def compute_overall_subclass_counts(modules, subclass_iris):
    """
    Compute overall subclass counts for each provided IRI. For each IRI,
    this function traverses the ontology's rdfs:subClassOf hierarchy transitively
    (i.e. counting all subclasses, not just the direct ones).
    The counts are summed over all modules.
    """
    subclass_counts = {iri: 0 for iri in subclass_iris}
    for mod in modules:
        if not mod:
            continue
        g = mod["graph"]
        for iri in subclass_iris:
            iri_ref = URIRef(iri)
            visited = collect_transitive_subclasses(g, iri_ref)
            subclass_counts[iri] += len(visited)
    return subclass_counts

def generate_markdown_report(module_reports, overall_metrics, subclass_counts):
    """
    Generate a detailed Markdown report with natural language introductions for each section.
    Each section includes:
      - Explanations of what was counted and why.
      - For hierarchy metrics, a discussion of depth and breadth of subclass relationships.
      - For graph connectivity, an explanation of average and maximum node degree.
      - The ontology abstract (if available) is also displayed.
    Only aggregated adaptedFrom sources by namespace are displayed.
    """
    md = []
    md.append("# Ontology Modules Metrics Report\n")
    md.append("## Overview\n")
    md.append("This report summarizes the metrics computed across all processed ontology modules. "
              "Below are the definitions for the counts and metrics:\n")
    md.append("- **Total Modules Processed:** Number of ontology files analyzed.\n"
              "- **Total Classes:** Count of ontology concepts (entities typed as owl:Class or rdfs:Class).\n"
              "- **Total Properties:** Count of properties (entities typed as rdf:Property or owl:AnnotationProperty).\n"
              "- **Total Labels:** Count of rdfs:label annotations attached to entities.\n"
              "- **Total Comments:** Count of rdfs:comment annotations attached to entities.\n"
              "- **Total Imports:** Number of owl:imports statements indicating reuse of external ontologies.\n")
    md.append(f"- **Total Modules Processed:** **{len(module_reports)}**")
    md.append(f"- **Total Classes:** **{overall_metrics['total_classes']}**")
    md.append(f"- **Total Properties:** **{overall_metrics['total_properties']}**")
    md.append(f"- **Total Labels:** **{overall_metrics['total_labels']}**")
    md.append(f"- **Total Comments:** **{overall_metrics['total_comments']}**")
    md.append(f"- **Total Imports:** **{overall_metrics['total_imports']}**\n")

    md.append("### AdaptedFrom Sources (Aggregated by Namespace)\n"
              "The adaptedFrom property indicates the provenance or source from which parts of the ontology were adapted. "
              "To provide a concise overview, these sources have been aggregated by their namespace (the common base URI).\n")
    namespace_agg = aggregate_adapted_from(overall_metrics["adapted_from"])
    if namespace_agg:
        for ns, cnt in sorted(namespace_agg.items()):
            md.append(f"- **{ns}**: {cnt}")
    else:
        md.append("- None found")

    md.append("\n### Hierarchy Metrics (Overall)\n"
              "These metrics describe the structure of the ontologies based on subclass relationships:\n"
              "- **Maximum Hierarchy Depth:** The longest chain of subclass relationships from a root to a leaf class.\n"
              "- **Average Hierarchy Depth:** The typical number of levels in the class hierarchy.\n"
              "- **Maximum Hierarchy Breadth:** The highest number of direct subclasses any class has.\n"
              "- **Average Hierarchy Breadth:** The average number of direct subclasses per class.\n")
    md.append(f"- **Maximum Hierarchy Depth:** {overall_metrics['max_depth']}")
    md.append(f"- **Average Hierarchy Depth:** {overall_metrics['avg_depth']:.2f}")
    md.append(f"- **Maximum Hierarchy Breadth:** {overall_metrics['max_breadth']}")
    md.append(f"- **Average Hierarchy Breadth:** {overall_metrics['avg_breadth']:.2f}")

    if overall_metrics['avg_degree'] is not None:
        md.append("\n### Graph Connectivity Metrics (Overall)\n"
                  "These metrics are derived by modeling each ontology as an undirected graph, where nodes represent entities and edges represent relationships. "
                  "- **Average Node Degree:** Reflects the average number of connections per entity, indicating overall interconnectedness.\n"
                  "- **Maximum Node Degree:** The maximum number of connections that any single entity has.\n")
        md.append(f"- **Average Node Degree:** {overall_metrics['avg_degree']:.2f}")
        md.append(f"- **Maximum Node Degree:** {overall_metrics['max_degree']}")

    if subclass_counts:
        md.append("\n### Specified Subclass Counts (Transitive)\n"
                  "For each specified IRI, this metric counts all subclasses (both direct and indirect) in the ontology hierarchy.\n")
        for iri, count in subclass_counts.items():
            md.append(f"- **{iri}**: {count}")

    md.append("\n---\n")

    for module_name, metrics in module_reports:
        md.append(f"## Module: {module_name}\n")
        if metrics.get("ontology_abstract"):
            md.append(f"**Abstract:** {metrics['ontology_abstract']}\n")
        md.append("The following metrics were computed for this ontology module:\n")
        md.append("- **Classes Count:** Number of defined ontology concepts (owl:Class and rdfs:Class).")
        md.append("- **Properties Count:** Number of properties (rdf:Property and owl:AnnotationProperty).")
        md.append("- **Labels Count:** Number of rdfs:label annotations.")
        md.append("- **Comments Count:** Number of rdfs:comment annotations.")
        md.append("- **Imports Count:** Number of owl:imports (external ontology references).\n")
        md.append(f"- **Classes Count:** {metrics['class_count']}")
        md.append(f"- **Properties Count:** {metrics['property_count']}")
        md.append(f"- **Labels Count:** {metrics['label_count']}")
        md.append(f"- **Comments Count:** {metrics['comment_count']}")
        md.append(f"- **Imports Count:** {metrics['import_count']}\n")

        md.append("### Hierarchy Metrics\n"
                  "These metrics describe the subclass structure of the ontology:\n")
        md.append(f"- **Maximum Depth:** {metrics['max_depth']} (Longest chain of subclass relationships)")
        md.append(f"- **Average Depth:** {metrics['avg_depth']:.2f} (Typical number of levels in the hierarchy)")
        md.append(f"- **Maximum Breadth:** {metrics['max_breadth']} (Highest number of direct subclasses)")
        md.append(f"- **Average Breadth:** {metrics['avg_breadth']:.2f} (Average direct subclasses per class)")

        if metrics["avg_degree"] is not None:
            md.append("\n### Graph Connectivity Metrics\n"
                      "These metrics are derived from modeling the ontology as an undirected graph:\n")
            md.append(f"- **Average Node Degree:** {metrics['avg_degree']:.2f} (Average connections per entity)")
            md.append(f"- **Maximum Node Degree:** {metrics['max_degree']} (Highest connections on a single entity)")

        module_namespace_agg = aggregate_adapted_from(metrics["adapted_from"])
        md.append("\n### Aggregated AdaptedFrom Sources (by Namespace)\n"
                  "This section shows the provenance of adapted content, aggregated by the common base URI.\n")
        if module_namespace_agg:
            for ns, cnt in sorted(module_namespace_agg.items()):
                md.append(f"- **{ns}**: {cnt}")
        else:
            md.append("- None found")

        if metrics["consistency"] is not None:
            md.append("\n### Logical Consistency\n"
                      "The ontology was checked for logical consistency using a reasoner.\n")
            md.append(f"- **Status:** {metrics['consistency']}")

        md.append("\n---\n")
    return "\n".join(md)

def main():
    parser = argparse.ArgumentParser(
        description="Generate a detailed and documented metrics report for ontology modules."
    )
    parser.add_argument("--directory", type=str, default=".",
                        help="Directory containing ontology files (default: current directory)")
    parser.add_argument("--subclass-iri", type=str, nargs="*", default=[],
                        help="List of IRIs for which to count subclasses transitively using rdfs:subClassOf")
    parser.add_argument("--reason", action="store_true",
                        help="Enable logical consistency checking using Owlready2 (if installed)")
    parser.add_argument("--output", type=str, default="report.md",
                        help="Output Markdown report filename (default: report.md)")
    args = parser.parse_args()

    ontology_files = gather_file_list(args.directory)
    if not ontology_files:
        print("No ontology files found in the specified directory.")
        return

    module_reports = []
    overall_classes = overall_properties = overall_labels = overall_comments = overall_imports = 0
    overall_adapted_from = defaultdict(int)
    depth_list, breadth_list = [], []
    avg_degs = []
    overall_max_degree = 0
    module_metrics_list = []

    for file_path in ontology_files:
        metrics = compute_metrics_for_module(file_path, bool(args.subclass_iri), do_reasoning=args.reason)
        if not metrics:
            continue
        module_name = os.path.basename(file_path)
        module_reports.append((module_name, metrics))
        overall_classes += metrics["class_count"]
        overall_properties += metrics["property_count"]
        overall_labels += metrics["label_count"]
        overall_comments += metrics["comment_count"]
        overall_imports += metrics["import_count"]
        for src, cnt in metrics["adapted_from"].items():
            overall_adapted_from[src] += cnt
        depth_list.append(metrics["max_depth"])
        breadth_list.append(metrics["max_breadth"])
        if metrics["avg_degree"] is not None:
            avg_degs.append(metrics["avg_degree"])
            overall_max_degree = max(overall_max_degree, metrics["max_degree"])
        module_metrics_list.append(metrics)

    overall_max_depth = max(depth_list) if depth_list else 0
    overall_avg_depth = sum(depth_list) / len(depth_list) if depth_list else 0
    overall_max_breadth = max(breadth_list) if breadth_list else 0
    overall_avg_breadth = sum(breadth_list) / len(breadth_list) if breadth_list else 0
    overall_avg_degree = sum(avg_degs) / len(avg_degs) if avg_degs else None

    overall_metrics = {
        "total_classes": overall_classes,
        "total_properties": overall_properties,
        "total_labels": overall_labels,
        "total_comments": overall_comments,
        "total_imports": overall_imports,
        "adapted_from": dict(overall_adapted_from),
        "max_depth": overall_max_depth,
        "avg_depth": overall_avg_depth,
        "max_breadth": overall_max_breadth,
        "avg_breadth": overall_avg_breadth,
        "avg_degree": overall_avg_degree,
        "max_degree": overall_max_degree
    }
    subclass_counts = {}
    if args.subclass_iri:
        subclass_counts = compute_overall_subclass_counts(module_metrics_list, args.subclass_iri)

    report_md = generate_markdown_report(module_reports, overall_metrics, subclass_counts)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report_md)
    print(f"Report generated and saved to {args.output}")

if __name__ == "__main__":
    main()
