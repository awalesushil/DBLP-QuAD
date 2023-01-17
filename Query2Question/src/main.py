# Importing libraries
import os
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader, RandomSampler, SequentialSampler
import os

# Importing the T5 modules from huggingface/transformers
from transformers import AutoTokenizer, T5ForConditionalGeneration

# rich: for a better display on terminal
from rich.table import Column, Table
from rich import box
from rich.console import Console

# define a rich console logger
console = Console(record=True)

# to display dataframe in ASCII format
def display_df(df):
    """display dataframe in ASCII format"""

    console = Console()
    table = Table(
        Column("source_text", justify="center"),
        Column("target_text", justify="center"),
        title="Sample Data",
        pad_edge=False,
        box=box.ASCII,
    )

    for i, row in enumerate(df.values.tolist()):
        table.add_row(row[0], row[1])

    console.print(table)

# training logger to log training progress
training_logger = Table(
    Column("Epoch", justify="center"),
    Column("Steps", justify="center"),
    Column("Loss", justify="center"),
    title="Training Status",
    pad_edge=False,
    box=box.ASCII,
)

# Setting up the device for GPU usage
from torch import cuda
device = 'cuda' if cuda.is_available() else 'cpu'

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

def demask_query(sequence):
    sequence = sequence.replace(".", " .")
    
    for idx in sparql_vocab_dict_rev:
        sequence = sequence.replace(idx, sparql_vocab_dict_rev[idx])
    return sequence

class DBLPDataset(Dataset):
    """
        Handles DBLP Dataset
    """
    def __init__(self, dataframe, tokenizer, source_len, target_len, source_text, target_text):
        """
            Args:
                data_dir (str): Path to data directory
                tokenizer (transformers.tokenizer): Tokenizer to use
                split (str): train/val/test
        """
        self.tokenizer = tokenizer
        self.data = dataframe
        self.source_len = source_len
        self.summ_len = target_len
        self.target_text = self.data[target_text]
        self.source_text = self.data[source_text]
        
    def __len__(self):
        """
            Returns:
                length (int): Length of dataset
        """
        return len(self.target_text)
    
    def __getitem__(self, index):
        """
            Args:
                idx (int): Index of sample
            Returns:
                sample (dict): Transformed sample from the dataset
        """

        source_text = mask_question(str(self.source_text[index]))
        target_text = mask_query(str(self.target_text[index]))
        
        source = self.tokenizer.batch_encode_plus(
            [source_text],
            max_length=self.source_len,
            pad_to_max_length=True,
            truncation=True,
            padding="max_length",
            return_tensors="pt",
        )

        target = self.tokenizer.batch_encode_plus(
            [target_text],
            max_length=self.summ_len,
            pad_to_max_length=True,
            truncation=True,
            padding="max_length",
            return_tensors="pt",
        )

        source_ids = source["input_ids"].squeeze()
        source_mask = source["attention_mask"].squeeze()
        target_ids = target["input_ids"].squeeze()
        target_mask = target["attention_mask"].squeeze()

        return {
            "source_ids": source_ids.to(dtype=torch.long),
            "source_mask": source_mask.to(dtype=torch.long),
            "target_ids": target_ids.to(dtype=torch.long),
            "target_mask": target_mask.to(dtype=torch.long)
        }

def train(epoch, tokenizer, model, device, loader, optimizer):

    model.train()

    for _, data in enumerate(loader, 0):

        lm_labels = data["target_ids"].to(device, dtype = torch.long)
        lm_labels[lm_labels[:, :] == tokenizer.pad_token_id] = -100

        outputs = model(
            input_ids=data["source_ids"].to(device, dtype = torch.long),
            attention_mask=data["source_mask"].to(device, dtype = torch.long),
            decoder_attention_mask=data["target_mask"].to(device, dtype = torch.long),
            labels=lm_labels
        )

        loss = outputs[0]

        if _ % 10 == 0:
            training_logger.add_row(str(epoch), str(_), str(loss))
            console.print(training_logger)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

def validate(epoch, tokenizer, model, device, loader):
    """
    Function to evaluate model for predictions

    """
    model.eval()
    predictions = []
    actuals = []
    with torch.no_grad():
        for _, data in enumerate(loader, 0):
            y = data['target_ids'].to(device, dtype = torch.long)
            ids = data['source_ids'].to(device, dtype = torch.long)
            mask = data['source_mask'].to(device, dtype = torch.long)

            generated_ids = model.generate(
                input_ids = ids,
                attention_mask = mask, 
                max_length=512, 
                num_beams=2,
                repetition_penalty=2.5, 
                length_penalty=1.0, 
                early_stopping=True
                )
            preds = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in generated_ids]
            target = [tokenizer.decode(t, skip_special_tokens=True, clean_up_tokenization_spaces=False) for t in y]
            
            # preds = [demask_seq(pred) for pred in preds]

            if _%10==0:
                console.print(f'Completed {_}')
            
            predictions.extend(preds)
            actuals.extend(target)
    return predictions, actuals

