from torch.utils.data import DataLoader

from config import *
from DBLPDataset import DBLPDataset
from Model import Model

def main(args):
    train = DBLPDataset(DATA_DIR, split="train")
    val = DBLPDataset(DATA_DIR, split="val")
    test = DBLPDataset(DATA_DIR, split="test")

    train_loader = DataLoader(train, batch_size=TRAIN_BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val, batch_size=VAL_BATCH_SIZE, shuffle=False)
    test_loader = DataLoader(test, batch_size=TEST_BATCH_SIZE, shuffle=False)



