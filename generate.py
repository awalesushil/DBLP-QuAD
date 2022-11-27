"""
    Generate question-query pairs
"""
import json
import random

from templates import templates
from dblp import Graph

dblp = Graph("DBLP")
dblp.load_from_pickle("dblp.pkl")

class Sample:
    """
        Wrapper for the sample sub-graph sampled from the graph
    """
    def __init__(self, data):
        self.data = data[next(iter(data))]
        self.uri = next(iter(data))
        self.title = self.__get_title()
        self.type = self.__get_type()
        self.authors = self.__get_authors()
        self.year = self.__get_year()
        self.venue = self.__get_venue()
    
    def dblp_prefix(self, predicate):
        return f"<https://dblp.org/rdf/schema#{predicate}>"

    def __get_title(self):
        return self.data.get(self.dblp_prefix("title"),[""])[0]

    def __get_type(self):
        return self.data.get(self.dblp_prefix("bibtexType"),[""])[0]

    def __get_authors(self):
        for author in self.data.get(self.dblp_prefix("authoredBy"),[]):
            print(author)
        return [
            {
                "uri": next(iter(author)),
                "name": author.get(self.dblp_prefix("primaryFullCreatorName"), ""),
                "affiliation": author.get(self.dblp_prefix("primaryAffiliation"), "")
            } for author in self.data.get(self.dblp_prefix("authoredBy"),[])]

    def __get_year(self):
        return self.data.get(self.dblp_prefix("yearOfPublication"),[""])[0]
    
    def __get_venue(self):
        return self.data.get(self.dblp_prefix("publishedIn"),[""])[0]


class SampleGenerator:
    """
        Get a sample from the graph
    """
    def __init__(self, graph):
        self.graph = graph
    
    def get(self, type, count=1):
        """
            Get a sample from the graph
        """
        return Sample(self.graph.sample_vertex(type, count))


class TemplateGenerator:
    """
        Template functions
    """
    def __init__(self):
        self.entities = ["CREATOR", "PUBLICATION"]
        self.query_types = [
            "SINGLE_FACT","MULTI_FACT","DOUBLE_INTENT",
            "BOOLEAN","NEGATION","DOUBLE_NEGATION",
            "UNION","DISAMBIGUATION",
            "COUNT","RANK"
        ]

    def get(self):
        """
            Get a random template from the templates dictionary
        """
        # Randomly select an entity and query type
        entity = random.choice(self.entities)
        query_type = random.choices(self.query_types)[0]

        return random.choice(templates[entity][query_type]), entity, query_type

keywords = ["entity linking"]

class DataGenerator:
    """
        Generate question-query pairs
    """
    def __init__(self, graph):
        self.sample_generator = SampleGenerator(graph)
        self.template_generator = TemplateGenerator()

    def fill_slots(self, template, first_sample, second_sample):
        
        creator = random.choice(first_sample.authors)
        other_creator = random.choice(second_sample.authors)
        duration = random.choice(range(1, 5))

        mapping_dict = {
            "?p1": first_sample.uri,
            "?p2": second_sample.uri,
            "?c1": creator.uri,
            "?c2": other_creator.uri,
            "[TITLE]": first_sample.title,
            "[OTHER_TITLE]": second_sample.title,
            "[TYPE]": first_sample.type,
            "[CREATOR_NAME]": creator.name,
            "[OTHER_CREATOR_NAME]": other_creator.name,
            "[PARTIAL_CREATOR_NAME]": creator.split(" ")[0],
            "[AFFILIATION]": creator.affiliation,
            "[YEAR]": first_sample.year,
            "[DURATION]": duration,
            "[VENUE]": first_sample.venue,
            "[OTHER_VENUE]": second_sample.venue,
            "[KEYWORD]": str(keywords[0])
        }

        # Randomly select a question
        question = random.choice(template["questions"])
        query = template["query"]

        # Fill in the template with the sample
        for placeholder, value in mapping_dict.items():
            question = question.replace(placeholder, value)
            query = query.replace(placeholder, value)

        return question, query

    def generate(self, n=1):
        """
            Generate question-query pairs
        """
        for _ in range(n):

            # Get two random samples
            first_sample = self.sample_generator.get("Publication")
            second_sample = self.sample_generator.get("Publication")

            # Get a random template
            template, entity, query_type = self.template_generator.get()

            # Fill in the template with the sample
            question, query = self.fill_slots(template, first_sample, second_sample)

            yield question, query, entity, query_type

if __name__ == "__main__":

    dataGenerator = DataGenerator(dblp).generate(500)
    
    dataset = []
    with open("train.json", "w", encoding="utf-8") as f:
        for question, query, entity, query_type in dataGenerator:
            dataset.append({
                "question": question,
                "query": query,
                "entity": entity,
                "query_type": query_type
            })
        json.dump(dataset, f, indent=4)