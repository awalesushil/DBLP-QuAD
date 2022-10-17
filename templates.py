"""
    A collection of SPARQL templates grouped by query types
"""

templates = {
    "PUBLICATION": {
        "FACTOID": [{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:title [TITLE] . ?x dblp:authoredBy ?answer }",
            "questions": [
                "Who wrote the paper [TITLE]?",
                "Who authored the paper [TITLE]?",
                "Who is the author of the paper [TITLE]?",
                "Who is the author of [TITLE]?",
                "Who wrote [TITLE]?",
                "Who authored [TITLE]?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:title [TITLE] . ?x dblp:authoredBy ?y . ?y dblp:primaryAffiliation ?answer }",
            "questions": [
                "What are the primary affiliations of the authors of [TITLE]?",
                "What are the primary affiliations of the authors of the paper [TITLE]?",
                "Where are the authors of [TITLE] from?",
                "Where are the authors of the paper [TITLE] from?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:title [TITLE] . ?x dblp:yearOfPublication ?answer }",
            "questions": [
                "When was [TITLE] published?",
                "When was the paper [TITLE] published?",
                "What year was [TITLE] published?",
                "What year was the paper [TITLE] published?",
                "In what year was [TITLE] published?",
                "In what year was the paper [TITLE] published?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:title [TITLE] . ?x dblp:publishedIn ?answer }",
            "questions": [
                "Where was [TITLE] published?",
                "Where was the paper [TITLE] published?",
                "What is the venue of the paper [TITLE]?",
                "What is the venue of the publication [TITLE]?",
                "In what venue was [TITLE] published?",
                "In which venue was the paper [TITLE] published?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:title [TITLE] . ?x dblp:authoredBy ?y . ?z dblp:authoredBy ?y . ?z dblp:title ?answer FILTER (?answer != [TITLE]) }",
            "questions": [
                "Which other papers were published by the authors of [TITLE]?",
                "Which other papers were published by the authors of the paper [TITLE]?",
                "What other papers were published by the authors of the publication [TITLE]?",
                "What other papers were published by the authors of the paper [TITLE]?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:title [TITLE] . ?x dblp:authoredBy ?y . ?z dblp:authoredBy ?y . ?z dblp:publishedIn ?answer FILTER (?answer != [TITLE]) }",
            "questions": [
                "What are the venues of the other papers published by the authors of [TITLE]?",
                "What are the venues of the other papers published by the authors of the paper [TITLE]?",
                "What are the venues of the other papers published by the authors of the publication [TITLE]?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:title [TITLE] . ?x dblp:authoredBy ?y . ?y dblp:primaryAffiliation ?answer }",
            "questions": [
                "What are the affiliations of the authors of [TITLE]?",
                "What are the affiliations of the authors of the paper [TITLE]?",
                "What are the affiliations of the authors of the publication [TITLE]?",
                "What are the affiliations of the authors of the paper [TITLE]?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:title [TITLE] . ?x dblp:doi ?answer }",
            "questions": [
                "What is the DOI of the paper [TITLE]?",
                "What is the DOI of [TITLE]?",
                "What is the DOI of the publication [TITLE]?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:title [TITLE] . ?x dblp:bibtexType ?answer }",
            "questions": [
                "What is the type of the paper [TITLE]?",
                "What is the type of [TITLE]?",
                "What is the type of the publication [TITLE]?",
                "What type of publication is [TITLE]?"
            ]
        },{
            "query": "SELECT ?answer WHERE { ?x dblp:title [TITLE] . ?x dblp:numberOfCreators ?answer }",
            "questions": [
                "How many authors does [TITLE] have?",
                "How many authors wrote the paper [TITLE]?",
                "How many authors does the publication [TITLE] have?"
            ]
        },],
        "DOUBLE_INTENT": [{
            "query": "SELECT DISTINCT ?firstanswer ?secondanswer WHERE { ?x dblp:title [TITLE] . ?x dblp:publishedIn ?firstanswer . ?x dblp:yearOfPublication ?secondanswer }",
            "questions": [
                "Where was [TITLE] published and when?",
                "Where was the paper [TITLE] published and when?",
                "Where was the publication [TITLE] published and when?",
                "Where was the paper [TITLE] published and in what year?",
                "Where was the publication [TITLE] published and in what year?",
                "In what venue was [TITLE] published and when?",
                "In what year was [TITLE] published and in what venue?",
                "In what venue was the paper [TITLE] published and when?",
                "In what year was the paper [TITLE] published and in what venue?"
            ]
        },{
            "query": "SELECT DISTINCT ?firstanswer ?secondanswer WHERE { ?x dblp:title [TITLE] . ?x dblp:authoredBy ?y . ?y dblp:primaryFullCreatorName ?firstanswer . ?x dblp:primaryAffiliation ?secondanswer }",
            "questions": [
                "Who are the authors of [TITLE] and where are they from?",
                "Who are the authors of the paper [TITLE] and where are they from?",
                "Who are the authors of the publication [TITLE] and where are they from?",
                "Who are the authors of the paper [TITLE] and what are their affiliations?",
                "Who are the authors of the publication [TITLE] and what are their affiliations?"
            ]
        },{
            "query": "SELECT DISTINCT ?firstanswer ?secondanswer WHERE { ?x dblp:title [TITLE] . ?x dblp:authoredBy ?y . ?y dblp:primaryFullCreatorName ?firstanswer . ?z dblp:authoredBy ?y . ?z dblp:title ?secondanswer FILTER (?secondanswer != [TITLE]) }",
            "questions": [
                "Who are the authors of [TITLE] and which other papers did they publish?",
                "Who are the authors of the paper [TITLE] and which other papers did they publish?",
                "Who are the authors of the publication [TITLE] and which other papers did they publish?",
                "Who are the authors of the paper [TITLE] and what other papers did they publish?",
                "Who are the authors of the publication [TITLE] and what other papers did they publish?"
            ]
        },{
            "query": "SELECT DISTINCT ?firstanswer ?secondanswer WHERE { ?x dblp:title [TITLE] . ?x dblp:authoredBy ?y . ?y dblp:primaryFullCreatorName ?firstanswer . ?z dblp:authoredBy ?y . ?z dblp:publishedIn ?secondanswer FILTER (?secondanswer != [TITLE]) }",
            "questions": [
                "Who are the authors of [TITLE] and what are the venues of the other papers they published?",
                "Who are the authors of the paper [TITLE] and what are the venues of the other papers they published?",
                "Who are the authors of the publication [TITLE] and what are the venues of the other papers they published?",
                "Who are the authors of the paper [TITLE] and what are the venues of the other papers they published?",
                "Who are the authors of the publication [TITLE] and what are the venues of the other papers they published?"
            ]
        }],
        "ASK": [{
            "query": "ASK { ?x dblp:title [TITLE] }",
            "questions": [
                "Does [TITLE] exist?",
                "Does the paper [TITLE] exist?",
                "Does the publication [TITLE] exist?"
            ]
        },{
            "questions": [
                "Does [TITLE] not exist?",
                "Does the paper [TITLE] not exist?",
                "Does the publication [TITLE] not exist?"
            ],
            "query": "ASK { ?x dblp:title [TITLE] }"
        },{
            "query": "ASK { ?x dblp:title [TITLE] . ?x purl:bibtexType [TYPE] }",
            "questions": [
                "Is [TITLE] a [TYPE] publication?",
                "Is the publication [TITLE] a [TYPE] paper?"
            ]
        },{
            "query": "ASK { ?x dblp:title [TITLE] . ?x dblp:authoredBy ?y . ?y dblp:primaryAffiliation [AFFILIATION] }",
            "questions": [
                "Do the authors of [TITLE] have [AFFILIATION] as their primary affiliation?",
                "Do the authors of the paper [TITLE] have [AFFILIATION] as their primary affiliation?",
                "Do the authors of the publication [TITLE] have [AFFILIATION] as their primary affiliation?"
            ]
        },{
            "query": "ASK { ?x dblp:title [TITLE] . ?x dblp:yearOfPublication [YEAR] }",
            "questions": [
                "Was [TITLE] published in [YEAR]?",
                "Was the paper [TITLE] published in [YEAR]?",
                "Was the publication [TITLE] published in [YEAR]?",
                "Was [TITLE] published in the year [YEAR]?",
                "Was the paper [TITLE] published in the year [YEAR]?",
                "Was the publication [TITLE] published in the year [YEAR]?"
            ]
        },{
            "query": "ASK { ?x dblp:title [TITLE] . ?x dblp:publishedIn [VENUE] }",
            "questions": [
                "Was [TITLE] published in [VENUE]?",
                "Was the paper [TITLE] published in [VENUE]?",
                "Was the publication [TITLE] published in [VENUE]?",
                "Was [TITLE] published in the venue [VENUE]?",
                "Was the paper [TITLE] published in the venue [VENUE]?",
                "Was the publication [TITLE] published in the venue [VENUE]?"
            ]
        },{
            "query": "ASK { ?x dblp:title [TITLE] . ?x dblp:authoredBy ?y . ?z dblp:authoredBy ?y . ?z dblp:title ?a FILTER (?a != [TITLE]) . ?z dblp:title [OTHER_TITLE] }",
            "questions": [
                "Did the authors of [TITLE] also publish [OTHER_TITLE]?",
                "Did the authors of the paper [TITLE] also publish [OTHER_TITLE]?",
                "Did the authors of the publication [TITLE] also publish [OTHER_TITLE]?",
                "Did the authors of [TITLE] also publish the paper [OTHER_TITLE]?",
                "Did the authors of the paper [TITLE] also publish the paper [OTHER_TITLE]?",
                "Did the authors of the publication [TITLE] also publish the paper [OTHER_TITLE]?",
                "Did the authors of [TITLE] also publish the publication [OTHER_TITLE]?",
                "Did the authors of the paper [TITLE] also publish the publication [OTHER_TITLE]?",
                "Did the authors of the publication [TITLE] also publish the publication [OTHER_TITLE]?"
            ]
        },{
            "query": "ASK { ?x dblp:title [TITLE] . ?x dblp:authoredBy ?y . ?z dblp:authoredBy ?y . ?z dblp:title ?a FILTER (?a != [TITLE]) . ?z dblp:yearOfPublication [YEAR] }",
            "questions": [
                "Did the authors of [TITLE] also publish a paper in [YEAR]?",
                "Did the authors of the paper [TITLE] also publish a paper in [YEAR]?",
                "Did the authors of the publication [TITLE] also publish a paper in [YEAR]?",
                "Did the authors of [TITLE] also publish a publication in [YEAR]?",
                "Did the authors of the paper [TITLE] also publish a publication in [YEAR]?",
                "Did the authors of the publication [TITLE] also publish a publication in [YEAR]?"
            ]
        },{
            "query": "ASK { ?x dblp:title [TITLE] . ?x dblp:authoredBy ?y . ?z dblp:authoredBy ?y . ?z dblp:title ?a FILTER (?a != [TITLE]) . ?z dblp:publishedIn [VENUE] }",
            "questions": [
                "Did the authors of [TITLE] also publish a paper in [VENUE]?",
                "Did the authors of the paper [TITLE] also publish a paper in [VENUE]?",
                "Did the authors of the publication [TITLE] also publish a paper in [VENUE]?",
                "Did the authors of [TITLE] also publish a publication in [VENUE]?",
                "Did the authors of the paper [TITLE] also publish a publication in [VENUE]?",
                "Did the authors of the publication [TITLE] also publish a publication in [VENUE]?",
                "Did the authors of [TITLE] also publish a paper in the venue [VENUE]?"
            ]
        },{
            "query": "ASK { ?x dblp:title [TITLE] . ?x dblp:doi ?y }",
            "questions": [
                "Does [TITLE] have a DOI?",
                "Does the paper [TITLE] have a DOI?",
                "Does the publication [TITLE] have a DOI?"
            ]
        }],
        "UNION": [{
            "query": "SELECT DISTINCT ?answer WHERE { { ?x dblp:title [TITLE] . ?x dblp:authoredBy ?z . ?z dblp:primaryFullCreatorName ?answer } UNION { ?y dblp:title [OTHER_CREATOR_NAME] . ?y dblp:authoredBy ?z . ?z dblp:primaryFullCreatorName ?answer } }",
            "questions": [
                "Who are the authors of [TITLE] and [OTHER_TITLE]?",
                "Who are the authors of the paper [TITLE] and [OTHER_TITLE]?",
                "Who are the authors of the publication [TITLE] and [OTHER_TITLE]?",
                "Who are the authors of the paper [TITLE] and the paper [OTHER_TITLE]?",
                "Who are the authors of the paper [TITLE] and the publication [OTHER_TITLE]?",
                "Who are the authors of the publication [TITLE] and the paper [OTHER_TITLE]?",
                "Who are the authors of the publication [TITLE] and the publication [OTHER_TITLE]?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { { ?x dblp:title [TITLE] . ?x dblp:yearOfPublication ?answer } UNION { ?y dblp:title [OTHER_TITLE] . ?y dblp:yearOfPublication ?answer } }",
            "questions": [
                "When were [TITLE] and [OTHER_TITLE] published?",
                "When were the papers [TITLE] and [OTHER_TITLE] published?",
                "When were the publications [TITLE] and [OTHER_TITLE] published?",
                "When were the papers [TITLE] and [OTHER_TITLE] published?",
                "When were the papers [TITLE] and [OTHER_TITLE] published?",
                "When were the publications [TITLE] and [OTHER_TITLE] published?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { { ?x dblp:title [TITLE] . ?x dblp:publishedIn ?answer } UNION { ?y dblp:title [OTHER_TITLE] . ?y dblp:publishedIn ?answer } }",
            "questions": [
                "Where were [TITLE] and [OTHER_TITLE] published?",
                "Where were the papers [TITLE] and [OTHER_TITLE] published?",
                "Where were the publications [TITLE] and [OTHER_TITLE] published?",
                "Where were the papers [TITLE] and [OTHER_TITLE] published?",
                "Where were the papers [TITLE] and [OTHER_TITLE] published?",
                "Where were the publications [TITLE] and [OTHER_TITLE] published?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { { ?x dblp:title [TITLE] . ?x dblp:doi ?answer } UNION { ?y dblp:title [OTHER_TITLE] . ?y dblp:doi ?answer } }",
            "questions": [
                "What are the DOIs of [TITLE] and [OTHER_TITLE]?",
                "What are the DOIs of the papers [TITLE] and [OTHER_TITLE]?",
                "What are the DOIs of the publications [TITLE] and [OTHER_TITLE]?"
            ]
        }],
        "AGGREGATION": [{
            "query": "SELECT (COUNT(DISTINCT ?answer) AS ?count) WHERE { ?x dblp:title [TITLE] . ?x dblp:authoredBy ?answer . ?answer dblp:primaryAffiliation [AFFILIATION] }",
            "questions": [
                "How many authors of [TITLE] have [AFFILIATION] as their primary affiliation?",
                "How many authors of the paper [TITLE] have [AFFILIATION] as their primary affiliation?",
                "How many authors of the publication [TITLE] have [AFFILIATION] as their primary affiliation?"
            ]
        },{
            "query": "SELECT (COUNT(DISTINCT ?answer) AS ?count) WHERE { ?x dblp:title [TITLE] . ?x dblp:authoredBy ?y . ?z dblp:authoredBy ?y . ?z dblp:title ?a FILTER (?a != [TITLE]) . ?z dblp:title ?answer }",
            "questions": [
                "How many papers did the authors of [TITLE] publish?",
                "How many papers did the authors of the paper [TITLE] publish?",
                "How many papers did the authors of the publication [TITLE] publish?",
                "How many publications did the authors of [TITLE] publish?",
                "How many publications did the authors of the paper [TITLE] publish?",
                "How many publications did the authors of the publication [TITLE] publish?"
            ]
        },{
            "query": "SELECT (COUNT(DISTINCT ?answer) AS ?count) WHERE { ?x dblp:title [TITLE] . ?x dblp:authoredBy ?y . ?y dblp:primaryAffiliation ?answer }",
            "questions": [
                "How many different affiliations do the authors of [TITLE] have?",
                "How many different affiliations do the authors of the paper [TITLE] have?",
                "How many different affiliations do the authors of the publication [TITLE] have?"
            ]
        },{
            "query": "SELECT DISTINCT (COUNT(?answer) AS ?count) WHERE { ?x dblp:title [TITLE] . ?x dblp:authoredBy ?y . ?z dblp:authoredBy ?y . ?z dblp:yearOfPublication [YEAR] . ?z dblp:title ?answer }",
            "questions": [
                "How many papers did the authors of [TITLE] publish in [YEAR]?",
                "How many papers did the authors of the paper [TITLE] publish in [YEAR]?",
                "How many papers did the authors of the publication [TITLE] publish in [YEAR]?",
                "How many papers did the authors of the paper [TITLE] publish in the year [YEAR]?",
                "How many papers did the authors of the publication [TITLE] publish in the year [YEAR]?",
                "How many papers did the authors of the paper [TITLE] publish in the year [YEAR]?"
            ]
        },{
            "query": "SELECT (GROUP_CONCAT(?answer; separator=', ') AS ?answer) ?count WHERE { SELECT DISTINCT ?answer (COUNT(?answer) AS ?count) WHERE { ?x dblp:title [TITLE] . ?x dblp:authoredBy ?y . ?y dblp:primaryAffiliation ?answer } GROUP BY ?answer } ORDER BY DESC(?count) LIMIT 1",
            "questions": [
                "From where are most of the authors of [TITLE] from?",
                "From where are most of the authors of the paper [TITLE] from?",
                "Where are the majority of the authors of [TITLE] affiliated to?",
                "Where are the majority of the authors of the paper [TITLE] affiliated to?",
                "What is the primary affiliation of most of the authors of [TITLE]?",
                "What is the primary affiliation of most of the authors of the paper [TITLE]?"
            ]
        }],
        "DISAMBIGUATION": [{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:title ?t . FILTER(CONTAINS(LCASE(?t), [KEYWORD])) . ?x dblp:publishedIn ?v . FILTER(CONTAINS(LCASE(?v), [VENUE])) . ?x dblp:year ?y . FILTER(?y = [YEAR]) . ?x dblp:authoredBy ?y . ?y dblp:primaryFullCreatorName ?answer . }",
            "questions": [
                "Who are the authors that published papers about [KEYWORD] in [VENUE] in [YEAR]?",
                "Who are the authors that published research papers about [KEYWORD] in [VENUE] in the year [YEAR]?",
                "In [VENUE] in [YEAR], who are the authors that published papers about [KEYWORD]?",
                "In [VENUE] in the year [YEAR], who are the authors that published research papers about [KEYWORD]?",
                "In [YEAR] in [VENUE], who are the authors that published papers about [KEYWORD]?",
                "In the year [YEAR] in [VENUE], who are the authors that published research papers about [KEYWORD]?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:title ?answer . FILTER(CONTAINS(LCASE(?answer), [KEYWORD])) . ?x dblp:publishedIn ?v . FILTER(CONTAINS(LCASE(?v), [VENUE])) . ?x dblp:year ?y . FILTER(?y = [YEAR]) }",
            "questions": [
                "What are the titles of the papers on [KEYWORD] that were published in [VENUE] in [YEAR]?",
                "What are the titles of the research papers on [KEYWORD] that were published in [VENUE] in the year [YEAR]?",
                "In [VENUE] in [YEAR], what are the titles of the papers on [KEYWORD]?",
                "In [VENUE] in the year [YEAR], what are the titles of the research papers on [KEYWORD]?",
                "In [YEAR] in [VENUE], what are the titles of the papers on [KEYWORD]?",
                "In the year [YEAR] in [VENUE], what are the titles of the research papers on [KEYWORD]?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:title ?t . FILTER(CONTAINS(LCASE(?t), [KEYWORD])) . ?x dblp:year ?y . FILTER(?y = [YEAR]) . ?x dblp:authoredBy ?y . ?y dblp:primaryFullCreatorName ?answer . }",
            "questions": [
                "Who are the authors that published papers about [KEYWORD] in [YEAR]?",
                "Who are the authors that published research papers about [KEYWORD] in the year [YEAR]?",
                "In [YEAR], who are the authors that published papers about [KEYWORD]?",
                "In the year [YEAR], who are the authors that published research papers about [KEYWORD]?"
            ]
        }],
        "COMPARISON": [{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:title [TITLE] . ?x dblp:yearOfPublication ?y . ?z dblp:title [OTHER_TITLE] . ?z dblp:yearOfPublication ?w . BIND(IF(?y < ?w, [TITLE], [OTHER_TITLE]) AS ?answer) }",
            "questions": [
                "Between [TITLE] and [OTHER_TITLE], which one was published earlier?",
                "Between [TITLE] and [OTHER_TITLE], which one was published first?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:title [TITLE] . ?x dblp:numberOfCreators ?y . ?z dblp:title [OTHER_TITLE] . ?z dblp:numberOfCreators ?w . BIND(IF(?y > ?w, [TITLE], [OTHER_TITLE]) AS ?answer) }",
            "questions": [
                "Between [TITLE] and [OTHER_TITLE], which one has more authors?",
                "Between [TITLE] and [OTHER_TITLE], which one has more number of authors?",
                "Between [TITLE] and [OTHER_TITLE], which one has more number of co-authors?"
            ]
        }]
    },
    "CREATOR": {
        "FACTOID": [{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:title ?answer }",
            "questions": [
                "What are the papers written by [CREATOR_NAME]?",
                "What are the publications written by the author [CREATOR_NAME]?",
                "What are the papers written by the author named [CREATOR_NAME]?",
                "What are the research papers written by the person named [CREATOR_NAME]?",
                "What are the papers written by the person [CREATOR_NAME]?",
                "Which publications did [CREATOR_NAME] write?",
                "Which papers did the author [CREATOR_NAME] write?",
                "Which publications did [CREATOR_NAME] author?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:publishedIn ?answer }",
            "questions": [
                "What are the venues in which [CREATOR_NAME] published?",
                "What are the venues in which the author [CREATOR_NAME] published?",
                "Which venues has [CREATOR_NAME] published in?",
                "Which venues has [CREATOR_NAME] published in?",
                "In which conferences or journals has [CREATOR_NAME] published papers?",
                "In which conferences or journals has the author [CREATOR_NAME] published papers?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:primaryFullCreatorName [OTHER_CREATOR_NAME] . ?z dblp:authoredBy ?x . ?z dblp:authoredBy ?y . ?z dblp:title ?answer }",
            "questions": [
                "What are the papers written by [CREATOR_NAME] and [OTHER_CREATOR_NAME] together?",
                "What are the publications written by the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] in collaboration?",
                "Which papers did [CREATOR_NAME] and [OTHER_CREATOR_NAME] write together?",
                "What publications did [CREATOR_NAME] and [OTHER_CREATOR_NAME] author together?"
                "Which papers did the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] co-write?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:publishedIn [VENUE] . ?y dblp:title ?answer }",
            "questions": [
                "Which papers did [CREATOR_NAME] publish in [VENUE]?",
                "Which papers did the author [CREATOR_NAME] publish in [VENUE]?",
                "What publications did [CREATOR_NAME] publish in [VENUE]?",
                "In [VENUE], what papers did [CREATOR_NAME] publish?",
                "In [VENUE], what papers did the author [CREATOR_NAME] publish?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:primaryFullCreatorName [OTHER_CREATOR_NAME] . ?z dblp:authoredBy ?x . ?z dblp:authoredBy ?y . ?z dblp:publishedIn [VENUE] . ?z dblp:title ?answer }",
            "questions": [
                "Which papers did [CREATOR_NAME] and [OTHER_CREATOR_NAME] publish in collaboration in [VENUE]?",
                "Which papers did the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] publish together in [VENUE]?",
                "What publications did [CREATOR_NAME] and [OTHER_CREATOR_NAME] publish together in [VENUE]?",
                "In [VENUE], what papers did [CREATOR_NAME] and [OTHER_CREATOR_NAME] co-publish?",
                "In [VENUE], what papers did the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] co-publish?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?z dblp:authoredBy ?y . ?z dblp:primaryFullCreatorName ?answer FILTER(?answer != [CREATOR_NAME]) }",
            "questions": [
                "Who are the co-authors of [CREATOR_NAME]?",
                "Who are the co-authors of the author [CREATOR_NAME]?",
                "With which other authors has [CREATOR_NAME] co-authored papers?",
                "With which other authors has the author [CREATOR_NAME] co-authored papers?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:yearOfPublication ?z . FILTER(?z > YEAR(NOW())-[DURATION]) . ?y dblp:title ?answer }",
            "questions": [
                "Which papers did [CREATOR_NAME] publish in the last [DURATION] years?",
                "Which papers did the author [CREATOR_NAME] publish in the last [DURATION] years?",
                "Which papers did [CREATOR_NAME] publish in the last [DURATION] years?",
                "Which papers did the author [CREATOR_NAME] publish in the last [DURATION] years?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:yearOfPublication ?z . FILTER(?z > YEAR(NOW())-[DURATION]) . ?y dblp:publishedIn ?answer }",
            "questions": [
                "In which conferences or journals did [CREATOR_NAME] publish papers in the last [DURATION] years?",
                "In which conferences or journals did the author [CREATOR_NAME] publish papers in the last [DURATION] years?",
                "In which venues did [CREATOR_NAME] publish papers in the last [DURATION] years?",
                "In which venues did the author [CREATOR_NAME] publish papers in the last [DURATION] years?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:affiliation [AFFILIATION] . ?y dblp:title ?answer }",
            "questions": [
                "What research papers did [CREATOR_NAME] publish with the author affiliated to [AFFILIATION]?",
                "What research papers did the author [CREATOR_NAME] publish with the author affiliated to [AFFILIATION]?",
                "Which papers did [CREATOR_NAME] publish with the author affiliated to [AFFILIATION]?",
                "Which papers did the author [CREATOR_NAME] write with the author from [AFFILIATION]?",
                "Which publications did [CREATOR_NAME] write with the author from [AFFILIATION]?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?x dblp:orcid ?answer }",
            "questions": [
                "What is the ORCID of [CREATOR_NAME]?",
                "What is the ORCID of the author [CREATOR_NAME]?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?x dblp:website ?answer }",
            "questions": [
                "What is the website of [CREATOR_NAME]?",
                "What is the website of the author [CREATOR_NAME]?"
            ]
        }],
        "DOUBLE_INTENT": [{
            "query": "SELECT DISTINCT ?firstanswer ?secondanswer WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:title ?firstanswer . ?y dblp:yearOfPublication ?secondanswer }",
            "questions": [
                "Which papers did author [CREATOR_NAME] publish and in which year?",
                "What are the papers published by [CREATOR_NAME] and in which year?",
                "Which publications did [CREATOR_NAME] author and in which year?"
            ]
        },{
            "query": "SELECT DISTINCT ?firstanswer ?secondanswer WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:authoredBy ?z . ?z dblp:primaryFullCreatorName ?firstanswer FILTER(?firstanswer != [CREATOR_NAME]) . ?z dblp:primaryAffiliation ?secondanswer }",
            "questions": [
                "Who are the co-authors of [CREATOR_NAME] and where are they affiliated?",
                "Who are the co-authors of the author [CREATOR_NAME] and where are they affiliated?",
                "With which other authors has [CREATOR_NAME] co-authored papers and where are they affiliated?",
                "With which other authors has the author [CREATOR_NAME] co-authored papers and where are they affiliated?"
            ]
        },{
            "query": "SELECT DISTINCT ?firstanswer ?secondanswer WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:yearOfPublication ?z . FILTER(?z > YEAR(NOW())-[YEAR]) . ?y dblp:authoredBy ?a . ?a dblp:primaryFullCreatorName ?firstanswer FILTER(?firstanswer != [CREATOR_NAME]) . ?a dblp:primaryAffiliation ?secondanswer }",
            "questions": [
                "Who are the co-authors of [CREATOR_NAME] in the last [YEAR] years and where are they affiliated?",
                "Who are the co-authors of the author [CREATOR_NAME] in the last [YEAR] years and where are they affiliated?",
                "With which other authors has [CREATOR_NAME] co-authored papers in the last [YEAR] years and where are they affiliated?",
                "With which other authors has the author [CREATOR_NAME] co-authored papers in the last [YEAR] years and where are they affiliated?"
            ]
        },{
            "query": "SELECT DISTINCT ?firstanswer ?secondanswer WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:publishedIn ?firstanswer . ?y dblp:title ?secondanswer }",
            "questions": [
                "In which venues did [CREATOR_NAME] publish papers and what are the titles of these papers?",
                "In which venues did the author [CREATOR_NAME] publish papers and what are the titles of these papers?",
                "What are the titles of the papers that [CREATOR_NAME] published and in which venues?",
                "What are the titles of the papers that the author [CREATOR_NAME] published and in which venues?"
            ]
        },{
            "query": "SELECT DISTINCT ?firstanswer ?secondanswer WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:yearOfPublication ?z . FILTER(?z > YEAR(NOW())-[YEAR]) . ?y dblp:publishedIn ?firstanswer . ?y dblp:title ?secondanswer }",
            "questions": [
                "In which venues did [CREATOR_NAME] publish papers in the last [YEAR] years and what are the titles of these papers?",
                "In which venues did the author [CREATOR_NAME] publish papers in the last [YEAR] years and what are the titles of these papers?",
                "What are the titles of the papers that [CREATOR_NAME] published in the last [YEAR] years and in which venues?",
                "What are the titles of the papers that the author [CREATOR_NAME] published in the last [YEAR] years and in which venues?"
            ]
        }],
        "ASK": [{
            "query": "ASK { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:title [TITLE] }",
            "questions": [
                "Did [CREATOR_NAME] published the paper [TITLE]?",
                "Did the author [CREATOR_NAME] publish the paper [TITLE]?",
                "Did [CREATOR_NAME] publish the paper [TITLE]?",
                "Was the paper [TITLE] published by [CREATOR_NAME]?",
                "Was the paper [TITLE] published by the author [CREATOR_NAME]?",
                "Was the paper [TITLE] published by the person [CREATOR_NAME]?",
                "Was the paper [TITLE] published by the person named [CREATOR_NAME]?"
            ]
        },{
            "query": "ASK { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:publishedIn [VENUE] }",
            "questions": [
                "Did [CREATOR_NAME] publish in [VENUE]?",
                "Did the author [CREATOR_NAME] publish in [VENUE]?"
            ]
        },{
            "query": "ASK { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:primaryFullCreatorName [OTHER_CREATOR_NAME] . ?z dblp:authoredBy ?x . ?z dblp:authoredBy ?y . ?z dblp:title [TITLE] }",
            "questions": [
                "Did [CREATOR_NAME] and [OTHER_CREATOR_NAME] co-author the paper [TITLE]?",
                "Did the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] co-author the paper [TITLE]?",
                "Was the paper [TITLE] co-authored by [CREATOR_NAME] and [OTHER_CREATOR_NAME]?",
                "Was the paper [TITLE] co-authored by the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME]?"
            ]
        },{
            "query": "ASK { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:publishedIn [VENUE] . ?y dblp:title [TITLE] }",
            "questions": [
                "Did [CREATOR_NAME] publish the paper [TITLE] in [VENUE]?",
                "Did the author [CREATOR_NAME] publish the paper [TITLE] in [VENUE]?"
            ]
        },{
            "query": "ASK { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:yearOfPublication ?z . FILTER(?z > YEAR(NOW())-[DURATION]) . ?y dblp:title [TITLE] }",
            "questions": [
                "Did [CREATOR_NAME] publish the paper [TITLE] in the last [DURATION] years?",
                "Did the author [CREATOR_NAME] publish the paper [TITLE] in the last [DURATION] years?",
                "Did [CREATOR_NAME] publish the paper [TITLE] in the last [DURATION] years?",
                "Did the author [CREATOR_NAME] publish the paper [TITLE] in the last [DURATION] years?"
            ]
        },{
            "query": "ASK { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:yearOfPublication ?z . FILTER(?z > YEAR(NOW())-[DURATION]) . ?y dblp:publishedIn [VENUE] }",
            "questions": [
                "Did [CREATOR_NAME] publish in [VENUE] in the last [DURATION] years?",
                "Did the author [CREATOR_NAME] publish in [VENUE] in the last [DURATION] years?"
            ]
        },{
            "query": "ASK { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:yearOfPublication ?z . FILTER(?z > YEAR(NOW())-[DURATION]) . ?y dblp:publishedIn [VENUE] . ?y dblp:title [TITLE] }",
            "questions": [
                "Did [CREATOR_NAME] publish the paper [TITLE] in [VENUE] in the last [DURATION] years?",
                "Did the author [CREATOR_NAME] publish the paper [TITLE] in [VENUE] in the last [DURATION] years?"
            ]
        },{
            "query": "ASK { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?x dblp:orcid ?y }",
            "questions": [
                "Does [CREATOR_NAME] have an ORCID?",
                "Does the author [CREATOR_NAME] have an ORCID?"
            ]
        },{
            "query": "ASK { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?x dblp:website ?y }",
            "questions": [
                "Does [CREATOR_NAME] have a website?",
                "Does the author [CREATOR_NAME] have a website?"
            ]
        }],
        "UNION": [{
            "query": "SELECT DISTINCT ?answer WHERE { { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?z dblp:authoredBy ?x . ?z dblp:title ?answer } UNION { ?y dblp:primaryFullCreatorName [OTHER_CREATOR_NAME] . ?z dblp:authoredBy ?y . ?z dblp:title ?answer } }",
            "questions": [
                "What are the titles of the papers that [CREATOR_NAME] and [OTHER_CREATOR_NAME] published?",
                "What are the titles of the papers that the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] published?"
                "What are all the papers that [CREATOR_NAME] and [OTHER_CREATOR_NAME] published?",
                "What are the titles of the papers that the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] published?",
                "What are all the papers that the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] published?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?z dblp:authoredBy ?x . ?z dblp:publishedIn [VENUE] . ?z dblp:title ?answer } UNION { ?y dblp:primaryFullCreatorName [OTHER_CREATOR_NAME] . ?z dblp:authoredBy ?y . ?z dblp:publishedIn [VENUE] . ?z dblp:title ?answer } }",
            "questions": [
                "What are the titles of the papers that [CREATOR_NAME] and [OTHER_CREATOR_NAME] published in [VENUE]?",
                "What are the titles of the papers that the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] published in [VENUE]?"
                "What are all the papers that [CREATOR_NAME] and [OTHER_CREATOR_NAME] published in [VENUE]?",
                "What are the titles of the papers that the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] published in [VENUE]?",
                "What are all the papers that the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] published in [VENUE]?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?z dblp:authoredBy ?x { ?z dblp:publishedIn [VENUE] . ?z dblp:title ?answer } UNION { ?z dblp:publishedIn [OTHER_VENUE] . ?z dblp:title ?answer } }",
            "questions": [
                "What papers did [CREATOR_NAME] publish in [VENUE] and [OTHER_VENUE]?",
                "What papers did the author [CREATOR_NAME] publish in [VENUE] and [OTHER_VENUE]?",
                "What publications did [CREATOR_NAME] publish in [VENUE] and [OTHER_VENUE]?",
                "What publications did the author [CREATOR_NAME] publish in [VENUE] and [OTHER_VENUE]?"
            ] 
        }],
        "AGGREGATION": [{
            "query": "SELECT (COUNT(DISTINCT ?answer) AS ?count) WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?answer dblp:authoredBy ?x }",
            "questions": [
                "How many papers has [CREATOR_NAME] published?",
                "How many papers has the author [CREATOR_NAME] published?",
                "How many publications has [CREATOR_NAME] published?",
                "How many publications has the author [CREATOR_NAME] published?",
                "How many research papers has [CREATOR_NAME] published?",
                "How many research papers has the author [CREATOR_NAME] published?"
            ]
        },{
            "query": "SELECT (COUNT(DISTINCT ?answer) AS ?count) WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?answer dblp:authoredBy ?x . ?answer dblp:publishedIn [VENUE] }",
            "questions": [
                "How many papers has [CREATOR_NAME] published in [VENUE]?",
                "How many papers has the author [CREATOR_NAME] published in [VENUE]?",
                "How many publications has [CREATOR_NAME] published in [VENUE]?",
                "In [VENUE], how many papers has [CREATOR_NAME] published?",
                "In [VENUE], how many papers has the author [CREATOR_NAME] published?",
                "In [VENUE], how many publications has [CREATOR_NAME] published?"
            ]
        },{
            "query": "SELECT (COUNT(DISTINCT ?answer) AS ?count) WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:publishedIn ?answer }",
            "questions": [
                "How many venues has [CREATOR_NAME] published in?",
                "How many venues has the author [CREATOR_NAME] published in?",
                "In how many conferences or journals has [CREATOR_NAME] published papers?",
                "In how many conferences or journals has the author [CREATOR_NAME] published papers?"
            ]
        },{
            "query": "SELECT (COUNT(DISTINCT ?answer) AS ?count) WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:authoredBy ?z . ?z dblp:primaryFullCreatorName ?answer . FILTER(?answer != [CREATOR_NAME])}",
            "questions": [
                "How many co-authors does [CREATOR_NAME] have?",
                "How many co-authors does the author [CREATOR_NAME] have?",
                "With how many other authors has [CREATOR_NAME] co-authored papers?",
                "With how many other authors has the author [CREATOR_NAME] co-authored papers?"
            ]
        },{
            "query": "SELECT (COUNT(DISTINCT ?answer) AS ?count) WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:publishedIn [YEAR] . ?y dblp:title ?answer }",
            "questions": [
                "How many papers has [CREATOR_NAME] published in [YEAR]?",
                "How many papers has the author [CREATOR_NAME] published in [YEAR]?",
                "How many publications has [CREATOR_NAME] published in [YEAR]?",
                "In [YEAR], how many papers has [CREATOR_NAME] published?",
                "In [YEAR], how many papers has the author [CREATOR_NAME] published?",
                "In [YEAR], how many publications has [CREATOR_NAME] published?"
            ]
        },{
            "query": "SELECT (COUNT(DISTINCT ?answer) AS ?count) WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:primaryFullCreatorName [OTHER_CREATOR_NAME] . ?z dblp:authoredBy ?x . ?z dblp:authoredBy ?y . ?z dblp:title ?answer }",
            "questions": [
                "How many papers did [CREATOR_NAME] and [OTHER_CREATOR_NAME] write together?",
                "How many publications did [CREATOR_NAME] and [OTHER_CREATOR_NAME] author together?",
                "How many papers did the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] co-write?",
                "How many research papers did [CREATOR_NAME] and [OTHER_CREATOR_NAME] write together?",
                "How many research papers did the authors [CREATOR_NAME] and [OTHER_CREATOR_NAME] co-write?"
            ]
        },{
            "query": "SELECT DISTINCT MIN(xsd:integer(?answer)) AS ?answer WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:yearOfPublication ?answer }",
            "questions": [
                "When was [CREATOR_NAME]'s first paper published?",
                "When was the author [CREATOR_NAME]'s first paper published?",
                "When was [CREATOR_NAME]'s first publication published?",
                "When was the author [CREATOR_NAME]'s first publication published?",
                "In which year was [CREATOR_NAME]'s first paper published?",
                "In which year was the author [CREATOR_NAME]'s first paper published?"
            ]
        },{
            "query": "SELECT DISTINCT MAX(xsd:integer(?answer)) AS ?answer WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:yearOfPublication ?answer }",
            "questions": [
                "When was [CREATOR_NAME]'s last paper published?",
                "When was the author [CREATOR_NAME]'s last paper published?",
                "When was [CREATOR_NAME]'s last publication published?",
                "When was the author [CREATOR_NAME]'s last publication published?",
                "In which year was [CREATOR_NAME]'s last paper published?",
                "In which year was the author [CREATOR_NAME]'s last paper published?"
            ]
        },{
            "query": "SELECT (AVG(?count) AS ?answer) { SELECT (COUNT(?z) AS ?count) WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:yearOfPublication ?z } GROUP BY ?z }",
            "questions": [
                "What is the average number of papers published by [CREATOR_NAME] per year?",
                "What is the average number of papers published by the author [CREATOR_NAME] per year?",
                "What is the average number of publications published by [CREATOR_NAME] per year?",
                "What is the average number of publications published by the author [CREATOR_NAME] per year?",
                "What is the average number of research papers published by [CREATOR_NAME] per year?",
                "What is the average number of research papers published by the author [CREATOR_NAME] per year?"
            ],
        },{
            "query": "SELECT (AVG(?count) AS ?answer) { SELECT (COUNT(?z) AS ?count) WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:authoredBy ?z . ?z dblp:primaryFullCreatorName ?a . FILTER(?a != [CREATOR_NAME])} GROUP BY ?y }",
            "questions": [
                "What is the average number of co-authors for papers published by [CREATOR_NAME]?",
                "What is the average number of co-authors for papers published by the author [CREATOR_NAME]?",
                "What is the average number of co-authors for publications published by [CREATOR_NAME]?",
                "What is the average number of co-authors for publications published by the author [CREATOR_NAME]?",
                "What is the average number of co-authors for research papers published by [CREATOR_NAME]?",
                "What is the average number of co-authors for research papers published by the author [CREATOR_NAME]?"
            ],
        },{
            "query": "SELECT (GROUP_CONCAT(?answer; separator=', ') AS ?answer) ?count WHERE { SELECT DISTINCT ?answer (COUNT(?answer) AS ?count) WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:yearOfPublication ?answer } GROUP BY ?answer } ORDER BY DESC(?count) LIMIT 1",
            "questions": [
                "In which year did [CREATOR_NAME] publish the most papers?",
                "In which year did the author [CREATOR_NAME] publish the most papers?",
                "In which year did [CREATOR_NAME] publish the most publications?",
                "In which year did the author [CREATOR_NAME] publish the most publications?",
                "In which year did [CREATOR_NAME] publish the most research papers?",
                "In which year did the author [CREATOR_NAME] publish the most research papers?"
            ]
        },{
            "query": "SELECT (GROUP_CONCAT(?answer; separator=', ') AS ?answer) ?count WHERE { SELECT DISTINCT ?answer (COUNT(?answer) AS ?count) WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:yearOfPublication ?answer } GROUP BY ?answer } ORDER BY ASC(?count) LIMIT 1",
            "questions": [
                "In which year did [CREATOR_NAME] publish the least papers and how many?",
                "In which year did the author [CREATOR_NAME] publish the least papers and how many?",
                "In which year did [CREATOR_NAME] publish the least publications and how many?",
                "In which year did the author [CREATOR_NAME] publish the least publications?",
                "In which year did [CREATOR_NAME] publish the least research papers?",
                "In which year did the author [CREATOR_NAME] publish the least research papers?"
            ]
        },{
            "query": "SELECT (GROUP_CONCAT(?answer; separator=', ') AS ?answer) ?count WHERE { SELECT DISTINCT ?answer (COUNT(?answer) AS ?count) WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:publishedIn ?answer } GROUP BY ?answer } ORDER BY DESC(?count) LIMIT 1",
            "questions": [
                "In which venue did [CREATOR_NAME] publish the most papers and how many?",
                "In which venue did the author [CREATOR_NAME] publish the most papers?",
                "In which venue did [CREATOR_NAME] publish the most publications and how many?",
                "[CREATOR_NAME] published the most papers in which venue and how many?",
                "[CREATOR_NAME] published the most publications in which venue?"
            ]
        },{
            "query": "SELECT (GROUP_CONCAT(?answer; separator=', ') AS ?answer) ?count WHERE { SELECT DISTINCT ?answer (COUNT(?answer) AS ?count) WHERE { ?x dblp:primaryFullCreatorName [CREATOR_NAME] . ?y dblp:authoredBy ?x . ?y dblp:authoredBy ?z . ?z dblp:primaryFullCreatorName ?answer . FILTER(?answer != [CREATOR_NAME])} GROUP BY ?answer } ORDER BY DESC(?count) LIMIT 1",
            "questions": [
                "With which author does [CREATOR_NAME] has the most papers with and how many?",
                "With which author does [CREATOR_NAME] has the most publications with and how many?",
                "With which author does [CREATOR_NAME] has the most research papers with?",
                "What is the most common co-author of [CREATOR_NAME] and how many papers do they have together?",
                "What is the most frequent co-author of [CREATOR_NAME] and how many publications do they have together?",
                "What is the most frequent co-author of [CREATOR_NAME]?"
            ]
        }],
        "DISAMBIGUATION": [{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:primaryFullCreatorName ?y . FILTER(CONTAINS(LCASE(?y), [CREATOR_NAME])) . ?z dblp:authoredBy ?x . ?z dblp:title ?answer . FILTER(CONTAINS(LCASE(?answer), [KEYWORD])) }",
            "questions": [
                "What are the title of the papers that [PARTIAL_CREATOR_NAME] wrote about [KEYWORD]?",
                "What are the titles of the publications that [PARTIAL_CREATOR_NAME] published about [KEYWORD]?",
                "Which paper on [KEYWORD] was published by [PARTIAL_CREATOR_NAME]?",
                "Which paper on [KEYWORD] was published by the author [PARTIAL_CREATOR_NAME]?",
                "Which publication on [KEYWORD] was published by [PARTIAL_CREATOR_NAME]?",
                "Which publication on [KEYWORD] was published by the author [PARTIAL_CREATOR_NAME]?",
                "Which research paper on [KEYWORD] was published by [PARTIAL_CREATOR_NAME]?",
                "Which research paper on [KEYWORD] was published by the author [PARTIAL_CREATOR_NAME]?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:primaryFullCreatorName ?y . FILTER(CONTAINS(LCASE(?y), [CREATOR_NAME])) . ?z dblp:authoredBy ?x . ?z dblp:title ?answer . FILTER(CONTAINS(LCASE(?answer), [KEYWORD])) . ?z dblp:publishedIn ?v }",
            "questions": [
                "What are the title of the papers that [PARTIAL_CREATOR_NAME] wrote about [KEYWORD] published in [VENUE]?",
                "What are the titles of the publications that [PARTIAL_CREATOR_NAME] published about [KEYWORD] published in [VENUE]?",
                "Which paper on [KEYWORD] was published by [PARTIAL_CREATOR_NAME] in [VENUE]?",
                "Which paper on [KEYWORD] was published by the author [PARTIAL_CREATOR_NAME] in [VENUE]?",
                "Which publication on [KEYWORD] was published by [PARTIAL_CREATOR_NAME] in [VENUE]?",
                "Which publication on [KEYWORD] was published by the author [PARTIAL_CREATOR_NAME] in [VENUE]?",
                "Which research paper on [KEYWORD] was published by [PARTIAL_CREATOR_NAME] in [VENUE]?",
                "Which research paper on [KEYWORD] was published by the author [PARTIAL_CREATOR_NAME] in [VENUE]?"
            ]
        },{
            "query": "SELECT DISTINCT ?answer WHERE { ?x dblp:primaryFullCreatorName ?y . FILTER(CONTAINS(LCASE(?y), [CREATOR_NAME])) . ?z dblp:authoredBy ?x . ?z dblp:title ?t . FILTER(CONTAINS(LCASE(?t), [KEYWORD])) . ?z dblp:publishedIn ?answer }",
            "questions": [
                "In which venues did [PARTIAL_CREATOR_NAME] publish papers about [KEYWORD]?",
                "In which venues did [PARTIAL_CREATOR_NAME] publish publications about [KEYWORD]?",
                "In which venues did [PARTIAL_CREATOR_NAME] publish research papers about [KEYWORD]?",
                "[PARTIAL_CREATOR_NAME] published papers about [KEYWORD] in which venues?",
                "[PARTIAL_CREATOR_NAME] published publications about [KEYWORD] in which venues?",
                "[PARTIAL_CREATOR_NAME] published research papers about [KEYWORD] in which venues?"
            ]
        }]       
    },
    "GENERAL": {
        "AGGREGATION": [{
            "query": "SELECT DISTINCT (COUNT(?answer) AS ?count) WHERE { ?x dblp:title ?answer . FILTER CONTAINS (LCASE(?answer), [KEYWORD]) }",
            "questions": [
                "How many research papers contain the word [KEYWORD] in their title?",
                "How many papers contain the word [KEYWORD] in their title?",
                "How many publications contain the word [KEYWORD] in their title?"
            ]
        }]
    }
}