# Fetching Congress tweets

A quickie demo of how to fetch the latest 200 tweets for every current Congressmember who has a Twitter account.

Besides the [example Python scripts](scripts/), I've included the data that the scripts fetch, fresh from [unitedstates/congress-legislators](https://github.com/unitedstates/congress-legislators) and the [Twitter API](https://dev.twitter.com/rest/public). The Twitter data is included for educational purposes and is not intended for redistribution:

- [data/legislators-social-media.yaml](data/legislators-social-media.yaml) - the lookup-file that links Congressmembers to their social media identities
- [data/legislators-on-twitter.csv](data/legislators-on-twitter.csv) - a simplified lookup table showing only bioguide IDs and Twitter IDs.
- [data/twitter/profiles/](data/twitter/profiles/) - the profiles (in JSON format) for each of the Congressmember Twitter accounts
- [data/twitter/tweets/](data/twitter/tweets/) - the most recent 200 tweets (in JSON format) for each of the Congressmember Twitter accounts




## Running the code

Assuming you've managed to [register a Twitter application and get authentication credentials](#step-twitter-auth) -- and have created a your own file named [creds_twitter.json](sample.creds_twitter.json)...and that you have [__tweepy__](http://docs.tweepy.org/) installed, along with Python 3.5 and the relevant libraries, you should be able to run the Python scripts in [scripts/](scripts/) in this sequence (via command-line interpreter):


~~~sh
$ python scripts/fetch_legislators.y
# creates data/legislators-on-twitter.csv
$ python scripts/fetch_profiles.py
# creates data/twitter/profiles/
$ python scripts/fetch_tweets.py
# creates data/twitter/tweets/
~~~





# Walkthrough

An elaboration of where the data comes from and the programming logic behind the scripts in [scripts/](scripts/)


## Step 1A: Fetch social-media-account data from unitedstates/congress-legislators

