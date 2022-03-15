import spacy
import pandas as pd
from torchtext.legacy.data import Field, BucketIterator, TabularDataset
from sklearn.model_selection import train_test_split

train_statement = pd.read_json("data/train_statement.json")
test_statement = pd.read_json("data/test_statement.json")

def tokenize_text(text):
    return [tok.text for tok in spacy.load('en').tokenizer(text)]

statement = Field(sequential = True, use_vocab = True, tokenize = tokenize_text)

fields = {"statement": ("statement", statement)}

train_data, test_data = TabularDataset.splits(
    path = "data",
    train = "train_statement.json",
    test = "test_statement.json",
    format = "json",
    fields = fields)
