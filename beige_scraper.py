from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm

df = pd.DataFrame(columns=['date', 'beige'])
df.set_index('date', inplace=True)

beige_dates = pd.date_range('1970-01-01', '2021-10-01', freq='1M')
pbar = tqdm(beige_dates)
for b_date in pbar:
    pbar.set_description("Current: "+b_date.strftime("%Y%m"))

    url = "https://www.minneapolisfed.org/beige-book-reports/{year}/{year}-{month}-su".format(year = b_date.year, month = str(b_date.month).zfill(2))
    beige_book = BeautifulSoup(requests.get(url).content, 'html.parser').find_all(attrs={'class': 'col-sm-12 col-lg-8 offset-lg-1'})
    if(not(beige_book)):
        continue
    beige_book = [text.get_text() for text in beige_book]
    beige_book = beige_book[0].split("\n")
    beige_book = [text.translate(str.maketrans({"\r": None, "\t": None, "\xa0": " "})).replace("  ", " ").strip() for text in beige_book][4:-1]
    beige_book = [text for text in beige_book if text != ""]
    beige_book = " ".join(beige_book)
    df.loc[b_date] = beige_book

df.to_csv("beige_data.csv")


