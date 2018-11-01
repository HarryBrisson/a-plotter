# https://github.com/unitedstates/congress-legislators
# let's start with a list of current legislators

import requests

r = requests.get('https://theunitedstates.io/congress-legislators/legislators-current.json')
congress_json = r.json()

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
	for congressman in congress_json:
	    bioguide = congressman['id']['bioguide']
	    photo_url = r'https://theunitedstates.io/images/congress/225x275/'+bioguide+'.jpg'
	    download_file(photo_url,downloadto=r'images/')


# now let's pull a few different datasets for the folks we have

def get_propublica_api_key():
	propublica_api_key = open(r"propublica_api_key.txt","r").read()
	return propublica_api_key

def get_recent_votes():

    # put your key in the header
    headers = {
        "X-API-Key": get_propublica_api_key()
    }

    url = "https://api.propublica.org/congress/v1/house/votes/recent.json"

    # make request
    r = requests.get(url, headers=headers)

    return(r.json())


def get_vote_breakdown(vote_number):

    # put your key in the header
    headers = {
        "X-API-Key": propublica_api_key
    }

    url = r"https://api.propublica.org/congress/v1/115/senate/sessions/1/votes/"+vote_number+r".json"

    # make request
    r = requests.get(url, headers=headers)

    return(r.json())


