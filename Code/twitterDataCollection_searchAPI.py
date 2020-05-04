#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Modified on Mon Jul 11 2017

@author: OstermannFO

twitterdatacollection_searchAPI.py: 
    access TwitterSeachAPI
    write Tweets as JSON objects in text file

currently using Python2; 
for Python3, replace unicode with str (untested!);
"""

import twitter
import io
import json
import time
from urllib import unquote

# set query parameters
QUERY = '' #Comma-separated list of terms
GEOCODE = '' #latitude, longitude, radius, e.g. 52.000000,5.500000,250km
UNTIL = '' # e.g. 2017-04-01
MAX_RESULTS = 1000 # up to 1000, default 200
SINCE_ID = # lowest, i.e. oldest Tweet ID to be returned

# set path to output files
OUTPUT_PATH = ''

# add authentification details 
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''
    
def oauth_login():   
    auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                               CONSUMER_KEY, CONSUMER_SECRET)    
    twitter_api = twitter.Twitter(auth=auth)
    return twitter_api

def twitter_search(twitter_api, q, max_results=200, **kw):
    search_results = twitter_api.search.tweets(q=q, count=100, **kw)
    statuses = search_results['statuses']
    max_results = min(1000, max_results)
    for _ in range(10): # 10*100 = 1000
        try:
            next_results = search_results['search_metadata']['next_results']
        except KeyError, e: # No more results when next_results doesn't exist
            break
        print next_results    
        # Create a dictionary from next_results, which has the following form:
        # ?max_id=313519052523986943&q=NCAA&include_entities=1
        kwargs = dict([ kv.split('=') 
            for kv in unquote(next_results[1:]).split("&") ])
        #print kwargs
        search_results = twitter_api.search.tweets(**kwargs)
        statuses += search_results['statuses']               
    return statuses
    
def save_json(filename, data):    
    with io.open('{}{}.txt'.format(OUTPUT_PATH, filename),
                 'a', encoding='utf-8') as f:
        f.write(unicode(json.dumps(data, ensure_ascii=False))+'\n')

def main():    
    twitter_api = oauth_login()          
    filename = time.strftime("%Y%m%d-%H%M%S")    
    results = twitter_search(twitter_api, QUERY, MAX_RESULTS, 
                             geocode=GEOCODE, until=UNTIL, since_id = SINCE_ID)
    for result in results:
        save_json(filename, result)
    #Show one sample search result by slicing the list...
    print json.dumps(results[0], indent=1)
    print len(results)

if __name__=="__main__":
    main()        
