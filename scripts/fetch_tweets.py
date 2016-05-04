from glob import glob
from os import makedirs
from os.path import join, basename, splitext
from twitterfoo import get_twitter_api

import json

DATA_DIR = 'data'
TWITTER_PROFILES_DIR = join(DATA_DIR, 'twitter', 'profiles')
TWITTER_TWEETS_DIR = join(DATA_DIR, 'twitter', 'tweets')
makedirs(TWITTER_TWEETS_DIR, exist_ok=True)

# initiate the twitter hookup
api = get_twitter_api('creds_twitter.json')

# only fetch tweets based on the profiles we've collected so far
for fname in glob(join(TWITTER_PROFILES_DIR, '*.json')):
    t_id = splitext(basename(fname))[0] # split the file name, get the first part
    print("Fetching tweets for id:", t_id)
    results = api.user_timeline(user_id=t_id, count=200,
                               trim_user=True, exclude_replies=False,
                               include_rts=True)

    # have to convert each tweet in the ResultSet to a dict
    tweets = [r._json for r in results]
    jname = join(TWITTER_TWEETS_DIR, '{id}.json'.format(id=t_id))
    print("Writing to:", jname)
    with open(jname, 'w') as wf:
        wf.write(json.dumps(tweets, indent=2))