The public Github repo at [unitedstates/congress-legislators](https://github.com/unitedstates/congress-legislators) contains a crowdsourced list of information about U.S. Congress, including who is currently serving, and what their social media accounts are.

Of particular interest to us is the [legislators-social-media.yaml](https://github.com/unitedstates/congress-legislators/blob/master/legislators-social-media.yaml) file, which lists social media accounts for every Congressmember in YAML format.

Think of YAML as a more-human-friendly JSON format:

~~~yaml
- id:
    bioguide: R000600
    thomas: '02222'
    govtrack: 412664
  social:
    twitter: RepAmata
    facebook: congresswomanaumuaamata
    facebook_id: '1537155909907320'
    youtube_id: UCGdrLQbt1PYDTPsampx4t1A
    twitter_id: 3026622545
- id:
    bioguide: H001070
    thomas: '02260'
    govtrack: 412645
  social:
    twitter: RepHardy
    facebook: RepCresentHardy
    youtube: RepHardy
    facebook_id: '320612381469421'
    youtube_id: UCc8E6NWCdgrXjBVI2NNPYdA
    twitter_id: 2964222544
~~~


Here's the JSON equivalent:

~~~json
[
  {
    "id": {
      "govtrack": 412664,
      "thomas": "02222",
      "bioguide": "R000600"
    },
    "social": {
      "facebook_id": "1537155909907320",
      "facebook": "congresswomanaumuaamata",
      "twitter": "RepAmata",
      "twitter_id": 3026622545,
      "youtube_id": "UCGdrLQbt1PYDTPsampx4t1A"
    }
  },
  {
    "id": {
      "govtrack": 412645,
      "thomas": "02260",
      "bioguide": "H001070"
    },
    "social": {
      "facebook_id": "320612381469421",
      "youtube_id": "UCc8E6NWCdgrXjBVI2NNPYdA",
      "twitter_id": 2964222544,
      "youtube": "RepHardy",
      "facebook": "RepCresentHardy",
      "twitter": "RepHardy"
    }
  }
]
~~~


How do you deserialize a YAML-formatted string into a Python data object (in this case, a list of dictionaries)? Just [use the __yaml__ module](http://pyyaml.org/wiki/PyYAMLDocumentation).

The script for this step can be found at: [scripts/fetch_legislators.py](scripts/fetch_legislators.py). The YAML deserialization looks like this:

~~~py
import yaml
# assuming resp contains a downloaded file via Requests...
datarows = yaml.load(resp.text)
~~~



## Step 1B: Extract Twitter IDs from legislators-social-media

For the exercise at hand, we don't need most of the data in [legislators-social-media.yaml](data/legislators-social-media.yaml), just these two things from each legislator:

- Their `bioguide_id`, which is in `['id']['bioguide']`, because it serves as the unique identifier for a Congressmember.
- Their `twitter_id`, which is in `['social']['twitter_id']`, because it serves as the unique ID for a Twitter account (even if the _name_ of the account changes).

And then we write it into a nice flat CSV file, [data/legislators-on-twitter.csv](data/legislators-on-twitter.csv), which looks like:


| bioguide_id | twitter_id |
|-------------|------------|
| R000600     | 3026622545 |
| H001070     | 2964222544 |
| Y000064     |  234128524 |
| E000295     | 2856787757 |

Again, the script for this step can be found at: [scripts/fetch_legislators.py](scripts/fetch_legislators.py)


<a id="step-twitter-auth"></a>

## Step 2A: Create a Twitter developer account and get app credentials

This is the step that will probably deter you from just jumping in and running the included scripts. To work directly with Twitter's API, you need to have a Twitter account and you need to then create a developer account and then, register an "application".

I've written a walkthrough here, no guarantees on how up-to-date it is: [Twitter App Authentication Process](http://2015.compjour.org/tutorials/twitter-app-authentication-process/)

When you finish it, you should be able to make a JSON file that looks like the one included in this repo at [sample.creds_twitter.json](sample.creds_twitter.json):

~~~json
{
    "consumer_key": "CONSUMERKEY",
    "consumer_secret": "CONSUMER_SECRET",
    "access_token": "ACCESS_TOKEN",
    "access_token_secret": "ACCESS_SECRET"
}
~~~


## Step 2B: Install the tweepy library

While Twitter's API can be called via HTTP requests...I don't recommend it. It's far easier to use the [tweepy library](http://docs.tweepy.org/en/v3.5.0/), which abstracts all the details into a nice programmatic interface.

Tweepy doesn't come with Anaconda, so you'll have to install it via pip:

~~~sh
$ pip install tweepy
~~~

If you finished steps 2A and 2B, you should be able to play around with the Twitter API.

Assuming you have a JSON file named `creds_twitter.json` and it's formatted like [sample.creds_twitter.json](sample.creds_twitter.json), try this in iPython:

~~~py
import tweepy
import json
with open('creds_twitter.json', 'r') as rf:
    creds = json.load(rf)

# Authenticate with twitter
auth = tweepy.OAuthHandler(consumer_key=creds['consumer_key'],
                           consumer_secret=creds['consumer_secret'])

auth.set_access_token(creds['access_token'],
                      creds['access_token_secret'])                           

# Pass in the `auth` object to tweepy.API to 
# get an object for handling API calls:
api = tweepy.API(auth)

# look up the account that is connected to the auth 
# credentials
profile = api.me()
profile.screen_name
# 'whateveryourtwitternameis'
profile.followers_count
# 42

# let's lookup another user
trump = api.get_user(screen_name='realDonaldTrump')
trump.name
# 'Donald J. Trump'
trump.followers_count
# 7911876
trump.description
# '#MakeAmericaGreatAgain #Trump2016'
~~~


In the file [scripts/twitterfoo.py](scripts/twitterfoo.py), I've written a convenience method named `get_twitter_api()` that handles the open-a-JSON-file-and-authenticate-process. This function is used in subsequent scripts.


## Step 3: Fetch and save each Congressmember's Twitter profile

- Open the file [data/legislators-on-twitter.csv](data/legislators-on-twitter.csv) and pull out just the `twitter_id` column to get a list of Twitter IDs.
- Pass this list of Twitter IDs into the tweepy-wrapped API call for fetching profile information.
- Save each profile object as its own JSON file.

The code for this step is at [scripts/fetch_profiles.py](scripts/fetch_profiles.py). And the result can be seen in the directory [data/twitter/profiles/](data/twitter/profiles/).

It's worth reading the [Twitter API documentation for its GET users/lookup call](https://dev.twitter.com/rest/reference/get/users/lookup) to understand the code in [scripts/fetch_profiles.py](scripts/fetch_profiles.py) and the structure of the returned data.


## Step 4: Fetch the most recent 200 tweets associated with each Congressmember's account

This step assumes that [scripts/fetch_profiles.py](scripts/fetch_profiles.py) did its work and the directory [data/twitter/profiles/](data/twitter/profiles/) is full of individual JSON files, each named after the Twitter profile ID number that it represents, e.g. [data/twitter/profiles/1037321378.json](data/twitter/profiles/1037321378.json)

1. Glob through [data/twitter/profiles/](data/twitter/profiles/) and extract the ID number from each filename.
2. For each ID number, use tweepy's `user_timeline()` function to request the most recent 200 tweets from Twitter's [GET statuses/user_timeline endpoint](https://dev.twitter.com/rest/reference/get/statuses/user_timeline)
3. Save each list of tweets as its own file in [data/twitter/tweets](data/twitter/tweets), using the Twitter user ID number for the filename, e.g. [data/twitter/tweets/1037321378.json](data/twitter/tweets/1037321378.json)


