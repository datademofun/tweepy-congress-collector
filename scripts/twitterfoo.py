import tweepy
import os
import json


def get_twitter_api(credsfilename):
    """
    Takes care of the Twitter OAuth authentication process and
    creates an API-handler to execute commands on Twitter

    Arguments:
      - credsfile (str): the full path of the filename that contains a JSON
        file with credentials for Twitter

    Returns:
      A tweepy.api.API object

    """
    fn = os.path.expanduser(credsfilename)  # get the full path in case the ~ is used
    creds = json.load(open(fn))
    # Get authentication token
    auth = tweepy.OAuthHandler(consumer_key=creds['consumer_key'],
                               consumer_secret=creds['consumer_secret'])

    auth.set_access_token(creds['access_token'],
                          creds['access_token_secret'])
    # create an API handler
    return tweepy.API(auth, wait_on_rate_limit_notify=True,
                            wait_on_rate_limit=True)


