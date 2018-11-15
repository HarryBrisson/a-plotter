import requests
from bs4 import BeautifulSoup
import json
import pandas as pd


def get_list_of_youtube_channels(term,n):

    # initialize list of links
    links = []

    # get a list of links for channels while searching for a given term
    for i in range(0,n,10):
        r = requests.get("https://www.bing.com/search?q="+term+"%20site%3A%20https%3A%2F%2Fwww.youtube.com%2Fchannel%2F&first="+str(i))
        soup = BeautifulSoup(r.text,'html.parser')
        link_elements = soup.find_all('h2')
        for l in link_elements:
            try:
                a = l.find('a')
                links = links + [a['href']]
            except:
                pass

    # get user ids from urls    
    channel_ids_rough = [l.split("/")[l.split("/").index('channel')+1] for l in links if "channel" in l.split("/")]
    channel_ids = [c.split("?")[0] for c in channel_ids_rough]

    # remove duplicates
    channel_ids = list(set(channel_ids))

    return channel_ids


# get API key for the YouTube Data v3 API -- you can create one at https://console.developers.google.com/apis/credentials
def get_youtube_api_key():

    with open('authentications/youtube_api_key.txt', 'r') as f:
        api_key=f.read()

    return api_key


def get_data_string_for_youtube_channels(channel_ids):

    # initialize dataframe
    df = pd.DataFrame()

    api_key = get_youtube_api_key()

    # access youtube stats for each channel id, adding rows to the dataframe
    for c in channel_ids:
        
        r = requests.get("https://www.googleapis.com/youtube/v3/channels?part=snippet%2CcontentDetails%2Cstatistics&id="+c+"&key="+api_key)
        full_data = json.loads(r.text)
        
        # try to get a complete row for as many ids as we can
        try:
            row = {}
            row['id'] = full_data['items'][0]['id']
            row['title'] = full_data['items'][0]['snippet']['title']
            row['img'] = full_data['items'][0]['snippet']['thumbnails']['medium']['url']
            row['subs'] = full_data['items'][0]['statistics']['subscriberCount']
            row['videos'] = full_data['items'][0]['statistics']['videoCount']
            row['views'] = full_data['items'][0]['statistics']['viewCount']
            df = df.append(row,ignore_index=True)
        
        # if there's an error for any field, we won't keep the row in the mix
        except:
            pass
      
    # filter out any rows with 0 videos, subs or views      
    df = df[df['videos'].astype(int)>0]
    df = df[df['subs'].astype(int)>0]
    df = df[df['views'].astype(float)>0]

    # convert to list of dictionaries
    d3_data_string = str(df.to_dict('records'))

    return d3_data_string


def get_youtube_data_string_for_search_term(term,n):
    channel_ids = get_list_of_youtube_channels(term,n)
    data_string = get_data_string_for_youtube_channels(channel_ids)
    return data_string


def get_test_youtube_data_string():
    with open("youtube_demo/test_youtube_data_string.txt") as f:
        test_data_string = f.read()
    return test_data_string
