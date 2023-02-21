import re
import csv
import json

from evaluate import clean_query

error_query_ids = {
    "t5-small": [],
    "t5-base": []
}

correct_query_ids = {
    "t5-small": [],
    "t5-base": []
}

error_query = {
    "t5-small": [],
    "t5-base": []
}

correct_query = {
    "t5-small": [],
    "t5-base": []
}

with open("../../data/test_questions.json", "r", encoding="utf-8") as f:
    test_questions = json.load(f)["questions"]

for model in ["t5-small", "t5-base"]:

    with open(model+"-outputs/errors.csv", "r", encoding="utf-8") as ef:
        error_query_ids[model] = ef.readlines()
        error_query_ids[model] = [int(id.strip()) for id in error_query_ids[model]]

    with open(model+"-outputs/correct.csv", "r", encoding="utf-8") as cf:
        correct_query_ids[model] = cf.readlines()
        correct_query_ids[model] = [int(id.strip()) for id in correct_query_ids[model]]

    with open(model+"-outputs/predictions.csv", "r", encoding="utf-8") as pf:
        reader = csv.reader(pf)
        next(reader)

        id = 0

        for row in reader:
            generated_query = clean_query(row[1])
            actual_query = clean_query(row[2])

            if id in error_query_ids[model]:
                test_question = test_questions[id]
                error_query[model].append({
                    "id": id,
                    "question": test_question["question"],
                    "generated_query": generated_query,
                    "actual_query": actual_query,
                    "template_id": test_question["template_id"],
                    "query_type": test_question["query_type"],
                    "temporal": test_question["temporal"],
                    "held_out": test_question["held_out"]
                })
            elif id in correct_query_ids[model]:
                test_question = test_questions[id]
                correct_query[model].append({
                    "id": id,
                    "question": test_question["question"],
                    "generated_query": generated_query,
                    "actual_query": actual_query,
                    "template_id": test_question["template_id"],
                    "query_type": test_question["query_type"],
                    "temporal": test_question["temporal"],
                    "held_out": test_question["held_out"]
                })
            id += 1

    with open(model+"-error_query.json", "w", encoding="utf-8") as f:
        json.dump(error_query, f, indent=4)
    
    with open(model+"-correct_query.json", "w", encoding="utf-8") as f:
        json.dump(correct_query, f, indent=4)


            
        
