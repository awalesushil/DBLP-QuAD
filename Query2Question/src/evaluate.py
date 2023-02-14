import re
import json
import requests
import urllib.parse
import csv

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from numpy import NaN

class DBLPServer:
    """
        DBLP Server class
    """
    def __init__(self, path):
        with open(path, "r", encoding="utf-8") as f:
            self.host = json.load(f)["host"]
        self.result_format = "json"
    
    def query(self, query):
        """
            Query the DBLP server
        """
        url = f"{self.host}/sparql?query={urllib.parse.quote(query)}&format=application%2Fsparql-results%2B{self.result_format}"
        response = requests.get(url)
        if response.status_code == 200:
            result = json.loads(response.text)

            if "boolean" in result.keys():
                return result
            elif "results" in result.keys():
                if result["results"]["bindings"]:
                    return result
        return {}


def clean_query(query):
    """
        Clean the query
    """
    group = re.compile(r"(https:\S+)")
    query = group.sub(r"<\1>", query)
    group = re.compile(r"(http:\S+)")
    query = group.sub(r"<\1>", query)
    query = query.replace(",>", ">,")
    query = query.replace(" < s> ", "")
    query = query.replace('"', "")
    query = query.replace("( ", "(")
    query = query.replace(" )", ")")
    query = query.replace("  ", " ")
    return query 

