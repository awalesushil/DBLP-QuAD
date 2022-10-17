"""
    White list of valid entities and predicates for different subtasks
"""

publications = [
    "Book",
    "Inproceedings",
    "Publication",
    "Article",
    "Incollection",
    "Editorship",
    "Reference",
    "Data",
    "Informal",
    "Withdrawn"
]

creators = [
    "Person",
    "AmbiguousCreator",
    "Group",
    "Editor",
    "Creator"
]

predicates = [

    # Author related predicates
    "<https://dblp.org/rdf/schema#creatorOf>",
    "<https://dblp.org/rdf/schema#authorOf>",
    "<https://dblp.org/rdf/schema#authorBy>",
    "<https://dblp.org/rdf/schema#editorOf>",
    "<https://dblp.org/rdf/schema#numberOfCreators>",
    "<https://dblp.org/rdf/schema#coCreatorWith>",
    "<https://dblp.org/rdf/schema#coAuthorWith>",
    "<https://dblp.org/rdf/schema#coEditorWith>",
    "<https://dblp.org/rdf/schema#affiliation>",
    "<https://dblp.org/rdf/schema#primaryAffiliation>",
    "<https://dblp.org/rdf/schema#otherAffiliation>",
    "<https://dblp.org/rdf/schema#fullCreatorName>",
    "<https://dblp.org/rdf/schema#primaryFullCreatorName>",
    "<https://dblp.org/rdf/schema#otherFullCreatorName>",
    "<https://dblp.org/rdf/schema#possibleActualCreator>",
    "<https://dblp.org/rdf/schema#proxyAmbiguousCreator>",
    "<https://dblp.org/rdf/schema#orcid>",
    "<https://dblp.org/rdf/schema#wikidata>",
    "<https://dblp.org/rdf/schema#webpage>",

    # Publication related predicates
    "<https://dblp.org/rdf/schema#createdBy>",
    "<https://dblp.org/rdf/schema#authoredBy>",
    "<https://dblp.org/rdf/schema#editedBy>",
    "<https://dblp.org/rdf/schema#numberOfCreators>",
    "<https://dblp.org/rdf/schema#publishedIn>",
    "<https://dblp.org/rdf/schema#publishedBy>",
    "<https://dblp.org/rdf/schema#yearOfPublication>",
    "<https://dblp.org/rdf/schema#yearOfEvent>",
    "<https://dblp.org/rdf/schema#doi>",
    "<https://dblp.org/rdf/schema#title>",
    "<https://dblp.org/rdf/schema#bibtexType>"
]
