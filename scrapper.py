from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta, datetime
import pandas as pd
from tqdm import tqdm

df = pd.DataFrame(columns=['date', 'statement'])
df.set_index('date', inplace=True)
df_date = pd.read_csv("data/fomc_dates.csv")
df_date['date'] = pd.to_datetime(df_date['date'])

start_date = pd.Timestamp("2007-01-01")
end_date = pd.Timestamp("2017-01-01")

processed_df = df_date.loc[(df_date['date'] > start_date)&(df_date['date'] < end_date)]['date']
pbar = tqdm(processed_df)
for b_date in pbar:
    pbar.set_description("Current: "+b_date.strftime("%Y%m%d"))
    url = 'https://www.federalreserve.gov/newsevents/pressreleases/monetary{}a.htm'.format(b_date.strftime("%Y%m%d"))
    title = BeautifulSoup(requests.get(url).content, 'html.parser').find('h3', attrs={'class': 'title'})

    if title == None:
        continue
    if 'minutes' in title.get_text().lower():
        continue

    statement = BeautifulSoup(requests.get(url).content, 'html.parser').find(attrs={'class': 'col-xs-12 col-sm-8 col-md-8'})
    statement = statement.get_text().split("\n")
    processed_statement = list()
    for paragraph in statement:
        if((paragraph.lower().startswith("implementation")) or (paragraph.lower().startswith("voting for")) or (paragraph == "")):
            continue
        else:
            processed_statement.append(paragraph.strip())
    df.loc[b_date] = " ".join(processed_statement)

df.to_csv('train_statement.csv')