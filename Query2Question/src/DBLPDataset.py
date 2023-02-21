import torch
from torch.utils.data import Dataset

from utils import mask_question, mask_query


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