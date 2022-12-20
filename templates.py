"""
    A collection of SPARQL templates grouped by query types.
    Each template is a dictionary with the following keys:
        - query: the SPARQL query
        - questions: a list of questions in English that can be generated from the query
    The templates are grouped by entity type:
        - PUBLICATION: a query that returns a fact about a publication
        - CREATOR: a query that returns a fact about a creator
    The templates are further grouped by query type:
        - SINGLE_FACT: a query that returns a single fact
        - MULTI_FACT: a query that returns multiple facts
        - DOUBLE_INTENT: a query that returns two facts
        - BOOLEAN: a query that returns a boolean value
        - NEGATION: a query that returns a negation
        - DOUBLE_NEGATION: a query that returns a double negation
        - COUNT: a query that returns a count
        - SUPERLATIVE: a query that answers a superlative question
        - COMPARISON: a query that answers a comparison question
        - DISAMBIGUATION: a query that answers a disambiguation question

    The templates use the following SPARQL variables for URIs:
        - ?p1: the URI of the publication
        - ?p2: the URI of another publication
        - ?c1: the URI of the creator
        - ?c2: the URI of another creator
        - ?b: the URI of the bibtextype
    
    The templates use the following SPARQL variables for intermediate results:
        - ?x: an intermediate result
        - ?y: another intermediate result
        - ?z: another intermediate result
        - ?t: another intermediate result
        - ?answer: the final result
        - ?firstanswer: the first final result
        - ?secondanswer: the second final result
        - ?count: the count of the final result

    The templates and questions contain the following placeholders/slots for literals:
        - [TITLE]: the title> of the publication
        - [CREATOR_NAME]: the name of the creator
        - [AFFILIATION]: the affiliation of the creator
        - [VENUE]: the venue of the publication
        - [YEAR]: the year of the publication
        - [TYPE]: the bibtextype of the publication
        - [DURATION]: duration in years
        - [OTHER_TITLE]: the title> of another publication
        - [OTHER_CREATOR]: the name of another creator
        - [OTHER_VENUE]: the venue of another publication
        - [PARTIAL_CREATOR_NAME]: a partial name of the creator
        - [KEYWORD]: a keyword generated from the title> of the publication
"""

