from datetime import datetime, timezone
from dateutil import parser
from os import makedirs
from os.path import join, exists
import csv
import json

HEADERS_TO_KEEP = ['id', 'screen_name', 'name', 'created_at',
                    'description', 'location', 'url',
                    'statuses_count', 'friends_count', 'followers_count',
                    'verified', 'profile_image_url']

ADDITIONAL_HEADERS = ['bioguide_id', 'days_since_creation', 'days_since_last_tweet',
                      'tweets_count', 'tweets_per_day', 'recent_tweets_per_day']

ALL_HEADERS = HEADERS_TO_KEEP + ADDITIONAL_HEADERS

SECONDS_PER_DAY = 24 * 60 * 60

# Set up the data paths
PROFILES_DIR = join('data', 'twitter', 'profiles')
TWEETS_DIR = join('data', 'twitter', 'tweets')
BIOGUIDE_TWITTER_ID_FILENAME = join('data', 'legislators-on-twitter.csv')

OUTPUT_DIR = join('data', 'wrangled')
OUTPUT_FILENAME = join(OUTPUT_DIR, 'congress-twitter-profiles.csv')
makedirs(OUTPUT_DIR, exist_ok=True)


# what time is it now?
nowtime = datetime.now(timezone.utc)


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
    twitter_id = a['twitter_id']
    profile_fname = join(PROFILES_DIR, twitter_id + '.json')
    # open and process the profile data
    with open(profile_fname, 'r') as rf:
        print("opening", profile_fname)
        profile = json.load(rf)


    mydict = {'bioguide_id': bioguide_id}
    # add the boilerplate headers
    for h in HEADERS_TO_KEEP:
        mydict[h] = profile[h]
    # manually add the derived headers
    # there's no derivation here, I just want
    # to not have to remember that statuses_count refers to tweets count
    mydict['tweets_count'] = profile['statuses_count']


    # timedelta since now and the profile['created_at'] date
    pdt = nowtime - parser.parse(profile['created_at'])
    mydict['days_since_creation'] = pdt.days
    # calculate tweet rate over that days_since_creation count
    tpdrate = mydict['tweets_count'] / pdt.days
    mydict['tweets_per_day'] = round(tpdrate, 2)
    # calculate days since last tweet
    # ...though maybe there might not be a latest tweet...
    latesttweet = profile.get('status')
    if latesttweet:
        xdt = nowtime - parser.parse(latesttweet['created_at'])
        mydict['days_since_last_tweet'] = xdt.days

    # finally, calculate rate among most recent tweets
    tweets_fname = join(TWEETS_DIR, twitter_id + '.json')
    with open(tweets_fname, 'r') as rf:
        tweets = json.load(rf)
    recent_tweet_count = len(tweets)
    # if no tweets then tweets_per_day is NA
    if recent_tweet_count < 1:
        mydict['recent_tweets_per_day'] = 0
    else:
        # assuming reverse-chrono sorting,
        # get oldest tweet timestamp from the last tweet in the list
        oldtime = parser.parse(tweets[-1]['created_at'])
        # get the number of seconds between oldest tweet and right now
        # and calculate the fractional day from seconds
        zdays = (nowtime - oldtime).total_seconds() / SECONDS_PER_DAY
        # good ol law of proportions
        zrate = recent_tweet_count * 30 / zdays
        mydict['recent_tweets_per_day'] = round(zrate,  1)

        # write to CSV
        wcsv.writerow(mydict)

wf.close()
