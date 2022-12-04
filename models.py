"""
    Generate question-query pairs
"""
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
        self.type = self.__get_type()
        self.authors = self.__get_authors()
        self.year = self.__get_year()
        self.venue = self.__get_venue()
        self.validate = self.__validate()
    
    def __validate(self):
        return self.title and self.type and self.authors and self.year and self.venue
    
    def dblp_prefix(self, predicate):
        return f"<https://dblp.org/rdf/schema#{predicate}>"

    def __get_title(self):
        return self.data.get(self.dblp_prefix("title"),[""])[0].replace('"',"'").replace('.','')

    def __get_type(self):
        return self.data.get(self.dblp_prefix("bibtexType"),[""])[0].replace('"',"'")

    def __get_authors(self):
        authors = self.data.get(self.dblp_prefix("authoredBy"), [])
        return [
            {
                "uri": next(iter(author)),
                "name": author[next(iter(author))].get(self.dblp_prefix("primaryFullCreatorName"), [""])[0].replace('"',"'"),
                "affiliation": author[next(iter(author))].get(self.dblp_prefix("primaryAffiliation"), [""])[0].replace('"',"'")
            } for author in authors] if authors else None

    def __get_year(self):
        return self.data.get(self.dblp_prefix("yearOfPublication"),[""])[0].replace('"',"'")
    
    def __get_venue(self):
        return self.data.get(self.dblp_prefix("publishedIn"),[""])[0].replace('"',"'")


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


class DBLPServer:
    """
        DBLP Server class
    """
    def __init__(self, path):
        with open(path, "r", encoding="utf-8") as f:
            self.host = json.load(f)["host"]
        self.prefix = """PREFIX dblp: <https://dblp.org/rdf/schema#>
            PREFIX purl: <http://purl.org/dc/terms/>
        """
        self.result_format = "json"
    
    def query(self, query):
        """
            Query the DBLP server
        """
        query = self.prefix + query
        url = f"{self.host}/sparql?query={urllib.parse.quote(query)}&format=application%2Fsparql-results%2B{self.result_format}"
        response = requests.get(url)
        if response.status_code == 200:
            response_data = json.loads(response.text)
            if 'boolean' in response_data:
                return [{"boolean": response_data["boolean"]}]
            variables = response_data["head"]["vars"]
            results = response_data["results"]["bindings"]
            return [dict(zip(variables, [result[var]["value"] for var in variables])) for result in results]
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
        return "'" + random.choice(keywords) + "'"  if keywords else "''"


class DataGenerator:
    """
        Generate question-query pairs
    """
    def __init__(self, graph):
        self.sample_generator = SampleGenerator(graph)
        self.template_generator = TemplateGenerator()
        self.server = DBLPServer("config.json")
        self.keyword_generator = KeywordGenerator()

    def alt_name(self, name):
        """
            Generate alternative name for the creator
        """

        if name == "''":
            return "''"

        name = name.replace("'", "")
        name = name.split(" ")

        alt_names = [
            name[-1] + ", " + name[0] + " " + " ".join(name[1:-1]), # Smith, John William
            name[0][0] + ". " + " ".join(name[1:]), # J. William Smith
            name[0] + " " + name[1][0] + ". " + " ".join(name[2:]), # John W. Smith
            name[-1] + ", " + name[0][0] + ". " + " ".join(name[1:-1]), # Smith, J. William
        ]
        
        return "'" + random.choice(alt_names) + "'"

    
    def alt_duration(self, duration):
        """
            Generate alternative duration
        """
        num2words = {
            "1": "one", "2": "two", "3": "three", "4": "four", "5": "five",
            "6": "six", "7": "seven", "8": "eight", "9": "nine", "10": "ten"
        }
        return num2words[duration]

    def fill_slots(self, template, first_sample, second_sample):
        
        if first_sample.authors:
            if len(first_sample.authors) > 1:
                creator, other_creator = random.sample(first_sample.authors, 2)
            else:
                creator, other_creator = first_sample.authors[0], {}
        else:
            creator, other_creator = {}, {}

        duration = str(random.choice(range(1, 10)))

        def get_creator_name(name):
            return random.choice([name, self.alt_name(name)])
        
        def get_duration(duration):
            return random.choice([duration, self.alt_duration(duration)])

        def get_venue(venue):
            return random.choice([venue, CORE.get(venue.upper(), venue)])

        def get_partial_name(name):
            name = name.lower().replace("'", "")
            name = name.split(" ")
            return "'" + random.choice(name) + "'"
            
        slots = {
            "?p1": first_sample.uri,
            "?p2": second_sample.uri,
            "?c1": creator.get("uri", "''"),
            "?c2": other_creator.get("uri", "''"),
            "[TITLE]": first_sample.title,
            "[OTHER_TITLE]": second_sample.title,
            "[TYPE]": first_sample.type,
            "[PARTIAL_CREATOR_NAME]": get_partial_name(creator.get("name", "''")),
            "[AFFILIATION]": creator.get("affiliation", "''"),
            "[YEAR]": first_sample.year
        }

        # Randomly select a question
        question, paraphrase = random.sample(template["questions"], 2)
        query = template["query"]

        # Fill in the template with the sample
        for placeholder, value in slots.items():
            
            question = question.replace(placeholder, str(value))
            paraphrase = paraphrase.replace(placeholder, str(value))
            query = query.replace(placeholder, str(value))

        question = question.replace("[CREATOR_NAME]", get_creator_name(creator.get("name", "''")))
        paraphrase = paraphrase.replace("[CREATOR_NAME]", get_creator_name(creator.get("name", "''")))
        
        question = question.replace("[OTHER_CREATOR_NAME]", get_creator_name(other_creator.get("name", "''")))
        paraphrase = paraphrase.replace("[OTHER_CREATOR_NAME]", get_creator_name(other_creator.get("name", "''")))

        question = question.replace("[DURATION]", get_duration(duration))
        paraphrase = paraphrase.replace("[DURATION]", get_duration(duration))
        query = query.replace("[DURATION]", duration)

        question = question.replace("[VENUE]", get_venue(first_sample.venue))
        paraphrase = paraphrase.replace("[VENUE]", get_venue(first_sample.venue))
        query = query.replace("[VENUE]", first_sample.venue)

        question = question.replace("[OTHER_VENUE]", get_venue(second_sample.venue))
        paraphrase = paraphrase.replace("[OTHER_VENUE]", get_venue(second_sample.venue))
        query = query.replace("[OTHER_VENUE]", second_sample.venue)
        
        keyword = self.keyword_generator.get(first_sample.title.lower())
        question = question.replace("[KEYWORD]", keyword)
        paraphrase = paraphrase.replace("[KEYWORD]", keyword)
        query = query.replace("[KEYWORD]", keyword)

        return question, paraphrase, query

    def generate(self, num_samples):
        """
            Generate question-query pairs
        """
        valid_query_count = 0
        while valid_query_count < num_samples:

            # Get two random samples
            first_sample = self.sample_generator.get("Publication")
            second_sample = self.sample_generator.get("Publication")

            # Get a random template
            template, entity, query_type = self.template_generator.get()

            # Fill in the template with the sample
            question, paraphrase, query = self.fill_slots(template, first_sample, second_sample)
            answers = self.server.query(query)

            if answers:
                valid_query_count += 1

            yield question, paraphrase, query, entity, query_type, answers
