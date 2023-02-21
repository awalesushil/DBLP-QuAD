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

import seaborn as sns
import pandas as pd

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

def compute_data_distribution():
    """
        Compute the distribution of data
    """

    pd.set_option('display.max_columns', None)

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

    data, all_data = {}, {}

    for each in ["train", "valid", "test"]:
        with open(os.path.join("data","DBLP-QuAD",each,"questions.json"), "r") as f:
            data[each] = json.load(f)
            for x in data[each]["questions"]:
                x["question"] = x["question"]["string"]
                x["paraphrased_question"] = x["paraphrased_question"]["string"]
                x["query"] = x["query"]["sparql"]
            all_data["questions"] = all_data.get("questions", []) + data[each]["questions"]
    
    df = pd.DataFrame(all_data["questions"])

    print(df.head())

    df["question_word_count"] = df["question"].apply(lambda x: len(x.split()))
    df["paraphrased_question_word_count"] = df["paraphrased_question"].apply(lambda x: len(x.split()))
    df["query_vocab_count"] = df["query"].apply(lambda x: len(set(x.split())))

    df["question_char_count"] = df["question"].apply(lambda x: len(x))
    df["paraphrased_question_char_count"] = df["paraphrased_question"].apply(lambda x: len(x))
    df["query_char_count"] = df["query"].apply(lambda x: len(x))

    df["edit_distance"] = df.apply(lambda x: edit_distance(x["question"], x["paraphrased_question"]), axis=1)
    df["jaccard_similarity_unigram"] = df.apply(lambda x: jaccard_similarity_ngrams(x["question"], x["paraphrased_question"]), axis=1)
    df["jaccard_similarity_bigram"] = df.apply(lambda x: jaccard_similarity_ngrams(x["question"], x["paraphrased_question"], n=2), axis=1)

    print("-"*100)
    print("\033[1m" + "General statistics of the dataset" + "\033[0m")
    print("-"*100)
    print(df.describe())
    print("-"*100)
    print("\n"*2)


    print("-"*100)
    print("\033[1m" + "Distribution of query types" + "\033[0m")
    print("-"*100)
    print(df["query_type"].value_counts())
    print("-"*100)
    print("\n"*2)

    print("-"*100)
    print("\033[1m" + "Distribution of temporal queries" + "\033[0m")
    print("-"*100)
    print(df["temporal"].value_counts(normalize=True))
    print("-"*100)
    print("\n"*2)

    print("-"*100)
    print("\033[1m" + "Distribution of entities" + "\033[0m")
    print("-"*100)
    _df = df.explode("entities")
    print(_df["entities"].value_counts())
    print("-"*100)
    print("\n"*2)

    print("-"*100)
    print("\033[1m" + "Distribution of relations" + "\033[0m")
    print("-"*100)
    _df = df.explode("relations")
    print(_df["relations"].value_counts())
    print("-"*100)
    print("\n"*2)

    print("-"*100)
    print("\033[1m" + "GENERALIZATION STATS" + "\033[0m")
    print("-"*100)
    print("\n"*2)

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
    
    ax = sns.displot(df, x="edit_distance", kde=True, bins=20)
    ax.set(xlabel="Edit distance", ylabel="Number of question pairs")
    ax.savefig("edit_distance_distribution.png", dpi=300)

    ax = sns.displot(df, x="jaccard_similarity_unigram", kde=True)
    ax.set(xlabel="Jaccard similarity", ylabel="Number of question pairs")
    ax.savefig("jaccard_similarity_unigram_distribution.png", dpi=300)

    ax = sns.displot(df, x="jaccard_similarity_bigram", kde=True)
    ax.set(xlabel="Jaccard similarity", ylabel="Number of question pairs")
    ax.savefig("jaccard_similarity_bigram_distribution.png", dpi=300)