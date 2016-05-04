from os import makedirs
from os.path import join
from twitterfoo import get_twitter_api
from math import ceil
import csv
import json

DATA_DIR = 'data'
CONGRESS_TWITTER_FILENAME = join(DATA_DIR, 'legislators-on-twitter.csv')
TWITTER_PROFILES_DIR = join(DATA_DIR, 'twitter', 'profiles')
makedirs(TWITTER_PROFILES_DIR, exist_ok=True)

# Twitter's API only allows the lookup of 100 IDs at a time
BATCH_SIZE = 100

# get the twitter ids
with open(CONGRESS_TWITTER_FILENAME, 'r') as rf:
    rows = list(csv.DictReader(rf))
    twitter_ids = [r['twitter_id'] for r in rows if r]

print(len(twitter_ids), 'twitter ids, out of', len(rows), 'total rows')

# initiate the twitter hookup
api = get_twitter_api('creds_twitter.json')
numbatches = ceil(len(twitter_ids) / BATCH_SIZE)
for i in range(numbatches):
    xx = i * BATCH_SIZE
    yy = xx + BATCH_SIZE
    bids = twitter_ids[xx:yy]
    print("Batch:", i, 'from:', xx, 'to:', yy)
    results = api.lookup_users(user_ids=bids)
    for profile in results:
        # each result object is not a dictionary
        # so we call ._json, which turns it into a dictionary
        # which we then serialize into JSON and write to disk
        pdata = profile._json
        jname = join(TWITTER_PROFILES_DIR, '{id}.json'.format(id=pdata['id']))
        with open(jname, 'w') as wf:
            wf.write(json.dumps(pdata, indent=2))
            print("Wrote", pdata['screen_name'], 'data to:', jname)

