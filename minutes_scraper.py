from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm import tqdm
from datetime import datetime
import os

df = pd.DataFrame(columns=['date', 'minutes'])
df.set_index('date', inplace=True)

def get_href(decade = 1990):
    url = "https://fraser.stlouisfed.org/title/federal-open-market-committee-meeting-minutes-transcripts-documents-677?browse={}s".format(str(decade))
    meetings = BeautifulSoup(requests.get(url).content, 'html.parser').find_all(attrs={"class": "list-item"})
    minutes_url_list = list()
    skip_words = ['notation', 'cancelled', 'unscheduled']
    for meeting in meetings:
        if("meeting" in meeting['href'].split("/")[3][:7]):
            if(any(word in meeting['href'] for word in skip_words)):
                continue
            else:
                minutes_url_list.append(meeting['href'])
        else:
            continue
    return minutes_url_list


def get_date(minutes_url):
    composition = minutes_url.split("-")
    year = str(composition[-2])
    day = str(composition[-3]).zfill(2)

    try:
        month = str(datetime.strptime(composition[-4], "%B").month).zfill(2)
    except:
        month = str(datetime.strptime(composition[-5], "%B").month).zfill(2)

    return "".join([year, month, day])

def get_minutes(minutes_url_list):
    pbar = tqdm(minutes_url_list)
    for minutes_url in pbar:

        date_index = get_date(minutes_url)
        pbar.set_description("Current: "+str(date_index))
        if(pd.Timestamp(date_index) > pd.Timestamp("20070918")):
            url = "https://fraser.stlouisfed.org{}/content/fulltext/fomcminutes{}".format(minutes_url, date_index)
        else:
            url = "https://fraser.stlouisfed.org{}/content/fulltext/{}min".format(minutes_url, date_index)

        minutes = BeautifulSoup(requests.get(url).content, 'html.parser').find('pre')
        if minutes == None:
            continue
        else:
            minutes = minutes.get_text().strip()
            minutes = minutes.split("\n")
            minutes = [text.translate(str.maketrans({"\r": None, "\t": None, "\xa0": " "})).replace("  ", " ").strip() for text in minutes]
            minutes = " ".join([text for text in minutes if text != ""])
            df.loc[pd.Timestamp(date_index)] = minutes
    return df
