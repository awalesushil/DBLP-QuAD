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

def save_paraphrases_json(filename, generator):
    """
        Save paraphrases to a file
    """
    with open(os.path.join("data", filename), "w", encoding="utf-8") as file:
        file.write('[\n')
        count = 0
        for paraphrases in tqdm(generator, desc="Generating paraphrases "):
            for each in paraphrases:
                count += 1
                json.dump({
                        "id": "P"+str(count).zfill(4),
                        "template_id": each[2],
                        "paraphrases": each[:2]},
                    file, indent=4, ensure_ascii=False)
                file.write(",\n")
        file.seek(file.tell() - 2, 0)
        file.truncate()
        file.write("\n]")

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

def compute_data_distribution():
    """
        Compute the distribution of data
    """

    def edit_distance(s1, s2):
        """
            Compute the edit distance between two strings
        """
        if len(s1) < len(s2):
            return edit_distance(s2, s1)

        # len(s1) >= len(s2)
        if len(s2) == 0:
            return len(s1)

        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def jaccard_similarity_ngrams(s1, s2, n=1):
        """
            Compute the ngram jaccard similarity between two strings
        """
        s1 = s1.lower().split()
        s2 = s2.lower().split()
        a = set(zip(*[s1[i:] for i in range(n)]))
        b = set(zip(*[s2[i:] for i in range(n)]))
        c = a.intersection(b)
        return float(len(c)) / (len(a) + len(b) - len(c))

    data = {}
    all_data = {}

    for each in ["train", "valid", "test"]:
        with open(os.path.join("data",each+"_questions.json"), "r") as f:
            data[each] = json.load(f)
            all_data["questions"] = all_data.get("questions", []) + data[each]["questions"]
    

    WORD_COUNT = 0
    QUERY_VOCAB_COUNT = 0
    MAX_WORD_COUNT = 0
    MAX_QUERY_VOCAB_COUNT = 0
    CHAR_COUNT = 0
    QUERY_CHAR_COUNT = 0
    MAX_CHAR_COUNT = 0
    query_type_count = {}
    query_types = set()
    temporal_count = 0
    entities = []
    relations = []
    held_out = {
        "train": 0,
        "valid": 0,
        "test": 0
    }
    zero_shot = ['TP32', 'TC03', 'TC36', 'TP04', 'TP15']
    zero_shot_count = {
        "valid": 0,
        "test": 0
    }
    compositonal_count = {
        "valid": 0,
        "test": 0
    }
    iid_count = {
        "valid": 0,
        "test": 0
    }
    edit_distances = []
    jaccard_similarities_unigram = []
    jaccard_similarities_bigram = []

    for each in all_data["questions"]:
        WORD_COUNT += len(each['question']['string'].split(" "))
        WORD_COUNT += len(each['paraphrased_question']['string'].split(" "))
        QUERY_VOCAB_COUNT += len(each['query']['sparql'].split(" "))
        
        CHAR_COUNT += len(each['question']['string'])
        CHAR_COUNT += len(each['paraphrased_question']['string'])
        QUERY_CHAR_COUNT += len(each['query']['sparql'])

        MAX_CHAR_COUNT = max(MAX_CHAR_COUNT, len(each['question']['string']))
        MAX_WORD_COUNT = max(MAX_WORD_COUNT, len(each['question']['string'].split(" ")))
        MAX_WORD_COUNT = max(MAX_WORD_COUNT, len(each['paraphrased_question']['string'].split(" ")))
        MAX_QUERY_VOCAB_COUNT = max(MAX_QUERY_VOCAB_COUNT, len(each['query']['sparql'].split(" ")))

        entities.extend(each["entities"])
        relations.extend(each["relations"])
        query_type = each["query_type"]
        query_types.add(query_type)
        query_type_count.setdefault(query_type, 0)
        query_type_count[query_type] += 1
        edit_distances.append(
            edit_distance(
                each["question"]['string'],
                each["paraphrased_question"]['string']))
        jaccard_similarities_unigram.append(
            jaccard_similarity_ngrams(
                each["question"]['string'],
                each["paraphrased_question"]['string']))
        jaccard_similarities_bigram.append(
            jaccard_similarity_ngrams(
                each["question"]['string'],
                each["paraphrased_question"]['string'],
                n=2))
        if each['temporal']:
            temporal_count += 1
        
    
    for group in ["valid", "test"]:
        for each in data[group]["questions"]:
            if each['held_out']:
                held_out[group] += 1
                if each['template_id'] in zero_shot:
                    zero_shot_count[group] += 1
                else:
                    compositonal_count[group] += 1
            else:
                iid_count[group] += 1


    # Average
    print("Average word count: ", WORD_COUNT / (2 * N))
    print("Average query vocab count: ", QUERY_VOCAB_COUNT / N)

    # Max
    print("Max word count: ", MAX_WORD_COUNT)
    print("Max query vocab count: ", MAX_QUERY_VOCAB_COUNT)
    print("Max char count: ", MAX_CHAR_COUNT)

    # Average
    print("Average char count: ", CHAR_COUNT / (2 * N))
    print("Average query char count: ", QUERY_CHAR_COUNT / N)
    
    print("Total number of questions:", len(all_data["questions"]))
    print("Total number of temporal questions:", temporal_count)
    print("Total number of entities:", len(set(entities)))
    print("Total number of relations:", len(set(relations)))
    print("Total number of query types:", len(query_types))
    print("Distribution of query types:")
    for each in query_types:
        print(each, query_type_count[each])
    
    print("Percent of held out questions:")
    for each in held_out:
        print(each, held_out[each]/len(data[each]["questions"]))
    
    print("Percent of zero-shot questions:")
    for each in zero_shot_count:
        print(each, zero_shot_count[each]/len(data[each]["questions"]))
    
    print("Percent of compositional questions:")
    for each in compositonal_count:
        print(each, compositonal_count[each]/len(data[each]["questions"]))
    
    print("Percent of iid questions:")
    for each in iid_count:
        print(each, iid_count[each]/len(data[each]["questions"]))
    
    print("Average edit distance:", np.mean(edit_distances))
    print("Standard deviation of edit distance:", np.std(edit_distances))

    print("Average Jaccard similarity unigram:", np.mean(jaccard_similarities_unigram))
    print("Standard deviation of Jaccard similarity unigram:", np.std(jaccard_similarities_unigram))

    print("Average Jaccard similarity bigram:", np.mean(jaccard_similarities_bigram))
    print("Standard deviation of Jaccard similarity bigram:", np.std(jaccard_similarities_bigram))