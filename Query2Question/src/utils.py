sparql_vocab = [
    "<s>", "</s>","https://dblp.org/pid/", "https://dblp.org/rec/journals/", "https://dblp.org/rec/conf/",
    "SELECT", "DISTINCT", "WHERE", "ASK", "FILTER", "YEAR", "NOW", "NOT", "EXISTS", "GROUP BY", "ORDER BY", 
    "ASC", "DESC", "LIMIT", "BIND", "AS", "IF", "GROUP_CONCAT", "COUNT", "separator=', '",
    "MAX", "MIN", "xsd:integer",
    "{", "}", "(", ")", ">", "<", "?answer", "?firstanswer", "?secondanswer", "?count",
    "?x", "?y", "?z", "?t", "!=",
    "https://dblp.org/rdf/schema#authoredBy",
    "https://dblp.org/rdf/schema#publishedIn",
    "https://dblp.org/rdf/schema#yearOfPublication",
    "https://dblp.org/rdf/schema#authoredBy",
    "https://dblp.org/rdf/schema#numberOfCreators",
    "https://dblp.org/rdf/schema#primaryAffiliation",
    "https://dblp.org/rdf/schema#bibtexType"
]

labels = " ".join([f"<extra_id_{idx}> {vocab}" for idx, vocab in enumerate(sparql_vocab)])
sparql_vocab_dict = {vocab: f"<extra_id_{idx}>" for idx, vocab in enumerate(sparql_vocab)}
sparql_vocab_dict_rev = {idx: vocab for vocab, idx in sparql_vocab_dict.items()}

def mask_question(sequence):
    for vocab in sparql_vocab_dict:
        if vocab in ["<",">"]:
            sequence = sequence.replace(" "+vocab+" ", " "+sparql_vocab_dict[vocab]+" ")
        else:
            sequence = sequence.replace(vocab, sparql_vocab_dict[vocab])
    return sequence


def mask_query(sequence):
    for vocab in sparql_vocab_dict:
        if vocab in ["<",">"]:
            sequence = sequence.replace(" "+vocab+" ", " "+sparql_vocab_dict[vocab]+" "+vocab+" ")
        else:
            sequence = sequence.replace(vocab, sparql_vocab_dict[vocab] + " " + vocab)
    return sequence