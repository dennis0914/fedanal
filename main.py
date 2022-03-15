import spacy
import pandas as pd
from torchtext.legacy.data import Field, BucketIterator, TabularDataset
from sklearn.model_selection import train_test_split
import torch

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

statement.build_vocab(train_data)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

BATCH_SIZE = 1

train_iterator, test_iterator = BucketIterator.splits(
    (train_data, test_data),
    sort = False,
    batch_sizes=BATCH_SIZE,
    device = device
)

print('Train: ')
for batch in train_iterator:
    print(batch)
