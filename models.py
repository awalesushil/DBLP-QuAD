"""
    Generate question-query pairs
"""
import re
import json
import random
import logging

import requests
import urllib.parse
from itertools import combinations

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
                "name": author[next(iter(author))].get(self.dblp_prefix("primaryFullCreatorName"), ["NONE"])[0].replace('"',""),
                "affiliation": author[next(iter(author))].get(self.dblp_prefix("primaryAffiliation"), ["NONE"])[0].replace('"',"")
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
            result = json.loads(response.text)

            if "boolean" in result.keys():
                return result
            elif "results" in result.keys():
                if result["results"]["bindings"]:
                    return result
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

class ParaphrasePairGenerator:
    """
        Generate paraphrase pairs
    """
    def __init__(self):
        self.datagenerator = DataGenerator()
    
    def generate(self):
        for entity_type in self.datagenerator.entity_types:
            for query_type in self.datagenerator.query_types:
                for each in templates[entity_type][query_type]:
                    first_sample = self.sample_generator.get("Publication")
                    second_sample = self.sample_generator.get("Publication")
                    _, _, _, _, paraphrase_pairs = self.datagenerator.fill_slots(each, first_sample, second_sample, group="test")
        return paraphrase_pairs

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
            "COUNT","SUPERLATIVE+COMPARATIVE"
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
            name[-1] + ", " + name[0][0].replace(".","") + ". " + " ".join(name[1:-1]) # Smith, J. William
        ]
        alt_name = random.choice(alt_names) + "$"
        return alt_name.replace(" $","").replace("$","")

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

    def alt_affiliation(self, affiliation):
        """
            Generate alternative affiliation name
        """
        affiliation = affiliation.split(",")[0]
        return affiliation

    def fill_slots(self, template, first_sample, second_sample, group):
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

        name = creator.get("name")
        other_name = other_creator.get("name")
        affiliation = creator.get("affiliation")
        duration = str(random.choice(range(2, 10)))
        venue = first_sample.venue
        other_venue = second_sample.venue

        slots = {
            "?p1": [first_sample.uri],
            "?p2": [second_sample.uri],
            "?c1": [creator.get("uri")],
            "?c2": [other_creator.get("uri")],
            "?b": [first_sample.bibtextype],
            "[TITLE]": [first_sample.title],
            "[OTHER_TITLE]": [second_sample.title],
            "[CREATOR_NAME]": [name, self.alt_name(name)],
            "[OTHER_CREATOR_NAME]": [other_name, self.alt_name(other_name)],
            "[TYPE]": [get_bibtextype(first_sample.bibtextype)],
            "[PARTIAL_CREATOR_NAME]": name.split(" "),
            "[AFFILIATION]": [affiliation, self.alt_affiliation(affiliation)],
            "[YEAR]": [first_sample.year],
            "[DURATION]": [duration, self.alt_duration(duration)],
            "[VENUE]": [venue, self.alt_venue(venue)],
            "[OTHER_VENUE]": [other_venue, self.alt_venue(other_venue)],
            "[KEYWORD]": [self.keyword_generator.get(first_sample.title)]
        }

        question_strings = template["question"]["strings"].copy()
        paraphrase_pairs = list(combinations(question_strings, 2))

        # Withold two questions for the train set but not test set
        if group == "train":
            question_strings.pop(1)
            question_strings.pop(2)

        # Randomly select two questions
        question, paraphrase = random.sample(question_strings, 2)
        query = template["query"]["sparql"]

        # Fill in the template with the sample
        for placeholder, value in slots.items():
            question, paraphrase = [
                    each.replace(placeholder, str(random.choice(value)))
                        for each in [question, paraphrase]
                ]

            query = query.replace(placeholder, value[0]
                if placeholder.startswith("?") or placeholder == "[DURATION]" else "'" + str(value[0]) + "'")

            paraphrase_pairs = [
                (template["id"],
                    each[0].replace(placeholder, str(random.choice(value))),
                        each[1].replace(placeholder, str(random.choice(value))))
                    for each in paraphrase_pairs
            ]
        
        entities = []
        
        # Save the entities
        for entity in template["question"]["entities"]:
            entities.append(slots[entity][0])

        return question, paraphrase, query, entities, paraphrase_pairs

    def generate(self, group, num_samples):
        """
            Generate question-query pairs
        """

        valid_query_count_dict = {
            "PUBLICATION": {query_type: 0 for query_type in self.query_types},
            "CREATOR": {query_type: 0 for query_type in self.query_types}
        }

        invalid_query_count_dict = {
            "PUBLICATION": {query_type: 0 for query_type in self.query_types},
            "CREATOR": {query_type: 0 for query_type in self.query_types}
        }
        
        required_sample_size = (num_samples / len(self.entity_types)) / len(self.query_types)

        valid_query_index = 0
        invalid_query_index = 0

        for entity_type in self.entity_types:
            for query_type in self.query_types:
                
                while valid_query_count_dict[entity_type][query_type] < required_sample_size:
                    
                    # Get two random samples
                    first_sample = self.sample_generator.get("Publication")
                    second_sample = self.sample_generator.get("Publication")

                    # Withold test_only templates for the train set
                    selected_templates = templates[entity_type][query_type]
                    if group == "train":
                        selected_templates = [template for template in selected_templates if not template["test_only"]]

                    # Get a random template for entity type and query type
                    template = random.choice(selected_templates)

                    # Fill in the template with the sample
                    question, paraphrase, query, entities, _ = self.fill_slots(template, first_sample, second_sample, group)
                    answers = self.server.query(query)

                    if answers and not re.search("NONE", question) and not re.search("NONE", paraphrase):
                        valid_query_index += 1
                        valid_query_count_dict[entity_type][query_type] += 1
                        id = "Q"+str(valid_query_index).zfill(4) # Q0001, Q0002, ...
                    else:
                        invalid_query_index += 1
                        invalid_query_count_dict[entity_type][query_type] += 1
                        id = "Q"+str(invalid_query_index).zfill(4)

                    yield id, {
                            "query_type": query_type,
                            "question": {
                                "string": question
                            },
                            "paraphrased_question": {
                                "string": paraphrase
                            },
                            "query": {
                                "sparql": query,
                            },
                            "template_id": template["id"],
                            "entities": entities,
                            "relations": template["question"]["relations"],
                            "temporal": template["query"]["temporal"],
                            "held_out": template["test_only"],
                        }, {
                            "answer": answers
                        }
