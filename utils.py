"""
    Helper functions
"""
import re
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

def add_to_json(file, id, doc):
    """
        Add a document to a json file
    """
    _doc = {"id": id, **doc}
    json.dump(_doc, file, indent=4, ensure_ascii=False)
    file.write(",\n")


def save_to_json(data_file, answers_file, failed_queries_file, dataGenerator):
    """
        Save data to a json file
    """
    with open(os.path.join("data", data_file), "w", encoding="utf-8") as data_file:
        with open(os.path.join("data", failed_queries_file), "w", encoding="utf-8") as failed_queries_file:
            with open(os.path.join("data", answers_file), "w", encoding="utf-8") as answers_file:
                data_file.write('{\n"questions": [')
                answers_file.write('{\n"answers": [')
                failed_queries_file.write('{\n"failed_queries": [')
                for id, data, answer in tqdm(dataGenerator, desc="Generating data: "):
                    if (
                        answer["answer"] and 
                        not re.search("NONE", data["question"]["string"]) and 
                        not re.search("NONE", data["paraphrased_question"]["string"])
                    ):
                        add_to_json(data_file, id, data)
                        add_to_json(answers_file, id, answer)
                    else:
                        add_to_json(failed_queries_file, id, data)
                data_file.seek(data_file.tell() - 2, 0)
                data_file.truncate()
                data_file.write("\n]}")

                answers_file.seek(answers_file.tell() - 2, 0)
                answers_file.truncate()
                answers_file.write("\n]}")

                failed_queries_file.seek(failed_queries_file.tell() - 2, 0)
                failed_queries_file.truncate()
                failed_queries_file.write("\n]}")


def plot_template_distribution():
    """
        Plot template distribution
    """
    for entity in ["CREATOR", "PUBLICATION"]:
        print(f"Stats for Entity: {entity}")
        
        query_types = templates[entity].keys()
        total_templates = [len(templates[entity][each]) for each in query_types]

        print("Total number of templates:", sum(total_templates))
        
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
    data_file = ["data.json", "failed_queries.json"]

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

