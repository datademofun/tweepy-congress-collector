from os import makedirs
from os.path import join, exists
import csv
import json
import re

HEADERS_TO_KEEP = ['id', 'text', 'created_at',
                    'favorite_count', 'retweet_count',
                    'in_reply_to_screen_name',
                    'in_reply_to_status_id',
                    'in_reply_to_user_id_str',
                    'is_quote_status']

ADDITIONAL_HEADERS =  ['bioguide_id', 'user_id', 'user_screen_name', 'source_name',
                       'retweeted_status_id', 'retweeted_status_user_id']

ALL_HEADERS = HEADERS_TO_KEEP + ADDITIONAL_HEADERS


TWEETS_DIR = join('data', 'twitter', 'tweets')
PROFILES_DIR = join('data', 'twitter', 'profiles')

BIOGUIDE_TWITTER_ID_FILENAME = join('data', 'legislators-on-twitter.csv')

OUTPUT_DIR = join('data', 'wrangled')
OUTPUT_FILENAME = join(OUTPUT_DIR, 'congress-tweets.csv')
makedirs(OUTPUT_DIR, exist_ok=True)

# set up the CSV file
wf = open(OUTPUT_FILENAME, 'w')
wcsv = csv.DictWriter(wf, fieldnames=ALL_HEADERS)
wcsv.writeheader()

# first, get a list (of dicts) of all bioguide_ids and twitter_ids
with open(BIOGUIDE_TWITTER_ID_FILENAME, 'r') as rf:
    xlist = list(csv.DictReader(rf))
    # not all congressmembers have twitter ids
    accounts = [a for a in xlist if a['twitter_id']]


for a in accounts:
    bioguide_id = a['bioguide_id']
    tw_user_id = a['twitter_id']
    # open the tweets file
    tweets_fname = join(TWEETS_DIR, tw_user_id + '.json')
    with open(tweets_fname, 'r') as rf:
        print("Processing", tweets_fname)
        tweets = json.load(rf)
    # screen_name is NOT included in the tweet objects
    # we have to open the corresponding profile to get it
    profiles_fname = join(PROFILES_DIR, tw_user_id + '.json')
    with open(profiles_fname, 'r') as pf:
        p = json.load(pf)
        tw_screen_name = p['screen_name']

    # tweets is a list
    # we'll be operating on each tweet
    for tweet in tweets:
        mydict = {'bioguide_id': bioguide_id,
                  'user_id': tw_user_id,
                  'user_screen_name': tw_screen_name}
        # add the boilerplate headers
        for h in HEADERS_TO_KEEP:
            mydict[h] = tweet[h]
        #########################
        # now add the additional headers
        #
        # adding source_name
        # the `source` attribute looks like this:
        # "<a href=\"http://twitter.com\" rel=\"nofollow\">Twitter Web Client</a>"
        # We want source_name to be:
        #  Twitter Web Client
        mtch = re.search(r'">(.+?)</a>', tweet['source'])
        if mtch:
            mydict['source_name'] = mtch.groups()[0] # first capturing group
        else:
            mydict['source_name'] = None
        # if there is a retweet, add retweeted_status_id and retweeted_status_user_id
        retweet = tweet.get('retweeted_status')
        if retweet:
            mydict['retweeted_status_id'] = retweet['id']
            mydict['retweeted_status_user_id'] = retweet['user']['id']
        else:
            mydict['retweeted_status_id'] = None
            mydict['retweeted_status_user_id'] = None
        wcsv.writerow(mydict)

wf.close()