def T5Trainer(train_df, valid_df, source_text, target_text, model_params, output_dir="./outputs/"):

    torch.manual_seed(model_params["SEED"])
    np.random.seed(model_params["SEED"])
    torch.backends.cudnn.deterministic = True

    console.log(f"""[Model]: Loading {model_params["MODEL"]}...\n""")

    tokenizer = AutoTokenizer.from_pretrained(model_params["MODEL"])
    tokenizer.add_tokens([" {"," }"," <"])

    model = T5ForConditionalGeneration.from_pretrained(model_params["MODEL"])
    model = model.to(device)

    console.log(f"[Data]: Reading data...\n")

    train_dataset = train_df[[source_text, target_text]]
    val_dataset = valid_df[[source_text, target_text]]
    
    console.print(f"TRAIN Dataset: {train_dataset.shape}")
    console.print(f"TEST Dataset: {val_dataset.shape}\n")

    training_set = DBLPDataset(
        train_dataset,
        tokenizer,
        model_params["MAX_SOURCE_TEXT_LENGTH"],
        model_params["MAX_TARGET_TEXT_LENGTH"],
        source_text,
        target_text,
    )
    val_set = DBLPDataset(
        val_dataset,
        tokenizer,
        model_params["MAX_SOURCE_TEXT_LENGTH"],
        model_params["MAX_TARGET_TEXT_LENGTH"],
        source_text,
        target_text,
    )

    # Defining the parameters for creation of dataloaders
    train_params = {
        "batch_size": model_params["TRAIN_BATCH_SIZE"],
        "shuffle": True,
        "num_workers": 0,
    }

    val_params = {
        "batch_size": model_params["VALID_BATCH_SIZE"],
        "shuffle": False,
        "num_workers": 0,
    }

    # Creation of Dataloaders for testing and validation. This will be used down for training and validation stage for the model.
    training_loader = DataLoader(training_set, **train_params)
    val_loader = DataLoader(val_set, **val_params)

    # Defining the optimizer that will be used to tune the weights of the network in the training session.
    optimizer = torch.optim.Adam(
        params=model.parameters(), lr=model_params["LEARNING_RATE"]
    )

    # Training loop
    console.log(f"[Initiating Fine Tuning]...\n")

    for epoch in range(model_params["TRAIN_EPOCHS"]):
        train(epoch, tokenizer, model, device, training_loader, optimizer)
    
    console.log(f"[Saving Model]...\n")
    # Saving the model after training
    path = os.path.join(output_dir, "model_files")
    model.save_pretrained(path)
    tokenizer.save_pretrained(path)

    # evaluating test dataset
    console.log(f"[Initiating Validation]...\n")
    for epoch in range(model_params["VAL_EPOCHS"]):
        predictions, actuals = validate(epoch, tokenizer, model, device, val_loader)
        final_df = pd.DataFrame({"Generated Text": predictions, "Actual Text": actuals})
        final_df.to_csv(os.path.join(output_dir, "predictions.csv"))

    console.save_text(os.path.join(output_dir, "logs.txt"))

    console.log(f"[Validation Completed.]\n")
    console.print(
        f"""[Model] Model saved @ {os.path.join(output_dir, "model_files")}\n"""
    )
    console.print(
        f"""[Validation] Generation on Validation data saved @ {os.path.join(output_dir,'predictions.csv')}\n"""
    )
    console.print(f"""[Logs] Logs saved @ {os.path.join(output_dir,'logs.txt')}\n""")

# let's define model parameters specific to T5
model_params = {
    "MODEL": "t5-base",  # model_type: t5-base/t5-large
    "TRAIN_BATCH_SIZE": 4,  # training batch size
    "VALID_BATCH_SIZE": 4,  # validation batch size
    "TRAIN_EPOCHS": 5,  # number of training epochs
    "VAL_EPOCHS": 1,  # number of validation epochs
    "LEARNING_RATE": 1e-4,  # learning rate
    "MAX_SOURCE_TEXT_LENGTH": 512,  # max length of source text
    "MAX_TARGET_TEXT_LENGTH": 512,  # max length of target text
    "SEED": 42,  # set seed for reproducibility
}

import re
import json
import pandas as pd

data = {
    "train": [],
    "valid": []
}

for each in ["train", "valid"]:
    with open("../data/"+each+"_questions.json","r") as f:
        raw = json.load(f)

    entity_group = re.compile(r"<(\S+)>")

    data = [{
        "id": d["id"],
        "question": d["question"]["string"],
        "entities": entity_group.sub(r"\1", " ".join(d["entities"])),
        "relations": entity_group.sub(r"\1", " ".join(d["relations"])),
        "sparql": entity_group.sub(r"\1", d["query"]["sparql"])
        } for d in raw["questions"]]

    df = pd.DataFrame(data)

    prefix = "parse text to SPARQL query: " 
    df["question"] = prefix + df["question"] + " [SEP] " + df["entities"] + " [SEP] " + df["relations"]
    df["sparql"] = "<s> " + df["sparql"] + " </s>"

    data[each] = df

train_df = data["train"]
valid_df = data["valid"]

T5Trainer(
    train_dataframe=train_df,
    valid_dataframe=valid_df,
    source_text="question",
    target_text="sparql",
    model_params=model_params,
    output_dir="outputs"
)