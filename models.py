"""
    Generate question-query pairs
"""
import re
import json
import random
import logging

import requests
import urllib.parse

import spacy
from spacy.matcher import Matcher

nlp = spacy.load("en_core_web_sm")

from templates import templates

logging.basicConfig(level=logging.INFO)

with open("data/CORE.json", "r") as f:
    CORE = json.load(f)

class Sample:
    """
        Wrapper for the sample sub-graph sampled from the graph
    """
    def __init__(self, data):
        self.data = data[next(iter(data))]
        self.uri = next(iter(data))
        self.title = self.__get_title()
        self.bibtextype = self.__get_bibtextype()
        self.authors = self.__get_authors()
        self.year = self.__get_year()
        self.venue = self.__get_venue()
        self.validate = self.__validate()
    
    def __validate(self):
        return self.title and self.bibtextype and self.authors and self.year and self.venue
    
    def dblp_prefix(self, predicate):
        return f"<https://dblp.org/rdf/schema#{predicate}>"

    def __get_title(self):
        return self.data.get(self.dblp_prefix("title"),[""])[0].replace('"',"").replace('.','')

    def __get_bibtextype(self):
        return self.data.get(self.dblp_prefix("bibtexType"),[""])[0].replace('"',"")

    def __get_authors(self):
        authors = self.data.get(self.dblp_prefix("authoredBy"), [])
        return [
            {
                "uri": next(iter(author)),
                "name": author[next(iter(author))].get(self.dblp_prefix("primaryFullCreatorName"), [""])[0].replace('"',""),
                "affiliation": author[next(iter(author))].get(self.dblp_prefix("primaryAffiliation"), [""])[0].replace('"',"")
            } for author in authors] if authors else None

    def __get_year(self):
        return self.data.get(self.dblp_prefix("yearOfPublication"),[""])[0].replace('"',"")
    
    def __get_venue(self):
        return self.data.get(self.dblp_prefix("publishedIn"),[""])[0].replace('"',"")


class SampleGenerator:
    """
        Get a sample from the graph
    """
    def __init__(self, graph):
        self.graph = graph
    
    def get(self, type, count=1):
        """
            Return a valid sample from the graph
        """
        sample = Sample(self.graph.sample_vertex(type, count))
        if sample.validate:
            return sample
        return self.get(type, count)


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
            return json.loads(response.text)
        return []

class KeywordGenerator:
    """
        Keyword generator from the title
    """
    def __init__(self):
        pass
    
    def get(self, title):
        """
            Extract main keywords from the title using spacy
        """
        doc = nlp(title.lower())
        matcher = Matcher(nlp.vocab)
        
        pattern = [{"POS": "NOUN"}, {"POS": "NOUN", "OP": "*"}, {"POS": "NOUN"}]
        matcher.add("NOUN_PHRASE", [pattern])
        matches = matcher(doc)
        
        keywords = [doc[start:end].text for _, start, end in matches]
        keywords = [keyword for keyword in keywords if not nlp.vocab[keyword].is_stop]
        return random.choice(keywords).capitalize() if keywords else "NONE"

