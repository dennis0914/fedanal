


from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm
from datetime import datetime

df = pd.DataFrame(columns=['date', 'minutes'])
df.set_index('date', inplace=True)

df_date = pd.read_csv("data/fomc_dates.csv")
df_date['date'] = pd.to_datetime(df_date['date'])

start_date = pd.Timestamp("1993-01-01")
end_date = pd.Timestamp("2021-06-01")

minutes_date = df_date.loc[(df_date['date'] > start_date)&(df_date['date'] < end_date)]['date']



url = "https://fraser.stlouisfed.org/title/federal-open-market-committee-meeting-minutes-transcripts-documents-677?browse=2000s"
meetings = BeautifulSoup(requests.get(url).content, 'html.parser').find_all(attrs={"class": "list-item"})
minutes_url_list = list()
for meeting in meetings:
    if("meeting" in meeting['href'].split("/")[3]):
        minutes_url_list.append(meeting['href'])
    else:
     continue
    #0 19


def get_date(minutes_url):
    composition = minutes_url.split("-")
    year = str(composition[-2])
    day = str(composition[-3]).zfill(2)
    try:
        month = str(datetime.strptime(composition[-4], "%B").month).zfill(2)
    except:
        month = str(datetime.strptime(composition[-5], "%B").month).zfill(2)
    return "".join([year, month, day])

pbar = tqdm(minutes_url_list)
for minutes_url in pbar:

    date_index = get_date(minutes_url)
    pbar.set_description("Current: "+str(date_index))
    url = "https://fraser.stlouisfed.org{}/content/fulltext/{}min".format(minutes_url, date_index)
    minutes = BeautifulSoup(requests.get(url).content, 'html.parser').find('pre')
    if minutes == None:
        continue
    else:
        df.loc[pd.Timestamp(date_index)] = minutes.get_text()

