"""
    Helper functions
"""
import os
import json
import logging
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

from templates import templates
from dblp import Graph

logging.basicConfig(level=logging.INFO)

def index_graph(path):
    """
        Index graph from path
    """
    g = Graph("DBLP")
    g.load_from_ntriple(path)
    g.save(os.join.path("dblp.pkl"))

def load_graph():
    """
        Load graph from pickle file
    """
    graph = Graph("DBLP")
    logging.info(" Loading DBLP graph...")
    graph.load_from_pickle("dblp.pkl")
    logging.info(" DBLP graph loaded")
    return graph

def add_to_json(file, doc):
    """
        Add a document to a json file
    """
    json.dump(doc, file, indent=4)
    file.write(",\n")


def save_to_json(data_file, failed_queries_file, dataGenerator):
    """
        Save data to a json file
    """
    with open(os.path.join("data", data_file), "w", encoding="utf-8") as f1:
        with open(os.path.join("data", failed_queries_file), "w", encoding="utf-8") as f2:
            json.dump("[", f1)
            json.dump("[", f2)
            for question, paraphrase, query, entity, query_type, answers in tqdm(dataGenerator, desc="Generating data: "):
                
                if answers:
                    add_to_json(f1, {
                        "question": question,
                        "paraphrase": paraphrase,
                        "query": query,
                        "entity": entity,
                        "query_type": query_type,
                        "answers": answers
                    })
                else:
                    add_to_json(f2, {
                        "question": question,
                        "paraphrase": paraphrase,
                        "query": query,
                        "entity": entity,
                        "query_type": query_type,
                        "answers": answers
                    })
            json.dump("]", f1)
            json.dump("]", f2)


def plot_template_distribution():
    """
        Plot template distribution
    """
    for entity in ["CREATOR", "PUBLICATION"]:
        print(f"Stats for Entity: {entity}")
        
        query_types = templates[entity].keys()
        total_templates = [len(templates[entity][each]) for each in query_types]
        weights = [len(templates[entity][each])/sum(total_templates) for each in query_types]

        print("Total number of templates:", sum(total_templates))
        print("Number of templates per query type:")
        for i, query_type in enumerate(query_types):
            print(f"{query_type}: {len(templates[entity][query_type])} ({weights[i]*100:.2f}%)")
        
        X_axis = np.arange(len(query_types))
        width = 0.4
        if entity == "CREATOR":
            creator = plt.bar(X_axis - 0.2, total_templates, width, label=entity)
        else:
            publication = plt.bar(X_axis + 0.2, total_templates, width, label=entity)

    plt.bar_label(creator, padding=3)
    plt.bar_label(publication, padding=3)
    plt.xticks(X_axis, query_types)
    plt.xlabel("Query Type")
    plt.ylabel("Number of templates")
    plt.title(f"Number of templates per query type")
    plt.legend()
    plt.show()


def plot_question_distributions():
    """
        Plot the distribution of questions generated and queries failed
    """
    data_file = ["train.json", "failed.json"]

    for file in data_file:
        
        with open(os.path.join("data",file), "r") as f:
            data = json.load(f)

        query_type_count = {}
        query_types = set()

        for each in data:
            entity = each["entity"]
            query_type = each["query_type"]
            query_types.add(query_type)
            query_type_count.setdefault(entity, {})
            query_type_count[entity].setdefault(query_type, 0)
            query_type_count[entity][query_type] += 1


        X_axis = np.arange(len(query_types))
        width = 0.4
        total_templates = [query_type_count['CREATOR'].get(each, 0) for each in query_types]
        creator = plt.bar(X_axis - 0.2, total_templates, width, label="CREATOR")

        total_templates = [query_type_count['PUBLICATION'].get(each, 0) for each in query_types]
        publication = plt.bar(X_axis + 0.2, total_templates, width, label="PUBLICATION")

        plt.bar_label(creator, padding=3)
        plt.bar_label(publication, padding=3)
        plt.xticks(X_axis, query_types)
        plt.xlabel("Query Type")
        plt.ylabel("Number of question-query")
        plt.title(f"Number of question-query pairs per query type for {file}")
        plt.legend()
        plt.show()