class DataGenerator:
    """
        Generate question-query pairs
    """
    def __init__(self, graph, seed):
        random.seed(seed)
        self.entity_types = ["CREATOR", "PUBLICATION"]
        self.query_types = [
            "SINGLE_FACT","MULTI_FACT","DOUBLE_INTENT",
            "BOOLEAN","NEGATION","DOUBLE_NEGATION",
            "UNION","DISAMBIGUATION",
            "COUNT","SUPERLATIVE"
        ]
        self.sample_generator = SampleGenerator(graph)
        self.server = DBLPServer("config.json")
        self.keyword_generator = KeywordGenerator()

    def alt_name(self, name):
        """
            Generate alternative name for the creator
        """
        if name == "": return "NONE"

        name = name.split(" ")
        if len(name) == 1: return name[0]

        alt_names = [
            name[-1] + ", " + name[0] + " " + " ".join(name[1:-1]), # Smith, John William
            name[0][0].replace(".","") + ". " + " ".join(name[1:]), # J. William Smith
            name[0] + " " + name[1][0].replace(".","") + ". " + " ".join(name[2:]), # John W. Smith
            name[-1] + ", " + name[0][0].replace(".","") + ". " + " ".join(name[1:-1]), # Smith, J. William
        ]
        return " ".join(random.choice(alt_names).split(" "))

    def alt_duration(self, duration):
        """
            Generate alternative duration
        """
        num2words = {
            "1": "one", "2": "two", "3": "three", "4": "four", "5": "five",
            "6": "six", "7": "seven", "8": "eight", "9": "nine", "10": "ten"
        }
        return num2words[duration]

    def alt_venue(self, venue):
        """
            Generate alternative venue
        """
        venue = re.sub(r"\(.*\)", "", venue).strip()
        return CORE.get(venue.upper().replace(".",""), venue)

    def fill_slots(self, template, first_sample, second_sample):
        """
            Fill the slots in the template with the values from the samples
        """
        def get_bibtextype(bibtextype):
            return bibtextype.split("#")[1].replace(">", "")

        if first_sample.authors:
            if len(first_sample.authors) > 1:
                creator, other_creator = random.sample(first_sample.authors, 2)
            else:
                creator, other_creator = first_sample.authors[0], second_sample.authors[0]
        else:
            creator, other_creator = {}, {}

        name = creator.get("name", "NONE")
        other_name = other_creator.get("name", "NONE")        
        duration = str(random.choice(range(1, 10)))
        venue = first_sample.venue
        other_venue = second_sample.venue

        slots = {
            "?p1": first_sample.uri,
            "?p2": second_sample.uri,
            "?c1": creator.get("uri", "NONE"),
            "?c2": other_creator.get("uri", "NONE"),
            "?b": first_sample.bibtextype,
            "[TITLE]": first_sample.title,
            "[OTHER_TITLE]": second_sample.title,
            "[CREATOR_NAME]": [name, self.alt_name(name)],
            "[OTHER_CREATOR_NAME]": [other_name, self.alt_name(other_name)],
            "[TYPE]": get_bibtextype(first_sample.bibtextype),
            "[PARTIAL_CREATOR_NAME]": name.split(" "),
            "[AFFILIATION]": creator.get("affiliation", "NONE"),
            "[YEAR]": first_sample.year,
            "[DURATION]": [duration, self.alt_duration(duration)],
            "[VENUE]": [venue, self.alt_venue(venue)],
            "[OTHER_VENUE]": [other_venue, self.alt_venue(other_venue)],
            "[KEYWORD]": self.keyword_generator.get(first_sample.title)
        }

        # Randomly select two questions
        question, paraphrase = random.sample(template["questions"]["strings"], 2)
        query = template["query"]["sparql"]

        # Fill in the template with the sample
        for placeholder, value in slots.items():
            question, paraphrase = [
                    each.replace(placeholder, str(random.choice(value)))
                        for each in [question, paraphrase]
                ]
            query = query.replace(
                    placeholder, str(random.choice(value))
                    if placeholder not in ["[DURATION]","[VENUE]","[OTHER_VENUE]"] else value[0]
                )
        
        entities = []
        
        # Save the entities
        for entity in template["query"]["entities"]:
            entities.append(slots[entity])

        return question, paraphrase, query, entities

    def generate(self, num_samples):
        """
            Generate question-query pairs
        """

        valid_query_count_dict = {
            "Publication": {query_type: 0 for query_type in self.query_types},
            "Creator": {query_type: 0 for query_type in self.query_types}
        }

        invalid_query_count_dict = {
            "Publication": {query_type: 0 for query_type in self.query_types},
            "Creator": {query_type: 0 for query_type in self.query_types}
        }
        
        required_samle_size = (num_samples / len(self.entities)) / len(self.query_types)

        valid_query_index = 0
        invalid_query_index = 0

        for entity_type in self.entity_types:
            for query_type in self.query_types:
                
                while valid_query_count_dict[entity_type][query_type] < required_samle_size:
                    
                    # Get two random samples
                    first_sample = self.sample_generator.get("Publication")
                    second_sample = self.sample_generator.get("Publication")

                    # Get a random template for entity type and query type
                    template = random.choice(templates[entity_type][query_type])

                    # Fill in the template with the sample
                    question, paraphrased_question, query, entities = self.fill_slots(template, first_sample, second_sample)
                    answers = self.server.query(query)

                    if answers:
                        valid_query_index += 1
                        valid_query_count_dict[entity_type][query_type] += 1
                        id = "Q"+str(valid_query_index).zfill(4) # Q0001, Q0002, ...
                    else:
                        invalid_query_index += 1
                        invalid_query_count_dict[entity_type][query_type] += 1
                        id = "Q"+str(invalid_query_index).zfill(4)

                    yield id, {
                        "entities": entities,
                        "relations": template["relations"],
                        "query_type": query_type,
                        "template_id": template["id"],
                        "question": [{
                            "language": "en",
                            "string": question
                        }],
                        "paraphrased_question": [{
                            "language": "en",
                            "string": paraphrased_question
                        }],
                        "query": [{
                            "sparql": query,
                        }]
                    }, {"answer": answers}
