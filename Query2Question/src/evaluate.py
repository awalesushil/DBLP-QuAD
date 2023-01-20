import re
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
        return {}


def clean_query(query):
    """
        Clean the query
    """
    group = re.compile(r"(https:\S+)")
    query = group.sub(r"<\1>", query)
    query = query.replace(" < s> ", "")
    query = query.replace('"', "")
    query = query.replace("( ", "(")
    query = query.replace(" )", ")")
    query = query.replace("  ", " ")
    return query 

def run_queries():
    """
        Run generated queries
    """

    TOTAL_QUERIES = 0

    dblp_server = DBLPServer("../../config.json")

    with open("../data/predicted_answers.json", "w+", encoding="utf-8") as pred_file:
        with open("../data/actual_answers.json", "w+", encoding="utf-8") as act_file:
            pred_file.write('{\n"answers":[')
            act_file.write('{\n"answers":[')
            with open("outputs/predictions.csv", "r", encoding="utf-8") as f:
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
                    # if TOTAL_QUERIES == 250:
                    #     break
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
                elif ["firstanswer", "secondanswer"] in answer["head"]["vars"]:
                    return [
                            (binding["firstanswer"]["value"], binding["secondanswer"]["value"])
                            for binding in answer["results"]["bindings"]
                        ]
                elif "count" in answer["head"]["vars"]:
                    return [binding["count"]["value"] for binding in answer["results"]["bindings"]]
    return None

def calculate_accuracy(total_queries):

    accuracy = 0
    with open("outputs/predictions.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            generated_query = clean_query(row[1])
            actual_query = clean_query(row[2])
            generated_query = generated_query.replace(" ", "")
            actual_query = actual_query.replace(" ", "")
            if generated_query == actual_query:
                accuracy += 1
    print("Accuracy: ", accuracy / total_queries)

def calculate_f1(total_queries):
    """
        Calculate precision and recall at rank 1
    """

    accuracy = 0
    precision = {"1": 0, "5": 0, "10": 0}
    recall = {"1": 0, "5": 0, "10": 0}
    
    with open("../data/predicted_answers.json", "r", encoding="utf-8") as pred_file:
        with open("../data/actual_answers.json", "r", encoding="utf-8") as act_file:
            pred_answers = json.load(pred_file)["answers"]
            act_answers = json.load(act_file)["answers"]
            
            for pred_answer, act_answer in zip(pred_answers, act_answers):
                
                pred_answer = get_answer(pred_answer)
                act_answer = get_answer(act_answer)
                
                if not pred_answer or not act_answer:
                    continue
                
                # Calculate accuracy
                if pred_answer == act_answer:
                    accuracy += 1

                relevant_and_retrieved_1 = set(pred_answer[:1]).intersection(set(act_answer[:1]))
                relevant_and_retrieved_5 = set(pred_answer[:6]).intersection(set(act_answer[:6]))
                relevant_and_retrieved_10 = set(pred_answer[:11]).intersection(set(act_answer[:11]))
                
                # Calculate precision at rank 1, 5 and 10
                precision["1"] += len(relevant_and_retrieved_1) / len(pred_answer[:1])
                precision["5"] += len(relevant_and_retrieved_5) / len(pred_answer[:6])
                precision["10"] += len(relevant_and_retrieved_10) / len(pred_answer[:11])
    
                # Calculate recall at rank 1, 5 and 10
                recall["1"] += len(relevant_and_retrieved_1) / len(act_answer[:1])
                recall["5"] += len(relevant_and_retrieved_5) / len(act_answer[:6])
                recall["10"] += len(relevant_and_retrieved_10) / len(act_answer[:11])

    print("Total queries: ", total_queries)
    print("Accuracy: ", accuracy / total_queries)
    
    precision["1"] = precision["1"] / total_queries
    print("Precision at rank 1: ", precision["1"])
    
    precision["5"] = precision["5"] / total_queries
    print("Precision at rank 5: ", precision["5"])
    
    precision["10"] = precision["10"] / total_queries
    print("Precision at rank 10: ", precision["10"])
    
    recall["1"] = recall["1"] / total_queries
    print("Recall at rank 1: ", recall["1"])

    recall["5"] = recall["5"] / total_queries
    print("Recall at rank 5: ", recall["5"])

    recall["10"] = recall["10"] / total_queries
    print("Recall at rank 10: ", recall["10"])

    # Calculate F1 score
    for k in precision.keys():
        print("F1 score at {}:".format(k), round(2 * ((precision[k] * recall[k]) / (precision[k] + recall[k])), 3))


if __name__ == "__main__":
    TOTAL_QUERIES = run_queries()
    calculate_accuracy(TOTAL_QUERIES)
    calculate_f1(TOTAL_QUERIES)
                



