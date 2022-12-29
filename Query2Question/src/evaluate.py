import json
import requests
import urllib.parse
import csv


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
        return []



def run_queries():
    """
        Run generated queries
    """
    dblp_server = DBLPServer("config.json")

    with open("data/predicted_answers.json", "w+", encoding="utf-8") as pred_file:
        with open("data/actual_answers.json", "w+", encoding="utf-8") as act_file:
            with open("data/predictions.csv", "r", encoding="utf-8") as f:
                reader = csv.reader(f)
                for row in reader:
                    pred_answer = dblp_server.query(row[0])
                    pred_answer = json.dumps(pred_answer, ensure_ascii=False)
                    act_answer = dblp_server.query(row[1])
                    act_answer = json.dumps(act_answer, ensure_ascii=False)

def get_answer(answer):
    """
        Get the answer from the result
    """
    if answer:
        if "boolean" in answer.keys():
            return [answer["boolean"]]
        elif "results" in answer.keys():
            if answer["results"]["bindings"]:
                
    return None

def evaluate():
    """
        Calculate precision and recall at rank 1
    """

    precision = {"1": 0, "5": 0, "10": 0}
    recall = {"1": 0, "5": 0, "10": 0}
    
    with open("data/predicted_answers.json", "r", encoding="utf-8") as pred_file:
        with open("data/actual_answers.json", "r", encoding="utf-8") as act_file:
            pred_answers = json.load(pred_file)
            act_answers = json.load(act_file)
            
            for pred_answer, act_answer in zip(pred_answers, act_answers):
                
                pred_answer = get_answer(pred_answer)
                act_answer = get_answer(act_answer)
                
                if not pred_answer or not act_answer:
                    continue

                # Calculate precision at rank 1, 5 and 10
                precision["1"] += 1 if pred_answer[0] == act_answer[0] else 0
                precision["5"] += len(set(pred_answer[1:6]).intersection(set(act_answer[1:6]))) / 5
                precision["10"] += len(set(pred_answer[1:11]).intersection(set(act_answer[1:11]))) / 10
    
                # Calculate recall at rank 1, 5 and 10
                recall["1"] += 1 if pred_answer[0] == act_answer[0] else 0
                recall["5"] += len(set(pred_answer[1:6]).intersection(set(act_answer[1:6]))) / len(act_answer)
                recall["10"] += len(set(pred_answer[1:11]).intersection(set(act_answer[1:11]))) / len(act_answer)
            
    
    print("Precision at rank 1: ", precision["1"] / len(pred_answers))
    print("Precision at rank 5: ", precision["5"] / len(pred_answers))
    print("Precision at rank 10: ", precision["10"] / len(pred_answers))
    print("Recall at rank 1: ", recall["1"] / len(pred_answers))
    print("Recall at rank 5: ", recall["5"] / len(pred_answers))
    print("Recall at rank 10: ", recall["10"] / len(pred_answers))

    # Calculate F1 score
    f1_score = {}
    for k in precision.keys():
        f1_score[k] = 2 * (precision[k] * recall[k]) / (precision[k] + recall[k])
    print("F1 score at rank 1: ", f1_score["1"])
    print("F1 score at rank 5: ", f1_score["5"])
    print("F1 score at rank 10: ", f1_score["10"])



                