templates = {
    "PUBLICATION": {
        "SINGLE_FACT": [{
            "id": "TP01",
            "query": {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?answer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Who wrote the paper [TITLE]?",
                    "Who authored the paper [TITLE]?",
                    "Who is the author of the paper [TITLE]?",
                    "[TITLE] was written by who?",
                    "[TITLE] was authored by which authors?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TP02",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?p1 <https://dblp.org/rdf/schema#yearOfPublication> ?answer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "When was [TITLE] published?",
                    "When was the paper [TITLE] published?",
                    "What year was [TITLE] published?",
                    "In what year was [TITLE] published?",
                    "[TITLE] was published in which year?",
                    "The paper [TITLE] was published in which year?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#yearOfPublication>"]
            }
        },{
            "id": "TP03",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?p1 <https://dblp.org/rdf/schema#publishedIn> ?answer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Where was [TITLE] published?",
                    "Where was the paper [TITLE] published?",
                    "In which venue was the paper [TITLE] published?",
                    "[TITLE] was published in which venue?",
                    "The paper [TITLE] was published in which venue?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#publishedIn>"]
            }
        },{
            "id": "TP04",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?p1 <https://dblp.org/rdf/schema#bibtexType> ?answer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "What is the bibtex type of the paper [TITLE]?",
                    "What is the bibtex type of [TITLE]?",
                    "What is the bibtex type of the publication [TITLE]?",
                    "What bibtex type of publication is [TITLE]?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#bibtexType>"]
            }
        },{
            "id": "TP05",
            "query":  {
                "sparql": "SELECT ?answer WHERE { ?p1 <https://dblp.org/rdf/schema#numberOfCreators> ?answer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "How many authors does [TITLE] have?",
                    "How many authors wrote the paper [TITLE]?",
                    "How many authors does the publication [TITLE] have?",
                    "[TITLE] has how many authors?",
                    "The paper [TITLE] has how many authors?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#numberOfCreators>"]
            }
        }],
        "MULTI_FACT": [{
            "id": "TP11",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?x . ?x <https://dblp.org/rdf/schema#primaryAffiliation> ?answer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "What are the primary affiliations of the authors of [TITLE]?",
                    "What are the primary affiliations of the authors of the paper [TITLE]?",
                    "Where are the authors of [TITLE] from?",
                    "Where are the authors of the paper [TITLE] from?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#primaryAffiliation>"]
            }
        },{
            "id": "TP12",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?x . ?answer <https://dblp.org/rdf/schema#authoredBy> ?x FILTER (?answer != ?p1) }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Which other publications were published by the authors of [TITLE]?",
                    "Which other publications were published by the authors of the paper [TITLE]?",
                    "Which other papers were written by the authors of [TITLE]?",
                    "Which other papers were written by the authors of the paper [TITLE]?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TP13",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?x . ?y <https://dblp.org/rdf/schema#authoredBy> ?x . ?y <https://dblp.org/rdf/schema#publishedIn> ?answer FILTER (?y != ?p1) }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "What are the venues of the other papers published by the authors of [TITLE]?",
                    "What are the venues of the other papers published by the authors of the publication [TITLE]?",
                    "In which venues were the other papers published by the authors of [TITLE]?",
                    "In which venues were the other publications published by the authors of [TITLE]?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#publishedIn>"]
            }
        },{
            "id": "TP14",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?x . ?x <https://dblp.org/rdf/schema#affiliation> ?answer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "To which institutions have the authors of [TITLE] been affiliated?",
                    "To which institutions have the authors of the paper [TITLE] been affiliated?",
                    "Which institutions have the authors of [TITLE] been affiliated to?",
                    "Which institutions have the authors of the paper [TITLE] been affiliated to?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#affiliation>"]
            }
        },{
            "id": "TP15",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?x . ?x <https://dblp.org/rdf/schema#orcid> ?answer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "What are the ORCIDs of the authors of [TITLE]?",
                    "What are the ORCIDs of the authors of the paper [TITLE]?",
                    "What ORCIDs do the authors of [TITLE] have?",
                    "What ORCIDs do the authors of the paper [TITLE] have?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#orcid>"]
            }
        },{
            "id": "TP16",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?x . ?p1 <https://dblp.org/rdf/schema#yearOfPublication> ?y . ?z <https://dblp.org/rdf/schema#authoredBy> ?x . ?z <https://dblp.org/rdf/schema#yearOfPublication> ?answer FILTER (?answer != ?y) }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "In which other years were the authors of [TITLE] publishing?",
                    "In which other years have the authors of [TITLE] published?",
                    "The authors of [TITLE] published in which other years?",
                    "The authors of [TITLE] published research papers in which other years?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#yearOfPublication>"]
            }
        }],
        "DOUBLE_INTENT": [{
            "id": "TP21",
            "query":  {
                "sparql": "SELECT DISTINCT ?firstanswer ?secondanswer WHERE { ?p1 <https://dblp.org/rdf/schema#publishedIn> ?firstanswer . ?p1 <https://dblp.org/rdf/schema#yearOfPublication> ?secondanswer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Where was [TITLE] published and when?",
                    "Where was the publication [TITLE] published and when?",
                    "Where was the paper [TITLE] published and in which year?",
                    "In which venue was [TITLE] published and when?",
                    "In which venue was the paper [TITLE] published and when?",
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#publishedIn>", "<https://dblp.org/rdf/schema#yearOfPublication>"]
            }
        },{
            "id": "TP22",
            "query":  {
                "sparql": "SELECT DISTINCT ?firstanswer ?secondanswer WHERE { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?firstanswer . ?firstanswer <https://dblp.org/rdf/schema#primaryAffiliation> ?secondanswer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Who are the authors of [TITLE] and where are they from?",
                    "Who are the authors of the paper [TITLE] and where are they from?",
                    "Who are the authors of the publication [TITLE] and where are they from?",
                    "Who are the authors of the paper [TITLE] and what are their affiliations?",
                    "Who are the authors of the publication [TITLE] and what are their affiliations?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#primaryAffiliation>"]
            }
        },{
            "id": "TP23",
            "query":  {
                "sparql": "SELECT DISTINCT ?firstanswer ?secondanswer WHERE { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?firstanswer . ?secondanswer <https://dblp.org/rdf/schema#authoredBy> ?firstanswer FILTER (?secondanswer != ?p1) }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Who are the authors of [TITLE] and which other papers did they publish?",
                    "Who are the authors of the paper [TITLE] and which other papers did they publish?",
                    "Who are the authors of the publication [TITLE] and which other papers did they publish?",
                    "Who are the authors of the paper [TITLE] and what other papers did they publish?",
                    "Who are the authors of the publication [TITLE] and what other papers did they publish?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TP24",
            "query":  {
                "sparql": "SELECT DISTINCT ?firstanswer ?secondanswer WHERE { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?firstanswer . ?x <https://dblp.org/rdf/schema#authoredBy> ?firstanswer . ?x <https://dblp.org/rdf/schema#publishedIn> ?secondanswer FILTER (?x != ?p1) }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Who are the authors of [TITLE] and what are the venues of the other papers they published?",
                    "Who are the authors of the paper [TITLE] and what are the venues of the other papers they published?",
                    "Who are the authors of the publication [TITLE] and what are the venues of the other papers they published?",
                    "Who are the authors of the paper [TITLE] and where did they publish other papers?",
                    "Who are the authors of the publication [TITLE] and where did they publish other papers?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#publishedIn>"]
            }
        }],
        "BOOLEAN": [{
            "id": "TP31",
            "query":  {
                "sparql": "ASK { ?p1 <https://dblp.org/rdf/schema#title> [TITLE] }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Does [TITLE] exist?",
                    "Does the paper [TITLE] exist?",
                    "Does the publication [TITLE] exist?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#title>"]
            }
        },{
            "id": "TP32",
            "query":  {
                "sparql": "ASK { ?p1 <http://purl.org/dc/terms/bibtexType> ?b }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Is [TITLE] a [TYPE] publication?",
                    "Is the publication [TITLE] a [TYPE] paper?",
                    "Is the paper [TITLE] a [TYPE] publication?"
                ],
                "entities": ["?p1", "?b"],
                "relations": ["<http://purl.org/dc/terms/bibtexType>"]
            }
        },{
            "id": "TP33",
            "query":  {
                "sparql": "ASK { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?x . ?x <https://dblp.org/rdf/schema#primaryAffiliation> [AFFILIATION] }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Do the authors of [TITLE] have [AFFILIATION] as their primary affiliation?",
                    "Do the authors of the publication [TITLE] have [AFFILIATION] as their primary affiliation?",
                    "Is [AFFILIATION] the primary affiliation of the authors of [TITLE]?",
                    "Is [AFFILIATION] the primary affiliation of the authors of the paper [TITLE]?"
                ],
                "entities": ["?p1","[AFFILIATION]"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#primaryAffiliation>"]
            }
        },{
            "id": "TP34",
            "query":  {
                "sparql": "ASK { ?p1 <https://dblp.org/rdf/schema#yearOfPublication> [YEAR] }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Was [TITLE] published in [YEAR]?",
                    "Was the paper [TITLE] published in [YEAR]?",
                    "Was the publication [TITLE] published in [YEAR]?",
                    "Was [TITLE] published in the year [YEAR]?",
                    "Was the paper [TITLE] published in the year [YEAR]?",
                    "Was the publication [TITLE] published in the year [YEAR]?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#yearOfPublication>"]
            }
        },{
            "id": "TP35",
            "query":  {
                "sparql": "ASK { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?x . ?p2 <https://dblp.org/rdf/schema#authoredBy> ?x FILTER (?p2 != ?p1) }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Did the authors of [TITLE] also publish [OTHER_TITLE]?",
                    "Did the authors of the paper [TITLE] also publish [OTHER_TITLE]?",
                    "Did the authors of the publication [TITLE] also publish [OTHER_TITLE]?",
                    "Did the authors of [TITLE] also publish the paper [OTHER_TITLE]?",
                    "Did the authors of the paper [TITLE] also publish the paper [OTHER_TITLE]?",
                    "Did the authors of the publication [TITLE] also publish the paper [OTHER_TITLE]?",
                    "Did the authors of [TITLE] also publish the publication [OTHER_TITLE]?",
                    "Did the authors of the paper [TITLE] also publish the publication [OTHER_TITLE]?",
                    "Did the authors of the publication [TITLE] also publish the publication [OTHER_TITLE]?"
                ],
                "entities": ["?p1", "?p2"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TP36",
            "query":  {
                "sparql": "ASK { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?x . ?y <https://dblp.org/rdf/schema#authoredBy> ?x FILTER (?y != ?p1) . ?y <https://dblp.org/rdf/schema#publishedIn> [OTHER_VENUE] }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Did the authors of [TITLE] also publish a paper in [OTHER_VENUE]?",
                    "Did the authors of the paper [TITLE] publish other papers in [OTHER_VENUE]?",
                    "Did the authors of the publication [TITLE] publish other papers in [OTHER_VENUE]?",
                    "Did the authors of [TITLE] also publish a publication in [OTHER_VENUE]?",
                    "Did the authors of the paper [TITLE] also publish a publication in [OTHER_VENUE]?",
                    "Did the authors of the publication [TITLE] also publish a publication in [OTHER_VENUE]?",
                    "Did the authors of [TITLE] also publish a paper in the venue [OTHER_VENUE]?"
                ],
                "entities": ["?p1", "[OTHER_VENUE]"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#publishedIn>"]
            }
        }],
        "NEGATION": [{
            "id": "TP41",
            "query":  {
                "sparql": "ASK { ?p1 <https://dblp.org/rdf/schema#title> [TITLE] FILTER NOT EXISTS { ?p1 <https://dblp.org/rdf/schema#title> [TITLE] } }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Does [TITLE] not exist?",
                    "Does the paper [TITLE] not exist?",
                    "Doesn't the publication [TITLE] exist?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#title>"]
            }
        },{
            "id": "TP42",
            "query":  {
                "sparql": "ASK { ?p1 <https://dblp.org/rdf/schema#yearOfPublication> [YEAR] FILTER NOT EXISTS { ?p1 <https://dblp.org/rdf/schema#yearOfPublication> [YEAR] } }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Was [TITLE] not published in [YEAR]?",
                    "Was the paper [TITLE] not published in [YEAR]?",
                    "Wasn't the publication [TITLE] published in [YEAR]?",
                    "Wasn't [TITLE] published in the year [YEAR]?",
                    "Wasn't the paper [TITLE] published in the year [YEAR]?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#yearOfPublication>"]
            }
        },{
            "id": "TP43",
            "query":  {
                "sparql": "ASK { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?x . ?y <https://dblp.org/rdf/schema#authoredBy> ?x FILTER (?y != ?p1) . ?y <https://dblp.org/rdf/schema#publishedIn> [VENUE] FILTER NOT EXISTS { ?p1 <https://dblp.org/rdf/schema#publishedIn> [VENUE] } }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Did the authors of [TITLE] not publish a paper in [VENUE]?",
                    "Didn't the authors of the paper [TITLE] publish a paper in [VENUE]?",
                    "Did the authors of the publication [TITLE] not publish a paper in [VENUE]?",
                    "Didn't the authors of [TITLE] publish a publication in [VENUE]?",
                    "Have the authors of the paper [TITLE] not published a publication in [VENUE]?",
                    "Haven't the authors of the publication [TITLE] published a publication in [VENUE]?",
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#publishedIn>"]
            }
        },{
            "id": "TP44",
            "query":  {
                "sparql": "ASK { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?x . ?p2 <https://dblp.org/rdf/schema#authoredBy> ?x FILTER (?p2 != ?p1) FILTER NOT EXISTS { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?x . ?p2 <https://dblp.org/rdf/schema#authoredBy> ?x FILTER (?p2 != ?p1) } }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Did the authors of [TITLE] not publish [OTHER_TITLE]?",
                    "Didn't the authors of the paper [TITLE] publish [OTHER_TITLE]?",
                    "Did the authors of the publication [TITLE] not publish [OTHER_TITLE]?",
                    "Didn't the authors of [TITLE] publish the paper [OTHER_TITLE]?",
                    "Have the authors of the paper [TITLE] not published the paper [OTHER_TITLE]?",
                    "Haven't the authors of the publication [TITLE] published the paper [OTHER_TITLE]?"
                ],
                "entities": ["?p1", "?p2"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        }],
        "DOUBLE_NEGATION": [{
            "id": "TP51",
            "query":  {
                "sparql": "ASK { ?p1 <https://dblp.org/rdf/schema#title> [TITLE] }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Does [TITLE] not not exist?",
                    "Doesn't the paper [TITLE] not exist?",
                    "Does the publication [TITLE] not not exist?",
                    "Doesn't the publication [TITLE] not exist?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#title>"]
            }
        },{
            "id": "TP52",
            "query":  {
                "sparql": "ASK { ?p1 <https://dblp.org/rdf/schema#yearOfPublication> [YEAR] }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Was [TITLE] not not published in [YEAR]?",
                    "Wasn't the paper [TITLE] not published in [YEAR]?",
                    "Was the publication [TITLE] not not published in [YEAR]?",
                    "Wasn't [TITLE] not published in the year [YEAR]?",
                    "Was the paper [TITLE] not not published in the year [YEAR]?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#yearOfPublication>"]
            }
        },{
            "id": "TP53",
            "query":  {
                "sparql": "ASK { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?x . ?y <https://dblp.org/rdf/schema#authoredBy> ?x FILTER (?y != ?p1) . ?y <https://dblp.org/rdf/schema#publishedIn> [VENUE] }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Did the authors of [TITLE] not not publish a paper in [VENUE]?",
                    "Didn't the authors of the paper [TITLE]  not publish a paper in [VENUE]?",
                    "Did the authors of the publication [TITLE] not not publish a paper in [VENUE]?",
                    "Didn't the authors of [TITLE] not not publish a publication in [VENUE]?",
                    "Have the authors of the paper [TITLE] not not published a publication in [VENUE]?",
                    "Haven't the authors of the publication [TITLE] not published a publication in [VENUE]?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#publishedIn>"]
            }
        },{
            "id": "TP54",
            "query":  {
                "sparql": "ASK { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?x . ?p2 <https://dblp.org/rdf/schema#authoredBy> ?x FILTER (?p2 != ?p1) }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Did the authors of [TITLE] not not publish [OTHER_TITLE]?",
                    "Didn't the authors of the paper [TITLE] not not publish [OTHER_TITLE]?",
                    "Did the authors of the publication [TITLE] not not publish [OTHER_TITLE]?",
                    "Didn't the authors of [TITLE] not not publish the paper [OTHER_TITLE]?",
                    "Have the authors of the paper [TITLE] not not published the paper [OTHER_TITLE]?",
                    "Haven't the authors of the publication [TITLE] not published the paper [OTHER_TITLE]?"
                ],
                "entities": ["?p1", "?p2"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        }],
        "UNION": [{
            "id": "TP61",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?answer } UNION { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?answer } }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Who are the authors of [TITLE] and [OTHER_TITLE]?",
                    "Who are the authors of the paper [TITLE] and [OTHER_TITLE]?",
                    "Who are the authors of the publication [TITLE] and [OTHER_TITLE]?",
                    "Who are the authors of the paper [TITLE] and the paper [OTHER_TITLE]?",
                    "Who are the authors of the paper [TITLE] and the publication [OTHER_TITLE]?",
                    "Who are the authors of the publication [TITLE] and the paper [OTHER_TITLE]?",
                    "Who are the authors of the publication [TITLE] and the publication [OTHER_TITLE]?"
                ],
                "entities": ["?p1", "?p2"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TP62",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { { ?p1 <https://dblp.org/rdf/schema#yearOfPublication> ?answer } UNION { ?p2 <https://dblp.org/rdf/schema#yearOfPublication> ?answer } }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "When were [TITLE] and [OTHER_TITLE] published?",
                    "When were the papers [TITLE] and [OTHER_TITLE] published?",
                    "When were the publications [TITLE] and [OTHER_TITLE] published?",
                    "When were the papers [TITLE] and [OTHER_TITLE] published?",
                    "When were the papers [TITLE] and [OTHER_TITLE] published?",
                    "When were the publications [TITLE] and [OTHER_TITLE] published?"
                ],
                "entities": ["?p1", "?p2"],
                "relations": ["<https://dblp.org/rdf/schema#yearOfPublication>"]
            }
        },{
            "id": "TP63",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { { ?p1 <https://dblp.org/rdf/schema#publishedIn> ?answer } UNION { ?p2 <https://dblp.org/rdf/schema#publishedIn> ?answer } }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Where were [TITLE] and [OTHER_TITLE] published?",
                    "Where were the papers [TITLE] and [OTHER_TITLE] published?",
                    "Where were the publications [TITLE] and [OTHER_TITLE] published?",
                    "Where were the papers [TITLE] and [OTHER_TITLE] published?",
                    "Where were the papers [TITLE] and [OTHER_TITLE] published?",
                    "Where were the publications [TITLE] and [OTHER_TITLE] published?"
                ],
                "entities": ["?p1", "?p2"],
                "relations": ["<https://dblp.org/rdf/schema#publishedIn>"]
            }
        }],
        "COUNT": [{
            "id": "TP71",
            "query":  {
                "sparql": "SELECT (COUNT(DISTINCT ?answer) AS ?count) WHERE { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?answer . ?answer <https://dblp.org/rdf/schema#primaryAffiliation> [AFFILIATION] }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "How many authors of [TITLE] have [AFFILIATION] as their primary affiliation?",
                    "How many authors of the paper [TITLE] have [AFFILIATION] as their primary affiliation?",
                    "How many authors of the publication [TITLE] have [AFFILIATION] as their primary affiliation?"
                ],
                "entities": ["?p1", "[AFFILIATION]"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#primaryAffiliation>"]
            }
        },{
            "id": "TP72",
            "query":  {
                "sparql": "SELECT (COUNT(DISTINCT ?answer) AS ?count) WHERE { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?x . ?answer <https://dblp.org/rdf/schema#authoredBy> ?x }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "How many papers did the authors of [TITLE] publish?",
                    "How many papers did the authors of the paper [TITLE] publish?",
                    "How many papers did the authors of the publication [TITLE] publish?",
                    "How many publications did the authors of [TITLE] publish?",
                    "How many publications did the authors of the paper [TITLE] publish?",
                    "How many publications did the authors of the publication [TITLE] publish?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TP73",
            "query":  {
                "sparql": "SELECT (COUNT(DISTINCT ?answer) AS ?count) WHERE { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?x . ?x <https://dblp.org/rdf/schema#primaryAffiliation> ?answer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "How many different affiliations do the authors of [TITLE] have?",
                    "How many different affiliations do the authors of the paper [TITLE] have?",
                    "How many different affiliations do the authors of the publication [TITLE] have?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#primaryAffiliation>"]
            }
        },{
            "id": "TP74",
            "query":  {
                "sparql": "SELECT DISTINCT (COUNT(?answer) AS ?count) WHERE { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?x . ?answer <https://dblp.org/rdf/schema#authoredBy> ?x . ?answer <https://dblp.org/rdf/schema#yearOfPublication> [YEAR] }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "How many papers did the authors of [TITLE] publish in [YEAR]?",
                    "How many papers did the authors of the paper [TITLE] publish in [YEAR]?",
                    "How many papers did the authors of the publication [TITLE] publish in [YEAR]?",
                    "How many papers did the authors of the paper [TITLE] publish in the year [YEAR]?",
                    "How many papers did the authors of the publication [TITLE] publish in the year [YEAR]?",
                    "How many papers did the authors of the paper [TITLE] publish in the year [YEAR]?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#yearOfPublication>"]
            }
        },{
            "id": "TP75",
            "query":  {
                "sparql": "SELECT DISTINCT (COUNT(?answer) AS ?count) WHERE { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?x . ?answer <https://dblp.org/rdf/schema#authoredBy> ?x . ?answer <https://dblp.org/rdf/schema#publishedIn> [VENUE] }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "How many papers did the authors of [TITLE] publish in [VENUE]?",
                    "In [VENUE], how many papers did the authors of [TITLE] publish?",
                    "How many publications did the authors of the paper [TITLE] publish in [VENUE]?",
                    "In [VENUE], how many publications did the authors of the paper [TITLE] publish?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#publishedIn>"]
            }
        }],
        "SUPERLATIVE": [{
            "id": "TP81",
            "query":  {
                "sparql": "SELECT (GROUP_CONCAT(?answer; separator=', ') AS ?answer) ?count WHERE { SELECT DISTINCT ?answer (COUNT(?answer) AS ?count) WHERE { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?x . ?x <https://dblp.org/rdf/schema#primaryAffiliation> ?answer } GROUP BY ?answer } ORDER BY DESC(?count) LIMIT 1"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Where are most of the authors of [TITLE] from?",
                    "Where are most of the authors of the paper [TITLE] from?",
                    "To which institution are the majority of the authors of [TITLE] affiliated to?",
                    "To which institution are the majority of the authors of the paper [TITLE] affiliated to?",
                    "What is the primary affiliation of most of the authors of [TITLE]?",
                    "What is the primary affiliation of most of the authors of the paper [TITLE]?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#primaryAffiliation>"]
            }
        },{
            "id": "TP82",
            "query":  {
                "sparql": "SELECT (GROUP_CONCAT(?answer; separator=', ') AS ?answer) ?count WHERE { SELECT DISTINCT ?answer (COUNT(?x) AS ?count) WHERE { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?answer . ?x <https://dblp.org/rdf/schema#authoredBy> ?answer } GROUP BY ?answer } ORDER BY DESC(?count) LIMIT 1"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Who has published the most papers among the authors of [TITLE]?",
                    "Who has published the most papers among the authors of the paper [TITLE]?",
                    "Among the authors of [TITLE], who has published the most papers?",
                    "Among the authors of the paper [TITLE], who has published the most papers?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TP83",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer (MIN(xsd:integer(?y) AS ?y) WHERE { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?answer . ?x <https://dblp.org/rdf/schema#authoredBy> ?answer . ?x <https://dblp.org/rdf/schema#yearOfPublication> ?y }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "When were the first papers of the authors of [TITLE] published?",
                    "When were the first papers of the authors of the paper [TITLE] published?",
                    "When were the first publications of the authors of [TITLE] published?",
                    "When were the first publications of the authors of the paper [TITLE] published?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#yearOfPublication>"]
            }
        },{
            "id": "TP84",
            "query":  {
                "sparql": "SELECT (GROUP_CONCAT(?answer; separator=', ') AS ?answer) ?z WHERE { SELECT DISTINCT ?answer ?y WHERE { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?answer . ?y <https://dblp.org/rdf/schema#authoredBy> ?answer . ?y <https://dblp.org/rdf/schema#yearOfPublication> ?z } GROUP BY ?z } ORDER BY ASC(?z) LIMIT 1"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Who published the first paper among the authors of [TITLE]?",
                    "Who published the first paper among the authors of the paper [TITLE]?",
                    "Among the authors of [TITLE], who published the first paper?",
                    "Among the authors of the paper [TITLE], who published the first paper?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#yearOfPublication>"]
            }
        },{
            "id": "TP85",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?p1 <https://dblp.org/rdf/schema#yearOfPublication> ?x . ?p2 <https://dblp.org/rdf/schema#yearOfPublication> ?y . BIND(IF(?x < ?y, ?p1, ?p2) AS ?answer) }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Between [TITLE] and [OTHER_TITLE], which paper was published earlier?",
                    "Between [TITLE] and [OTHER_TITLE], which one was published first?",
                    "Which one was published first, [TITLE] or [OTHER_TITLE]?",
                    "Which paper was published earlier, [TITLE] or [OTHER_TITLE]?"
                ],
                "entities": ["?p1", "?p2"],
                "relations": ["<https://dblp.org/rdf/schema#yearOfPublication>"]
            }
        },{
            "id": "TP86",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?p1 <https://dblp.org/rdf/schema#numberOfCreators> ?x . ?p2 <https://dblp.org/rdf/schema#numberOfCreators> ?y . BIND(IF(?x > ?y, ?p1, ?p1) AS ?answer) }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Between [TITLE] and [OTHER_TITLE], which paper has more authors?",
                    "Between [TITLE] and [OTHER_TITLE], which one has more number of authors?",
                    "Between [TITLE] and [OTHER_TITLE], which paper has more number of co-authors?",
                    "Which one has more number of co-authors, [TITLE] or [OTHER_TITLE]?",
                    "Which one has more number of authors, [TITLE] or [OTHER_TITLE]?"
                ],
                "entities": ["?p1", "?p2"],
                "relations": ["<https://dblp.org/rdf/schema#numberOfCreators>"]
            }
        }],
        "DISAMBIGUATION": [{
            "id": "TP91",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?answer . ?p1 <https://dblp.org/rdf/schema#publishedIn> [VENUE] . ?p1 <https://dblp.org/rdf/schema#yearOfPublication> [YEAR] }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Who are the authors that published papers about [KEYWORD] in [VENUE] in [YEAR]?",
                    "Who are the authors that published research papers about [KEYWORD] in [VENUE] in the year [YEAR]?",
                    "In [VENUE] in [YEAR], who are the authors that published papers about [KEYWORD]?",
                    "In [VENUE] in the year [YEAR], who are the authors that published research papers about [KEYWORD]?",
                    "In [YEAR] in [VENUE], who are the authors that published papers about [KEYWORD]?",
                    "In the year [YEAR] in [VENUE], who are the authors that published research papers about [KEYWORD]?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#publishedIn>", "<https://dblp.org/rdf/schema#yearOfPublication>", "<https://dblp.org/rdf/schema#authoredBy>"] 
            }
        },{
            "id": "TP92",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?p1 <https://dblp.org/rdf/schema#publishedIn> [VENUE] . ?p1 <https://dblp.org/rdf/schema#yearOfPublication> [YEAR] . ?p1 <https://dblp.org/rdf/schema#title> ?answer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "What are the titles of the papers on [KEYWORD] that were published in [VENUE] in [YEAR]?",
                    "What are the titles of the research papers on [KEYWORD] that were published in [VENUE] in the year [YEAR]?",
                    "In [VENUE] in [YEAR], what are the titles of the papers on [KEYWORD]?",
                    "In [VENUE] in the year [YEAR], what are the titles of the research papers on [KEYWORD]?",
                    "In [YEAR] in [VENUE], what are the titles of the papers on [KEYWORD]?",
                    "In the year [YEAR] in [VENUE], what are the titles of the research papers on [KEYWORD]?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#publishedIn>", "<https://dblp.org/rdf/schema#yearOfPublication>", "<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#title>"]
            }
        },{
            "id": "TP93",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?x . ?x <https://dblp.org/rdf/schema#primaryAffiliation> [AFFILIATION] . ?p1 <https://dblp.org/rdf/schema#yearOfPublication> ?answer }",
            },
            "question": {
                "language": "en",
                "strings": [
                    "When was the paper [KEYWORD] by [AFFILIATION] published?",
                    "In what year was the paper [KEYWORD] by [AFFILIATION] published?",
                    "When was the research paper [KEYWORD] by [AFFILIATION] published?",
                    "Mention the year in which the paper [KEYWORD] by [AFFILIATION] was published?"
                ],
                "entities": ["?p1","[AFFILIATION]"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#primaryAffiliation>", "<https://dblp.org/rdf/schema#yearOfPublication>"]
            }
        }]
    },
    "CREATOR": {
        "SINGLE_FACT": [{
            "id": "TC01",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?answer <https://dblp.org/rdf/schema#authoredBy> ?c1 }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "What are the papers written by [CREATOR_NAME]?",
                    "What are the publications written by the author [CREATOR_NAME]?",
                    "What are the papers written by the author named [CREATOR_NAME]?",
                    "What are the research papers written by the person named [CREATOR_NAME]?",
                    "What are the papers written by the person [CREATOR_NAME]?",
                    "Which publications did [CREATOR_NAME] write?",
                    "Which papers did the author [CREATOR_NAME] write?",
                    "Which publications did [CREATOR_NAME] author?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TC02",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?c1 <https://dblp.org/rdf/schema#primaryAffiliation> ?answer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "What is the primary affiliation of [CREATOR_NAME]?",
                    "What is the primary affiliation of the author [CREATOR_NAME]?",
                    "[CREATOR_NAME] is primarily affiliated to which institution?",
                    "The author [CREATOR_NAME] is primarily affiliated to which institution?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#primaryAffiliation>"]
            }
        },{
            "id": "TC03",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?c1 <https://dblp.org/rdf/schema#orcid> ?answer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "What is the ORCID of [CREATOR_NAME]?",
                    "What is the ORCID of the author [CREATOR_NAME]?",
                    "What is the ORCID of the person [CREATOR_NAME]?",
                    "What is the ORCID of the researcher [CREATOR_NAME]?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#orcid>"]
            }
        },{
            "id": "TC04",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?c1 <https://dblp.org/rdf/schema#affiliation> ?answer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Which institutions has [CREATOR_NAME] been affiliated to?",
                    "Which institutions has the author [CREATOR_NAME] been affiliated to?",
                    "What are the institutions that [CREATOR_NAME] has been affiliated to?",
                    "To which institutions has [CREATOR_NAME] been affiliated?",
                    "To which institutions has the author [CREATOR_NAME] been affiliated?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#affiliation>"]
            }
        },{
            "id": "TC05",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?c1 <https://dblp.org/rdf/schema#homepage> ?answer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "What is the homepage of [CREATOR_NAME]?",
                    "What is the homepage of the author [CREATOR_NAME]?",
                    "What is the homepage of the person [CREATOR_NAME]?",
                    "What is the homepage of the researcher [CREATOR_NAME]?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#homepage>"]
            }
        }],
        "MULTI_FACT": [{
            "id": "TC11",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?x <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?x <https://dblp.org/rdf/schema#publishedIn> ?answer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "What are the venues in which [CREATOR_NAME] published?",
                    "What are the venues in which the author [CREATOR_NAME] published?",
                    "Which venues has [CREATOR_NAME] published in?",
                    "Which venues has [CREATOR_NAME] published in?",
                    "In which conferences or journals has [CREATOR_NAME] published papers?",
                    "In which conferences or journals has the author [CREATOR_NAME] published papers?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#publishedIn>"]
            }
        },{
            "id": "TC12",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?answer <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?answer <https://dblp.org/rdf/schema#authoredBy> ?c2 }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "What are the papers written by [CREATOR_NAME] and [OTHER_CREATOR_NAME] together?",
                    "What are the publications written by the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] in collaboration?",
                    "Which papers did [CREATOR_NAME] and [OTHER_CREATOR_NAME] write together?",
                    "What publications did [CREATOR_NAME] and [OTHER_CREATOR_NAME] author together?",
                    "Which papers did the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] co-write?"
                ],
                "entities": ["?c1", "?c2"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TC13",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?answer <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?answer <https://dblp.org/rdf/schema#publishedIn> [VENUE] }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Which papers did [CREATOR_NAME] publish in [VENUE]?",
                    "Which papers did the author [CREATOR_NAME] publish in [VENUE]?",
                    "What publications did [CREATOR_NAME] publish in [VENUE]?",
                    "In [VENUE], which papers did [CREATOR_NAME] publish?",
                    "In [VENUE], which papers did the author [CREATOR_NAME] publish?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#publishedIn>"]
            }
        },{
            "id": "TC14",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?x <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?x <https://dblp.org/rdf/schema#authoredBy> ?answer FILTER(?answer != ?c1) }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Who are the co-authors of [CREATOR_NAME]?",
                    "Who are the co-authors of the author [CREATOR_NAME]?",
                    "With which other authors has [CREATOR_NAME] co-authored papers?",
                    "With which other authors has the author [CREATOR_NAME] co-authored papers?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TC15",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?answer <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?answer <https://dblp.org/rdf/schema#yearOfPublication> ?y FILTER(?y > YEAR(NOW())-[DURATION]) }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Which papers did [CREATOR_NAME] publish in the last [DURATION] years?",
                    "Which papers did the author [CREATOR_NAME] publish in the last [DURATION] years?",
                    "Which papers did [CREATOR_NAME] publish in the last [DURATION] years?",
                    "Which papers did the author [CREATOR_NAME] publish in the last [DURATION] years?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#yearOfPublication>"]
            }
        },{
            "id": "TC16",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?answer <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?answer <https://dblp.org/rdf/schema#authoredBy> ?y . ?y <https://dblp.org/rdf/schema#primaryAffiliation> [AFFILIATION] }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "What research papers did [CREATOR_NAME] publish with the author affiliated to [AFFILIATION]?",
                    "What research papers did the author [CREATOR_NAME] publish with the author affiliated to [AFFILIATION]?",
                    "Which papers did [CREATOR_NAME] publish with the author affiliated to [AFFILIATION]?",
                    "Which papers did the author [CREATOR_NAME] write with the author from [AFFILIATION]?",
                    "Which publications did [CREATOR_NAME] write with the author from [AFFILIATION]?"
                ],
                "entities": ["?c1", "[AFFILIATION]"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#primaryAffiliation>"]
            }
        }],
        "DOUBLE_INTENT": [{
            "id": "TC21",
            "query":  {
                "sparql": "SELECT DISTINCT ?firstanswer ?secondanswer WHERE { ?firstanswer <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?firstanswer <https://dblp.org/rdf/schema#yearOfPublication> ?secondanswer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Which papers did author [CREATOR_NAME] publish and in which year?",
                    "What are the papers published by [CREATOR_NAME] and in which year?",
                    "Which publications did [CREATOR_NAME] author and in which year?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#yearOfPublication>"]
            }
        },{
            "id": "TC22",
            "query":  {
                "sparql": "SELECT DISTINCT ?firstanswer ?secondanswer WHERE { ?x <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?x <https://dblp.org/rdf/schema#authoredBy> ?firstanswer FILTER(?firstanswer != ?c1) . ?firstanswer <https://dblp.org/rdf/schema#primaryAffiliation> ?secondanswer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Who are the co-authors of [CREATOR_NAME] and where are they affiliated?",
                    "Who are the co-authors of the author [CREATOR_NAME] and where are they affiliated?",
                    "With which other authors has [CREATOR_NAME] co-authored papers and where are they affiliated?",
                    "With which other authors has the author [CREATOR_NAME] co-authored papers and where are they affiliated?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#primaryAffiliation>"]
            }
        },{
            "id": "TC23",
            "query":  {
                "sparql": "SELECT DISTINCT ?firstanswer ?secondanswer WHERE { ?x <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?x <https://dblp.org/rdf/schema#yearOfPublication> ?y . FILTER(?y > YEAR(NOW())-[DURATION]) . ?x <https://dblp.org/rdf/schema#authoredBy> ?firstanswer FILTER(?firstanswer != ?c1) . ?firstanswer <https://dblp.org/rdf/schema#primaryAffiliation> ?secondanswer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Who are the co-authors of [CREATOR_NAME] in the last [DURATION] years and where are they affiliated?",
                    "Who are the co-authors of the author [CREATOR_NAME] in the last [DURATION] years and where are they affiliated?",
                    "With which other authors has [CREATOR_NAME] co-authored papers in the last [DURATION] years and where are they affiliated?",
                    "With which other authors has the author [CREATOR_NAME] co-authored papers in the last [DURATION] years and where are they affiliated?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#yearOfPublication>"]
            }
        },{
            "id": "TC24",
            "query":  {
                "sparql": "SELECT DISTINCT ?firstanswer ?secondanswer WHERE { ?x <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?x <https://dblp.org/rdf/schema#publishedIn> ?firstanswer . ?x <https://dblp.org/rdf/schema#title> ?secondanswer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "In which venues did [CREATOR_NAME] publish papers and what are the titles of these papers?",
                    "In which venues did the author [CREATOR_NAME] publish papers and what are the titles of these papers?",
                    "What are the titles of the papers that [CREATOR_NAME] published and in which venues?",
                    "What are the titles of the papers that the author [CREATOR_NAME] published and in which venues?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#publishedIn>", "<https://dblp.org/rdf/schema#title>"]
            }
        },{
            "id": "TC25",
            "query":  {
                "sparql": "SELECT DISTINCT ?firstanswer ?secondanswer WHERE { ?x <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?x <https://dblp.org/rdf/schema#yearOfPublication> ?y . FILTER(?y > YEAR(NOW())-[DURATION]) . ?x <https://dblp.org/rdf/schema#publishedIn> ?firstanswer . ?x <https://dblp.org/rdf/schema#title> ?secondanswer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "In which venues did [CREATOR_NAME] publish papers in the last [DURATION] years and what are the titles of these papers?",
                    "In which venues did the author [CREATOR_NAME] publish papers in the last [DURATION] years and what are the titles of these papers?",
                    "What are the titles of the papers that [CREATOR_NAME] published in the last [DURATION] years and in which venues?",
                    "What are the titles of the papers that the author [CREATOR_NAME] published in the last [DURATION] years and in which venues?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#yearOfPublication>", "<https://dblp.org/rdf/schema#publishedIn>", "<https://dblp.org/rdf/schema#title>"]
            }
        }],
        "BOOLEAN": [{
            "id": "TC31",
            "query":  {
                "sparql": "ASK { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?c1 }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Did [CREATOR_NAME] publish the paper [TITLE]?",
                    "Did the author [CREATOR_NAME] publish the paper [TITLE]?",
                    "Did [CREATOR_NAME] publish the paper [TITLE]?",
                    "Was the paper [TITLE] published by [CREATOR_NAME]?",
                    "Was the paper [TITLE] published by the author [CREATOR_NAME]?",
                    "Was the paper [TITLE] published by the person [CREATOR_NAME]?",
                    "Was the paper [TITLE] published by the person named [CREATOR_NAME]?"
                ],
                "entities": ["?c1", "?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TC32",
            "query":  {
                "sparql": "ASK { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?p1 <https://dblp.org/rdf/schema#authoredBy> ?c2 }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Did [CREATOR_NAME] and [OTHER_CREATOR_NAME] co-author the paper [TITLE]?",
                    "Did the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] co-author the paper [TITLE]?",
                    "Was the paper [TITLE] co-authored by [CREATOR_NAME] and [OTHER_CREATOR_NAME]?",
                    "Was the paper [TITLE] co-authored by the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME]?",
                    "Have [CREATOR_NAME] and [OTHER_CREATOR_NAME] co-authored the paper [TITLE]?"
                ],
                "entities": ["?c1", "?c2", "?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TC33",
            "query":  {
                "sparql": "ASK { ?x <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?x <https://dblp.org/rdf/schema#publishedIn> [VENUE] }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Did [CREATOR_NAME] publish the paper [TITLE] in [VENUE]?",
                    "Did the author [CREATOR_NAME] publish the paper [TITLE] in [VENUE]?",
                    "Was the paper [TITLE] published by [CREATOR_NAME] in [VENUE]?",
                    "Has [CREATOR_NAME] published the paper [TITLE] in [VENUE]?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#publishedIn>"]
            }
        },{
            "id": "TC34",
            "query":  {
                "sparql": "ASK { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?p1 <https://dblp.org/rdf/schema#yearOfPublication> ?y . FILTER(?y > YEAR(NOW())-[DURATION]) }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Did [CREATOR_NAME] publish the paper [TITLE] in the last [DURATION] years?",
                    "Did the author [CREATOR_NAME] publish the paper [TITLE] in the last [DURATION] years?",
                    "Did [CREATOR_NAME] publish the paper [TITLE] in the last [DURATION] years?",
                    "Did the author [CREATOR_NAME] publish the paper [TITLE] in the last [DURATION] years?"
                ],
                "entities": ["?c1", "?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#yearOfPublication>"]
            }
        },{
            "id": "TC35",
            "query":  {
                "sparql": "ASK { ?x <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?x <https://dblp.org/rdf/schema#yearOfPublication> ?y . FILTER(?y > YEAR(NOW())-[DURATION]) . ?x <https://dblp.org/rdf/schema#publishedIn> [VENUE] }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Did [CREATOR_NAME] publish in [VENUE] in the last [DURATION] years?",
                    "Did the author [CREATOR_NAME] publish in [VENUE] in the last [DURATION] years?",
                    "Has [CREATOR_NAME] published in [VENUE] in the last [DURATION] years?",
                    "Has the author [CREATOR_NAME] published in [VENUE] in the last [DURATION] years?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#yearOfPublication>", "<https://dblp.org/rdf/schema#publishedIn>"]
            }
        },{
            "id": "TC36",
            "query":  {
                "sparql": "ASK { ?c1 <https://dblp.org/rdf/schema#orcid> ?x }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Does [CREATOR_NAME] have an ORCID?",
                    "Does the author [CREATOR_NAME] have an ORCID?",
                    "Does the person [CREATOR_NAME] have an ORCID?",
                    "Does the person named [CREATOR_NAME] have an ORCID?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#orcid>"]
            }
        }],
        "NEGATION": [{
            "id": "TC41",
            "query":  {
                "sparql": "ASK { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?c1 FILTER NOT EXISTS { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?c1 } }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Did [CREATOR_NAME] not publish the paper [TITLE]?",
                    "Did the author [CREATOR_NAME] not publish the paper [TITLE]?",
                    "Didn't [CREATOR_NAME] publish the paper [TITLE]?",
                    "Has the paper [TITLE] not been published by [CREATOR_NAME]?",
                    "Has [CREATOR_NAME] not published the paper [TITLE]?",
                    "Was the paper [TITLE] not published by [CREATOR_NAME]?",
                    "Wasn't the paper [TITLE] not published by the author [CREATOR_NAME]?",
                    "Was the paper [TITLE] not published by the person [CREATOR_NAME]?",
                    "Wasn't the paper [TITLE] not published by the person named [CREATOR_NAME]?"
                ],
                "entities": ["?c1", "?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TC42",
            "query":  {
                "sparql": "ASK { ?x <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?x <https://dblp.org/rdf/schema#publishedIn> [VENUE] FILTER NOT EXISTS { ?x <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?x <https://dblp.org/rdf/schema#publishedIn> [VENUE] } }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Did [CREATOR_NAME] not publish in [VENUE]?",
                    "Did the author [CREATOR_NAME] not publish in [VENUE]?",
                    "Has [CREATOR_NAME] not published in [VENUE]?",
                    "Has the author [CREATOR_NAME] not published in [VENUE]?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#publishedIn>"]
            }
        },{
            "id": "TC43",
            "query":  {
                "sparql": "ASK { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?p1 <https://dblp.org/rdf/schema#authoredBy> ?c2 FILTER NOT EXISTS { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?p1 <https://dblp.org/rdf/schema#authoredBy> ?c2 } }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Did [CREATOR_NAME] and [OTHER_CREATOR_NAME] not co-author the paper [TITLE]?",
                    "Did the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] not co-author the paper [TITLE]?",
                    "Was the paper [TITLE] not co-authored by [CREATOR_NAME] and [OTHER_CREATOR_NAME]?",
                    "Was the paper [TITLE] not co-authored by the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME]?",
                    "Have [CREATOR_NAME] and [OTHER_CREATOR_NAME] not co-authored the paper [TITLE]?"
                ],
                "entities": ["?c1", "?c2", "?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TC44",
            "query":  {
                "sparql": "ASK { ?x <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?x <https://dblp.org/rdf/schema#yearOfPublication> ?y . FILTER(?y > YEAR(NOW())-[DURATION]) . ?x <https://dblp.org/rdf/schema#publishedIn> [VENUE] FILTER NOT EXISTS { ?x <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?x <https://dblp.org/rdf/schema#yearOfPublication> ?y . FILTER(?y > YEAR(NOW())-[DURATION]) . ?x <https://dblp.org/rdf/schema#publishedIn> [VENUE] } }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Did [CREATOR_NAME] not publish in [VENUE] in the last [DURATION] years?",
                    "Did the author [CREATOR_NAME] not publish in [VENUE] in the last [DURATION] years?",
                    "Has [CREATOR_NAME] not published in [VENUE] in the last [DURATION] years?",
                    "Has the author [CREATOR_NAME] not published in [VENUE] in the last [DURATION] years?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#publishedIn>"]
            }
        }],
        "DOUBLE_NEGATION": [{
            "id": "TC51",
            "query":  {
                "sparql": "ASK { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?c1 }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Didn't [CREATOR_NAME] not publish the paper [TITLE]?",
                    "Has the paper [TITLE] not not been published by [CREATOR_NAME]?",
                    "Has [CREATOR_NAME] not not published the paper [TITLE]?",
                    "Was the paper [TITLE] not not published by [CREATOR_NAME]?",
                    "Wasn't the paper [TITLE] not not published by the author [CREATOR_NAME]?",
                    "Was the paper [TITLE] not not published by the person [CREATOR_NAME]?",
                    "Wasn't the paper [TITLE] not not published by the person named [CREATOR_NAME]?"
                ],
                "entities": ["?c1", "?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TC52",
            "query":  {
                "sparql": "ASK { ?x <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?x <https://dblp.org/rdf/schema#yearOfPublication> [YEAR] }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Did [CREATOR_NAME] not not publish in [YEAR]?",
                    "Did the author [CREATOR_NAME] not not publish in [YEAR]?",
                    "Has [CREATOR_NAME] not not published in [YEAR]?",
                    "Has the author [CREATOR_NAME] not not published in [YEAR]?",
                    "Didn't [CREATOR_NAME] not publish in [YEAR]?",
                    "Hasn't [CREATOR_NAME] not published in [YEAR]?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#yearOfPublication>"]
            }
        },{
            "id": "TC53",
            "query":  {
                "sparql": "ASK { ?x <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?x <https://dblp.org/rdf/schema#authoredBy> ?c2 }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Didn't [CREATOR_NAME] and [OTHER_CREATOR_NAME] not co-author a paper?",
                    "Did the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] not not co-author a paper?",
                    "Was a paper not not co-authored by [CREATOR_NAME] and [OTHER_CREATOR_NAME]?",
                    "Have [CREATOR_NAME] and [OTHER_CREATOR_NAME] not not co-authored a paper?"
                ],
                "entities": ["?c1", "?c2"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TC54",
            "query":  {
                "sparql": "ASK { ?c1 <https://dblp.org/rdf/schema#primaryAffiliation> [AFFILIATION] }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Isn't [CREATOR_NAME] not affiliated with [AFFILIATION]?",
                    "Is [CREATOR_NAME] not not affiliated with [AFFILIATION]?",
                    "Doesn't [CREATOR_NAME] not work at [AFFILIATION]?",
                    "Does [CREATOR_NAME] not not have [AFFILIATION] as the primary affiliation?"
                ],
                "entities": ["?c1", "[AFFILIATION]"],
                "relations": ["<https://dblp.org/rdf/schema#primaryAffiliation>"]
            }
        }],
        "UNION": [{
            "id": "TC61",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { { ?answer <https://dblp.org/rdf/schema#authoredBy> ?c1 } UNION { ?answer <https://dblp.org/rdf/schema#authoredBy> ?c2 } }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "What are the papers that [CREATOR_NAME] and [OTHER_CREATOR_NAME] published?",
                    "What are the papers that the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] published?",
                    "What are all the papers that [CREATOR_NAME] and [OTHER_CREATOR_NAME] published?",
                    "What are the papers that the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] published?",
                    "What are all the papers that the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] published?"
                ],
                "entities": ["?c1", "?c2"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TC62",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { { ?answer <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?answer <https://dblp.org/rdf/schema#publishedIn> [VENUE] } UNION { ?answer <https://dblp.org/rdf/schema#authoredBy> ?c2 . ?answer <https://dblp.org/rdf/schema#publishedIn> [VENUE] } }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "What are the papers that [CREATOR_NAME] and [OTHER_CREATOR_NAME] published in [VENUE]?",
                    "What are the papers that the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] published in [VENUE]?",
                    "What are all the papers that [CREATOR_NAME] and [OTHER_CREATOR_NAME] published in [VENUE]?",
                    "What are the papers that the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] published in [VENUE]?",
                    "What are all the papers that the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] published in [VENUE]?"
                ],
                "entities": ["?c1", "?c2"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#publishedIn>"]
            }
        },{
            "id": "TC63",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?answer <https://dblp.org/rdf/schema#authoredBy> ?c1 { ?answer <https://dblp.org/rdf/schema#publishedIn> [VENUE] } UNION { ?answer <https://dblp.org/rdf/schema#publishedIn> [OTHER_VENUE] } }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "What papers did [CREATOR_NAME] publish in [VENUE] and [OTHER_VENUE]?",
                    "What papers did the author [CREATOR_NAME] publish in [VENUE] and [OTHER_VENUE]?",
                    "What publications did [CREATOR_NAME] publish in [VENUE] and [OTHER_VENUE]?",
                    "What publications did the author [CREATOR_NAME] publish in [VENUE] and [OTHER_VENUE]?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#publishedIn>"]
            }
        }],
        "COUNT": [{
            "id": "TC71",
            "query":  {
                "sparql": "SELECT (COUNT(DISTINCT ?answer) AS ?count) WHERE { ?answer <https://dblp.org/rdf/schema#authoredBy> ?c1 }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "How many papers has [CREATOR_NAME] published?",
                    "How many papers has the author [CREATOR_NAME] published?",
                    "How many publications has [CREATOR_NAME] published?",
                    "How many publications has the author [CREATOR_NAME] published?",
                    "How many research papers has [CREATOR_NAME] published?",
                    "How many research papers has the author [CREATOR_NAME] published?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TC72",
            "query":  {
                "sparql": "SELECT (COUNT(DISTINCT ?answer) AS ?count) WHERE { ?answer <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?answer <https://dblp.org/rdf/schema#publishedIn> [VENUE] }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "How many papers has [CREATOR_NAME] published in [VENUE]?",
                    "How many papers has the author [CREATOR_NAME] published in [VENUE]?",
                    "How many publications has [CREATOR_NAME] published in [VENUE]?",
                    "In [VENUE], how many papers has [CREATOR_NAME] published?",
                    "In [VENUE], how many papers has the author [CREATOR_NAME] published?",
                    "In [VENUE], how many publications has [CREATOR_NAME] published?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#publishedIn>"]
            }
        },{
            "id": "TC73",
            "query":  {
                "sparql": "SELECT (COUNT(DISTINCT ?answer) AS ?count) WHERE { ?x <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?x <https://dblp.org/rdf/schema#authoredBy> ?answer FILTER(?answer != ?c1) }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "How many co-authors does [CREATOR_NAME] have?",
                    "How many co-authors does the author [CREATOR_NAME] have?",
                    "With how many other authors has [CREATOR_NAME] co-authored papers?",
                    "With how many other authors has the author [CREATOR_NAME] co-authored papers?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TC74",
            "query":  {
                "sparql": "SELECT (COUNT(DISTINCT ?answer) AS ?count) WHERE { ?answer <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?answer <https://dblp.org/rdf/schema#authoredBy> ?c2 }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "How many papers did [CREATOR_NAME] and [OTHER_CREATOR_NAME] write together?",
                    "How many publications did [CREATOR_NAME] and [OTHER_CREATOR_NAME] author together?",
                    "How many papers did the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] co-write?",
                    "How many research papers did [CREATOR_NAME] and [OTHER_CREATOR_NAME] write together?",
                    "How many research papers did the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] co-write?"
                ],
                "entities": ["?c1", "?c2"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TC75",
            "query":  {
                "sparql": "SELECT (AVG(?count) AS ?answer) { SELECT (COUNT(?y) AS ?count) WHERE { ?x <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?x <https://dblp.org/rdf/schema#yearOfPublication> ?y } GROUP BY ?y }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "What is the average number of papers published by [CREATOR_NAME] per year?",
                    "What is the average number of papers published by the author [CREATOR_NAME] per year?",
                    "What is the average number of publications published by [CREATOR_NAME] per year?",
                    "What is the average number of publications published by the author [CREATOR_NAME] per year?",
                    "What is the average number of research papers published by [CREATOR_NAME] per year?",
                    "What is the average number of research papers published by the author [CREATOR_NAME] per year?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TC76",
            "query":  {
                "sparql": "SELECT (AVG(?count) AS ?answer) { SELECT (COUNT(?y) AS ?count) WHERE { ?x <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?x <https://dblp.org/rdf/schema#numberOfCreators> ?y } GROUP BY ?y }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "What is the average number of co-authors for papers published by [CREATOR_NAME]?",
                    "What is the average number of co-authors for papers published by the author [CREATOR_NAME]?",
                    "What is the average number of co-authors for publications published by [CREATOR_NAME]?",
                    "What is the average number of co-authors for publications published by the author [CREATOR_NAME]?",
                    "What is the average number of co-authors for research papers published by [CREATOR_NAME]?",
                    "What is the average number of co-authors for research papers published by the author [CREATOR_NAME]?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        }],
        "SUPERLATIVE": [{
            "id": "TC81",
            "query":  {
                "sparql": "SELECT (GROUP_CONCAT(?answer; separator=', ') AS ?answer) ?count WHERE { SELECT DISTINCT ?answer (COUNT(?answer) AS ?count) WHERE { ?x <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?x <https://dblp.org/rdf/schema#yearOfPublication> ?answer } GROUP BY ?answer } ORDER BY DESC(?count) LIMIT 1"
            },
            "question": {
                "language": "en",
                "strings": [
                    "In which year did [CREATOR_NAME] publish the most papers?",
                    "In which year did the author [CREATOR_NAME] publish the most papers?",
                    "In which year did [CREATOR_NAME] publish the most publications?",
                    "In which year did the author [CREATOR_NAME] publish the most publications?",
                    "In which year did [CREATOR_NAME] publish the most research papers?",
                    "In which year did the author [CREATOR_NAME] publish the most research papers?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TC82",
            "query":  {
                "sparql": "SELECT (GROUP_CONCAT(?answer; separator=', ') AS ?answer) ?count WHERE { SELECT DISTINCT ?answer (COUNT(?answer) AS ?count) WHERE { ?x <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?x <https://dblp.org/rdf/schema#yearOfPublication> ?answer } GROUP BY ?answer } ORDER BY ASC(?count) LIMIT 1"
            },
            "question": {
                "language": "en",
                "strings": [
                    "In which year did [CREATOR_NAME] publish the least papers and how many?",
                    "In which year did the author [CREATOR_NAME] publish the least papers and how many?",
                    "In which year did [CREATOR_NAME] publish the least publications and how many?",
                    "In which year did the author [CREATOR_NAME] publish the least publications?",
                    "In which year did [CREATOR_NAME] publish the least research papers?",
                    "In which year did the author [CREATOR_NAME] publish the least research papers?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TC83",
            "query":  {
                "sparql": "SELECT (GROUP_CONCAT(?answer; separator=', ') AS ?answer) ?count WHERE { SELECT DISTINCT ?answer (COUNT(?answer) AS ?count) WHERE { ?x <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?x <https://dblp.org/rdf/schema#publishedIn> ?answer } GROUP BY ?answer } ORDER BY DESC(?count) LIMIT 1"
            },
            "question": {
                "language": "en",
                "strings": [
                    "In which venue did [CREATOR_NAME] publish the most papers and how many?",
                    "In which venue did the author [CREATOR_NAME] publish the most papers?",
                    "In which venue did [CREATOR_NAME] publish the most publications and how many?",
                    "[CREATOR_NAME] published the most papers in which venue and how many?",
                    "[CREATOR_NAME] published the most publications in which venue?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TC84",
            "query":  {
                "sparql": "SELECT (GROUP_CONCAT(?answer; separator=', ') AS ?answer) ?count WHERE { SELECT DISTINCT ?answer (COUNT(?answer) AS ?count) WHERE { ?x <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?x <https://dblp.org/rdf/schema#authoredBy> ?answer FILTER(?answer != ?c1)} GROUP BY ?answer } ORDER BY DESC(?count) LIMIT 1"
            },
            "question": {
                "language": "en",
                "strings": [
                    "With which author does [CREATOR_NAME] has the most papers and how many?",
                    "With which author does [CREATOR_NAME] has the most publications and how many?",
                    "With which author does [CREATOR_NAME] has the most research papers?",
                    "Who is the most common co-author of [CREATOR_NAME] and how many papers do they have together?",
                    "Who is the most frequent co-author of [CREATOR_NAME] and how many publications do they have together?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TC85",
            "query":  {
                "sparql": "SELECT DISTINCT MIN(xsd:integer(?answer)) AS ?answer WHERE { ?x <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?x <https://dblp.org/rdf/schema#yearOfPublication> ?answer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "When was the first paper by [CREATOR_NAME] published?",
                    "When was the first publication by [CREATOR_NAME] published?",
                    "When was the first research paper by [CREATOR_NAME] published?",
                    "In which year was the first paper by [CREATOR_NAME] published?",
                    "In which year did [CREATOR_NAME] publish their first paper?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TC86",
            "query":  {
                "sparql": "SELECT DISTINCT MAX(xsd:integer(?answer)) AS ?answer WHERE { ?x <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?x <https://dblp.org/rdf/schema#yearOfPublication> ?answer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "When was the last paper by [CREATOR_NAME] published?",
                    "When was the last publication by [CREATOR_NAME] published?",
                    "When was the last research paper by [CREATOR_NAME] published?",
                    "In which year was the last paper by [CREATOR_NAME] published?",
                    "In which year did [CREATOR_NAME] publish their last paper?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        }],
        "DISAMBIGUATION": [{
            "id": "TC91",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?answer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Which author named [PARTIAL_CREATOR_NAME] published the paper on [KEYWORD]?",
                    "Who is the author named [PARTIAL_CREATOR_NAME] who published the paper about [KEYWORD]?",
                    "Which author published the paper on [KEYWORD] and has the name [PARTIAL_CREATOR_NAME]?",
                    "Which author with the name [PARTIAL_CREATOR_NAME] published the paper about [KEYWORD]?"
                ],
                "entities": ["?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>"]
            }
        },{
            "id": "TC92",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?answer <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?answer <https://dblp.org/rdf/schema#publishedIn> [VENUE] }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "Which paper on [KEYWORD] was published by [PARTIAL_CREATOR_NAME] in [VENUE]?",
                    "Which paper on [KEYWORD] was published by the author [PARTIAL_CREATOR_NAME] in [VENUE]?",
                    "Which publication on [KEYWORD] was published by [PARTIAL_CREATOR_NAME] in [VENUE]?",
                    "Which publication on [KEYWORD] was published by the author [PARTIAL_CREATOR_NAME] in [VENUE]?",
                    "Which research paper on [KEYWORD] was published by [PARTIAL_CREATOR_NAME] in [VENUE]?",
                    "Which research paper on [KEYWORD] was published by the author [PARTIAL_CREATOR_NAME] in [VENUE]?"
                ],
                "entities": ["?c1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#publishedIn>"]
            }
        },{
            "id": "TC93",
            "query":  {
                "sparql": "SELECT DISTINCT ?answer WHERE { ?p1 <https://dblp.org/rdf/schema#authoredBy> ?c1 . ?p1 <https://dblp.org/rdf/schema#publishedIn> ?answer }"
            },
            "question": {
                "language": "en",
                "strings": [
                    "In which venue did [PARTIAL_CREATOR_NAME] publish the paper about [KEYWORD]?",
                    "In which venue did [PARTIAL_CREATOR_NAME] author the publication on [KEYWORD]?",
                    "In which venue did [PARTIAL_CREATOR_NAME] write the research papers about [KEYWORD]?",
                    "[PARTIAL_CREATOR_NAME] published the paper on [KEYWORD] in which venue?",
                    "[PARTIAL_CREATOR_NAME] published the publication on [KEYWORD] in which venue?",
                    "[PARTIAL_CREATOR_NAME] published the research paper on [KEYWORD] in which venue?"
                ],
                "entities": ["?c1", "?p1"],
                "relations": ["<https://dblp.org/rdf/schema#authoredBy>", "<https://dblp.org/rdf/schema#publishedIn>"]
            }
        }]
    }
}
