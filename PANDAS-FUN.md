

~~~py
from os.path import join
import pandas as pd
DATA_DIR = join('data', 'wrangled')
dfprofiles = pd.read_csv(join(DATA_DIR, 'congress-twitter-profiles.csv'))
dftweets = pd.read_csv(join(DATA_DIR, 'congress-tweets.csv'))
~~~



# Tweet ranking and counting



## Most retweeted tweets

Of the recent tweets collected per Congressmember, which were the 5 most retweeted tweets?

~~~py
top5 = dftweets.sort_values('retweet_count', ascending=False).head(5)
top5[['id', 'user_screen_name', 'retweet_count', 'text']]
~~~

As it turns out, those retweets appear to be retweets of more popular retweets:

The tweet at:

[https://twitter.com/RepAnnaEshoo/status/644266781834477569](https://twitter.com/RepAnnaEshoo/status/644266781834477569)

Resolves to this [POTUS tweet](https://twitter.com/POTUS/status/644193755814342656):

<a href="https://twitter.com/POTUS/status/644193755814342656"><img src="assets/images/potus-tweet-644193755814342656.jpg" alt="potus-tweet-644193755814342656.jpg"></a>



Check out the redirect using Python and requests:

~~~py
import requests
xurl = 'https://twitter.com/RepAnnaEshoo/status/644266781834477569'
resp = requests.get(xurl)
resp.url
# 'https://twitter.com/POTUS/status/644193755814342656'
~~~


## Most retweeted original tweets 

So let's restrict our query to tweets that were _not_ retweets. Another way to specify this query is to filter for tweets in which `retweeted_status_id` is _empty_:

Using [pandas `isnull()` function to filter the array](http://pandas.pydata.org/pandas-docs/stable/missing_data.html):

~~~py
dfnotretweets = dftweets[dftweets.retweeted_status_id.isnull()]
top5 = dfnotretweets.sort_values('retweet_count', ascending=False).head(5)
top5[['id', 'user_screen_name', 'retweet_count', 'text']]
~~~






# Tweet content

## How many tweets were retweets of @realDonaldTrump?

## How many tweets mentioned "Trump"?