def run_queries(model):
    """
        Run generated queries
    """

    TOTAL_QUERIES = 0

    dblp_server = DBLPServer("../../config.json")

    with open("../"+model+"-data/predicted_answers.json", "w+", encoding="utf-8") as pred_file:
        with open("../"+model+"-data/actual_answers.json", "w+", encoding="utf-8") as act_file:
            pred_file.write('{\n"answers":[')
            act_file.write('{\n"answers":[')
            with open(model+"-outputs/predictions.csv", "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    TOTAL_QUERIES += 1
                    generated_query = clean_query(row[1])
                    actual_query = clean_query(row[2])
                    pred_answer = dblp_server.query(generated_query)
                    pred_answer['id'] = row[0]       
                    json.dump(pred_answer, pred_file, indent=4, ensure_ascii=False)
                    pred_file.write(",\n")
                    act_answer = dblp_server.query(actual_query)
                    act_answer['id'] = row[0]
                    json.dump(act_answer, act_file, indent=4, ensure_ascii=False)
                    act_file.write(",\n")
            pred_file.seek(pred_file.tell() - 2, 0)
            pred_file.truncate()
            pred_file.write("]}")
            act_file.seek(act_file.tell() - 2, 0)
            act_file.truncate()
            act_file.write("]}")

    return TOTAL_QUERIES

def get_answer(answer):
    """
        Get the answer from the result
    """
    if answer:
        if "boolean" in answer.keys():
            return [answer["boolean"]]
        elif "results" in answer.keys():
            if answer["results"]["bindings"] and answer["results"]["bindings"] != [{}]:
                if "answer" in answer["head"]["vars"]:
                    return [binding["answer"]["value"] for binding in answer["results"]["bindings"]]
                elif "firstanswer" in answer["head"]["vars"] and "secondanswer" in answer["head"]["vars"]:
                    return [
                            (binding.get("firstanswer", {}).get("value", None),
                            binding.get("secondanswer", {}).get("value", None))
                            for binding in answer["results"]["bindings"]
                        ]
                elif "count" in answer["head"]["vars"]:
                    return [binding["count"]["value"] for binding in answer["results"]["bindings"]]
    return None

def calculate_accuracy(model, total_queries):

    accuracy = 0
    with open(model+"-outputs/predictions.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            generated_query = clean_query(row[1])
            actual_query = clean_query(row[2])
            generated_query = generated_query.replace(" ", "")
            actual_query = actual_query.replace(" ", "")
            if generated_query == actual_query:
                accuracy += 1
    print("Exact-match Accuracy: ", accuracy / total_queries)

def calculate_f1(model):
    """
        Calculate F1 score
    """

    categories = [
            "SINGLE_FACT","MULTI_FACT","DOUBLE_INTENT",
            "BOOLEAN","NEGATION","DOUBLE_NEGATION",
            "UNION","DISAMBIGUATION",
            "COUNT","SUPERLATIVE+COMPARATIVE",
            "TEMPORAL", "NON_TEMPORAL",
            "IID", "ZERO-SHOT", "COMPOSITIONAL",
            "ALL"
        ]

    zero_shot_ids = ['TP32', 'TC03', 'TC36', 'TP04', 'TP15']
    precision = {category: 0 for category in categories}
    recall = {category: 0 for category in categories}
    count = {category: 0 for category in categories}

    precision_category_generalization = {
        category: {level: 0 for level in ["IID", "ZERO-SHOT", "COMPOSITIONAL"]}
            for category in categories}
    recall_category_generalization = {category: 
        {level: 0 for level in ["IID", "ZERO-SHOT", "COMPOSITIONAL"]}
            for category in categories}
    count_category_generalization = {category:
        {level: 0 for level in ["IID", "ZERO-SHOT", "COMPOSITIONAL"]}
            for category in categories}
    f1_category_generalization = {category:
        {level: 0 for level in ["IID", "ZERO-SHOT", "COMPOSITIONAL"]}
            for category in categories}

    with open("../../data/test_questions.json", "r", encoding="utf-8") as f:
        test_questions = json.load(f)["questions"]

    
    with open(model+"-outputs/correct.csv", "a+", encoding="utf-8") as cf:
        with open(model+"-outputs/errors.csv", "a+", encoding="utf-8") as ef:
            with open("../"+model+"-data/predicted_answers.json", "r", encoding="utf-8") as pred_file:
                with open("../"+model+"-data/actual_answers.json", "r", encoding="utf-8") as act_file:
                    pred_answers = json.load(pred_file)["answers"]
                    act_answers = json.load(act_file)["answers"]
                    
                    for pred_answer, act_answer in zip(pred_answers, act_answers):
                        
                        id = int(pred_answer["id"])
                        metadata = test_questions[id]
                        template_id = metadata["template_id"]
                        category = metadata["query_type"]
                        temporal = metadata["temporal"]
                        held_out = metadata["held_out"]

                        pred_answer = get_answer(pred_answer)
                        act_answer = get_answer(act_answer)

                        count[category] += 1
                        count["ALL"] += 1
                        if temporal:
                            count["TEMPORAL"] += 1
                        else:
                            count["NON_TEMPORAL"] += 1
                        
                        if held_out:
                            if template_id in zero_shot_ids:
                                count["ZERO-SHOT"] += 1
                                count_category_generalization[category]["ZERO-SHOT"] += 1
                            else:
                                count["COMPOSITIONAL"] += 1
                                count_category_generalization[category]["COMPOSITIONAL"] += 1
                        else:
                            count["IID"] += 1
                            count_category_generalization[category]["IID"] += 1

                        if not pred_answer or not act_answer:
                            ef.write(str(id)+"\n")
                            continue

                        if pred_answer != act_answer:
                            ef.write(str(id)+"\n")
                        else:
                            cf.write(str(id)+"\n")
                    
                        relevant_and_retrieved = set(pred_answer).intersection(set(act_answer))
                        precision[category] += len(relevant_and_retrieved) / len(pred_answer)
                        recall[category] += len(relevant_and_retrieved) / len(act_answer)

                        if temporal:
                            precision["TEMPORAL"] += len(relevant_and_retrieved) / len(pred_answer)
                            recall["TEMPORAL"] += len(relevant_and_retrieved) / len(act_answer)
                        else:
                            precision["NON_TEMPORAL"] += len(relevant_and_retrieved) / len(pred_answer)
                            recall["NON_TEMPORAL"] += len(relevant_and_retrieved) / len(act_answer)
                        
                        if held_out:
                            if template_id in zero_shot_ids:
                                precision["ZERO-SHOT"] += len(relevant_and_retrieved) / len(pred_answer)
                                recall["ZERO-SHOT"] += len(relevant_and_retrieved) / len(act_answer)
                                precision_category_generalization[category]["ZERO-SHOT"] += len(relevant_and_retrieved) / len(pred_answer)
                                recall_category_generalization[category]["ZERO-SHOT"] += len(relevant_and_retrieved) / len(act_answer)
                            else:
                                precision["COMPOSITIONAL"] += len(relevant_and_retrieved) / len(pred_answer)
                                recall["COMPOSITIONAL"] += len(relevant_and_retrieved) / len(act_answer)
                                precision_category_generalization[category]["COMPOSITIONAL"] += len(relevant_and_retrieved) / len(pred_answer)
                                recall_category_generalization[category]["COMPOSITIONAL"] += len(relevant_and_retrieved) / len(act_answer)
                        else:
                            precision["IID"] += len(relevant_and_retrieved) / len(pred_answer)
                            recall["IID"] += len(relevant_and_retrieved) / len(act_answer)
                            precision_category_generalization[category]["IID"] += len(relevant_and_retrieved) / len(pred_answer)
                            recall_category_generalization[category]["IID"] += len(relevant_and_retrieved) / len(act_answer)

                        precision["ALL"] += len(relevant_and_retrieved) / len(pred_answer)
                        recall["ALL"] += len(relevant_and_retrieved) / len(act_answer)

    print("Category", " " * 17, "F1 IID", " " * 4, "Count", " " * 3, "F1 Zero-Shot", " " * 2, "Count", " " * 2, "F1 Compositional", " " * 2, "Count", " " * 2, "F1", " " * 8, "Count")
    print("-" * 50)
    for category in categories:
        
        if count_category_generalization[category]["IID"] == 0:
            f1_IID = NaN
        else:
            precision_category_generalization[category]["IID"] = precision_category_generalization[category]["IID"] / count_category_generalization[category]["IID"]
            recall_category_generalization[category]["IID"] = recall_category_generalization[category]["IID"] / count_category_generalization[category]["IID"]
            if precision_category_generalization[category]["IID"] == 0 or recall_category_generalization[category]["IID"] == 0:
                f1_IID = 0
            else:
                f1_IID = round(2 * ((precision_category_generalization[category]["IID"] * recall_category_generalization[category]["IID"]) / (precision_category_generalization[category]["IID"] + recall_category_generalization[category]["IID"])), 3)
            
        if count_category_generalization[category]["ZERO-SHOT"] == 0:
            f1_zero_shot = NaN
        else:
            precision_category_generalization[category]["ZERO-SHOT"] = precision_category_generalization[category]["ZERO-SHOT"] / count_category_generalization[category]["ZERO-SHOT"]
            recall_category_generalization[category]["ZERO-SHOT"] = recall_category_generalization[category]["ZERO-SHOT"] / count_category_generalization[category]["ZERO-SHOT"]
            if precision_category_generalization[category]["ZERO-SHOT"] == 0 or recall_category_generalization[category]["ZERO-SHOT"] == 0:
                f1_zero_shot = 0
            else:
                f1_zero_shot = round(2 * ((precision_category_generalization[category]["ZERO-SHOT"] * recall_category_generalization[category]["ZERO-SHOT"]) / (precision_category_generalization[category]["ZERO-SHOT"] + recall_category_generalization[category]["ZERO-SHOT"])), 3)
            
        if count_category_generalization[category]["COMPOSITIONAL"] == 0:
            f1_COMPOSITIONAL = NaN
        else:
            precision_category_generalization[category]["COMPOSITIONAL"] = precision_category_generalization[category]["COMPOSITIONAL"] / count_category_generalization[category]["COMPOSITIONAL"]
            recall_category_generalization[category]["COMPOSITIONAL"] = recall_category_generalization[category]["COMPOSITIONAL"] / count_category_generalization[category]["COMPOSITIONAL"]
            if precision_category_generalization[category]["COMPOSITIONAL"] == 0 or recall_category_generalization[category]["COMPOSITIONAL"] == 0:
                f1_COMPOSITIONAL = 0
            else:
                f1_COMPOSITIONAL = round(2 * ((precision_category_generalization[category]["COMPOSITIONAL"] * recall_category_generalization[category]["COMPOSITIONAL"]) / (precision_category_generalization[category]["COMPOSITIONAL"] + recall_category_generalization[category]["COMPOSITIONAL"])), 3)
        
        f1_category_generalization[category]["IID"] = f1_IID
        f1_category_generalization[category]["ZERO-SHOT"] = f1_zero_shot
        f1_category_generalization[category]["COMPOSITIONAL"] = f1_COMPOSITIONAL

        precision[category] = precision[category] / count[category]
        recall[category] = recall[category] / count[category]
        f1 = round(2 * ((precision[category] * recall[category]) / (precision[category] + recall[category])), 3)

        print(category, " " * (25 - len(category)), f1_IID, " " * (10 - len(str(f1_IID))), count["IID"], " " * 4, f1_zero_shot, " " * (14 - len(str(f1_zero_shot))), count["ZERO-SHOT"], " " * 5, f1_COMPOSITIONAL, " " * (18 - len(str(f1_COMPOSITIONAL))), count["COMPOSITIONAL"], " " * 4, f1, " " * (10 - len(str(f1))), count[category])

    # Plot heatmap
    f1_category_generalization.pop("ALL")
    f1_category_generalization.pop("IID")
    f1_category_generalization.pop("ZERO-SHOT")
    f1_category_generalization.pop("COMPOSITIONAL")
    f1_category_generalization.pop("NON_TEMPORAL")
    f1_category_generalization.pop("TEMPORAL")

    df = pd.DataFrame.from_dict(f1_category_generalization, orient='index')
    ax = sns.heatmap(df, annot=True, cmap="YlGnBu", linewidths=.1)
    ax.set(xlabel="Level of Generalization", ylabel="Query Type")
    ax = ax.get_figure()
    ax.savefig("f1_scores_category_generalization_" + model + ".png", dpi=300, bbox_inches='tight', pad_inches=0.1)
    ax = ax.clf()
    # plt.show()

if __name__ == "__main__":

    for model in ["t5-small", "t5-base"]:
        print("\n Model: ", model)
        # TOTAL_QUERIES = run_queries(model)
        TOTAL_QUERIES = 2000
        calculate_accuracy(model, TOTAL_QUERIES)
        calculate_f1(model)
                



