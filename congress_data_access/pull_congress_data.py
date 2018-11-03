# https://github.com/unitedstates/congress-legislators
# let's start with a list of current legislators

import requests
import pandas as pd


def get_congressperson_data():
	r = requests.get('https://theunitedstates.io/congress-legislators/legislators-current.json')
	congress_json = r.json()
	return congress_json

# define a function to let us download files
# https://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
def download_file(url,downloadto=''):
    local_filename = downloadto + url.split('/')[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
    return local_filename



# let's download the relevant photos
# https://github.com/unitedstates/images
def download_congressman_images():
	for congressman in get_congressperson_data():
	    bioguide = congressman['id']['bioguide']
	    photo_url = r'https://theunitedstates.io/images/congress/225x275/'+bioguide+'.jpg'
	    download_file(photo_url,downloadto=r'images/')


# now let's pull a few different datasets for the folks we have

def get_propublica_api_key():
	propublica_api_key = open(r"authentications/propublica_api_key.txt","r").read()
	return propublica_api_key

def get_recent_votes(chamber):

    # put your key in the header
    headers = {
        "X-API-Key": get_propublica_api_key()
    }

    url = "https://api.propublica.org/congress/v1/{}/votes/recent.json".format(chamber)

    # make request
    r = requests.get(url, headers=headers)

    return(r.json())


def get_vote_data(congress_number,chamber,session_number,vote_number):

    # put your key in the header
    headers = {
        "X-API-Key": get_propublica_api_key()
    }

    url = r"https://api.propublica.org/congress/v1/{}/{}/sessions/{}/votes/{}.json".format(congress_number,chamber,session_number,vote_number)

    # make request
    r = requests.get(url, headers=headers)

    return(r.json())


def get_vote_positions_dataframe(vote_breakdown):
    
    congress_number = vote_breakdown['results']['votes']['vote']['congress']
    session_number = vote_breakdown['results']['votes']['vote']['session']
    roll_call_number = vote_breakdown['results']['votes']['vote']['roll_call']

    vote_id = "{}-{}-{}".format(congress_number,session_number, roll_call_number)

    vote_positions = vote_breakdown['results']['votes']['vote']['positions']

    temp_df = pd.DataFrame()
    
    for position in vote_positions:
        row = {
            'bioguide': position['member_id'],
            str(roll_call_number): position['vote_position']
        }
        temp_df = temp_df.append(row,ignore_index=True)
        
    return temp_df



def create_voting_dataframe(congress_number,chamber):
    
	# start with photos?

    vote_breakdown = get_vote_data(congress_number,chamber,1,1)
    votes_df = get_vote_positions_dataframe(vote_breakdown)
    print("created new voting dataframe")
    
    roll_call_number = 2

    
    for session_number in [1,2]:
    

        while True:

            vote_breakdown = get_vote_data(congress_number,chamber,session_number,roll_call_number)
            
            if vote_breakdown['status'] != 'ERROR':

                try: 
                    votes_df = pd.merge(votes_df,get_vote_positions_dataframe(vote_breakdown),on='bioguide')
                    print("added voting records for vote #{} from session #{}".format(roll_call_number,session_number))
                except:
                    pass

                roll_call_number += 1

            else:
                roll_call_number = 1
                break
        
    return votes_df


def binarize_df(votes_df):

    binary_df = votes_df[['bioguide']]

    for c in votes_df.columns:
        if c != "bioguide":
            binary_df[c] = (votes_df[c]=='Yes').astype(int)
            
    return binary_df