"""
    Generate question-query pairs
"""
import json
import random

from templates import templates
from dblp import Graph

class Sample:
    """
        Wrapper for the sample sub-graph sampled from the graph
    """
    def __init__(self, data):
        self.data = data[next(iter(data))]
        self.title = self.__get_title()
        self.type = self.__get_type()
        self.authors = self.__get_authors()
        self.author_names = self.__get_author_names()
        self.affiliations = self.__get_affiliations()
        self.year = self.__get_year()
        self.venue = self.__get_venue()
    
    def dblp_prefix(self, predicate):
        return f"<https://dblp.org/rdf/schema#{predicate}>"

    def __get_title(self):
        return self.data.get(self.dblp_prefix("title"),[""])[0]

    def __get_type(self):
        return self.data.get(self.dblp_prefix("bibtexType"),[""])[0]

    def __get_authors(self):
        return self.data.get(self.dblp_prefix("authoredBy"),[])
    
    def __get_author_names(self):
        return [author.get(self.dblp_prefix("primaryFullCreatorName"), "") for author in self.authors]
    
    def __get_affiliations(self):
        return [author.get(self.dblp_prefix("primaryAffiliation"), "") for author in self.authors]

    def __get_year(self):
        return self.data.get(self.dblp_prefix("yearOfPublication"),[""])[0]
    
    def __get_venue(self):
        return self.data.get(self.dblp_prefix("publishedIn"),[""])[0]


def get_random_template():
    """
        Get a random template from the templates dictionary
    """
    entity = random.choice(["CREATOR", "PUBLICATION"])
    query_types = ["FACTOID","DOUBLE_INTENT","ASK","AGGREGATION","DISAMBIGUATION"]
    
    total_templates = sum([len(templates[entity][each]) for each in query_types])
    weights = [len(templates[entity][each])/total_templates for each in query_types]

    query_type = random.choices(query_types, weights=weights)[0] # Weighted Sampling for query type

    return random.choice(templates[entity][query_type]), entity, query_type

keywords = ["entity linking"]

dblp = Graph("DBLP")
dblp.load_from_pickle("dblp.pkl")

def generate_example():

    sample = Sample(dblp.sample_vertex("Publication", count=1))
    second_sample = Sample(dblp.sample_vertex("Publication", count=1))
    creator_name = random.choice(sample.author_names)
    other_creator_name = random.choice(sample.author_names)
    affiliation = random.choice(sample.affiliations)
    duration = random.choice(range(1, 5))

    mapping_dict = {
        "[TITLE]": sample.title,
        "[OTHER_TITLE]": second_sample.title,
        "[TYPE]": sample.type,
        "[CREATOR_NAME]": creator_name,
        "[OTHER_CREATOR_NAME]": other_creator_name,
        "[PARTIAL_CREATOR_NAME]": creator_name.split(" ")[0],
        "[AFFILIATION]": affiliation,
        "[YEAR]": sample.year,
        "[DURATION]": duration,
        "[VENUE]": sample.venue,
        "[OTHER_VENUE]": second_sample.venue,
        "[KEYWORD]": keywords[0]
    }

    template, entity, query_type = get_random_template()
    
    question = random.choice(template["questions"])
    query = template["query"]

    # Fill in the template with the sample
    for placeholder, value in mapping_dict.items():
        question = question.replace(placeholder, value)
        query = query.replace(placeholder, value)

    return question, query, entity, query_type


if __name__ == "__main__":

    dataset = []
    with open("train.json", "w", encoding="utf-8") as f:
        for i in range(50):
            question, query, entity, query_type = generate_example()
            dataset.append({"question": question, "query": query, "entity": entity, "query_type": query_type})
        json.dump(dataset, f, indent=4)