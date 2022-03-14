import spacy
import pandas as pd
from torchtext.legacy.data import Field, BucketIterator, TabularDataset
from sklearn.model_selection import train_test_split

train_statement = pd.read_json("data/train_statement.json")
test_statement = pd.read_json("data/test_statement.json")

def tokenize_text(text):
    return [tok.text for tok in spacy.load('en').tokenizer(text)]

statement = Field(sequential = True, use_vocab = True, tokenize = tokenize_text, lower = True)

fields = {"Statement": ("statement", statement)}

train_data, test_data = TabularDataset.splits(
    path = "",
    train = "train_statement.json",
    test = "test_statement.json",
    format = "json",
    fields = fields)

statement.build_vocab(train_data, max_size = 10000, min_freq = 2)

train_iterator, test_iterator = BucketIterator.splits(
    (train_data, test_data),
    batch_size = 32,
    device = "cuda"
)

for batch in train_iterator:
    print(batch)
