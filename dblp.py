"""
    Modeling DBLP RDF data as Graph
"""

import re
import random
import pickle
from tqdm import tqdm
import whitelist

class Graph:
    """
        Graph data model
    """
    def __init__(self, label=None):
        self.label = label
        self.data = {}

    def __repr__(self):
        return f"Graph(label={self.label})"

    def add_triple(self, _type, vertex1, edge, vertex2):
        """
            Add a triple into the graph
        """
        self.data.setdefault(_type, {})

        # Get vertex1 if exists else add with empty dict
        self.data[_type].setdefault(vertex1, {})

        # add edge if exists else add epmty list
        self.data[_type][vertex1].setdefault(edge, [])

        # add vertex2
        self.data[_type][vertex1][edge].append(vertex2)

    def get(self, _type, vertex):
        """
            Return edges and connections for the given vertex
        """
        # Query from both publication and creator types
        other_type = "Publication" if _type != "Publication" else "Creator"
        try:
            try:
                return self.data[_type][vertex]
            except KeyError:
                return self.data[other_type][vertex]
        except KeyError:
            return None

    def sample_vertex(self, _type, count=1):
        """
            Sample a n subgraphs from Graph without replacement
        """
        def generate_subgraph(vertex):
            subgraph = {vertex: self.get(_type, vertex)}
            for edge in subgraph[vertex].keys(): # Iterate over edges
                for i, label in enumerate(subgraph[vertex][edge]):
                    vertex2 = self.get(_type, label)
                    if vertex2:
                        subgraph[vertex][edge][i] = {label: vertex2}
            return subgraph

        vertices = random.sample(self.data[_type].keys(), count)
        return generate_subgraph(vertices[0]) if count == 1 else [
                generate_subgraph(vertex) for vertex in vertices
            ]

    def sample_triples(self, _type, hops=2):
        """
            Sample a triple from Graph with n hops
        """

        def filter_edges(edges):
            return [e for e in edges if e in whitelist.nonleaf_predicates]

        for hop in range(hops):

            if hop == 0:
                triple_sequence = []
                subgraph = self.sample_vertex(_type)
            else:
                vertex = triple_sequence[-1][-1]
                subgraph = {vertex: self.get(_type, vertex)}
                if subgraph[vertex] is None: # If vertex2 is None return
                    return triple_sequence

            vertex1 = next(iter(subgraph)) # Get vertex name
            edges = subgraph[vertex1].keys() # Get all edges
            filtered_edges = edges if hop==hops-1 else filter_edges(edges) # Filter edges

            if not filtered_edges:
                if hop==0:
                    edge = random.sample(edges, 1)[0]
                    vertex2 = random.sample(subgraph[vertex1][edge], 1)[0]
                    triple_sequence.append([vertex1, edge, vertex2])
                return triple_sequence

            edge = random.sample(filtered_edges, 1)[0] # Sample an edge for vertex1
            vertex2 = random.sample(subgraph[vertex1][edge], 1)[0] # Sample a vertex2 for an edge
            triple_sequence.append([vertex1, edge, vertex2])

        return triple_sequence

    def load_from_ntriple(self, path):
        """
            Load triples into the graph from NTriple file
        """

        type_predicate = "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>"

        def parse(line):
            parts = line.split(" ")
            vertex1, edge = parts[0], parts[1]
            vertex2 = " ".join(parts[2:-1]) # Remove last "."
            return vertex1, edge, vertex2

        def classify_type(vertex):
            type_string = re.sub(">", "", vertex.rsplit("#", maxsplit=1)[-1])
            if type_string in whitelist.publications:
                return "Publication"
            if type_string in whitelist.creators:
                return "Creator"
            return None

        with open(path, encoding="utf-8") as infile:

            for triple in tqdm(infile, desc="Loading"):

                if len(triple.split(" ")) > 1:

                    vertex1, edge, vertex2 = parse(triple)

                    if vertex1.startswith("_"): # Ignore IDs and Lists
                        continue

                    if edge == type_predicate:

                        extracted_type = classify_type(vertex2)

                        if extracted_type == "Creator": # Don't store Creator sub-classes
                            _type = "Creator"
                            continue

                        # Ignore other types but save prior type string
                        _type = extracted_type if extracted_type else _type

                    if edge in whitelist.predicates:
                        self.add_triple(_type, vertex1, edge, vertex2)


    def load_from_pickle(self, file):
        """
            Load graph from pickle file
        """
        with open(file, "rb") as loadfile:
            self.data = pickle.load(loadfile)
            print("Graph loaded from ", file)

    def save(self, file):
        """
            save data to a pickle file
        """
        with open(file,"wb") as savefile:
            pickle.dump(self.data, savefile)
            print("Graph saved to ", file)
