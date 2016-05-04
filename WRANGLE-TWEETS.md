# Wrangling tweets


The code for this exercise can be found at [scripts/wrangle_tweets.csv](scripts/wrangle_tweets.csv).

The final data file (100,000+ records) can be found at [data/wrangled/congress-tweets.csv](data/wrangled/congress-tweets.csv)

For every JSON file in [data/twitter/profiles](data/twitter/profiles), there is a corresponding JSON file in the [data/twitter/tweets](data/twitter/tweets). The latter file contains a serialized list of a user's most recent 200 tweets.

The goal of this wrangle is to combine all the tweets in [data/twitter/tweets](data/twitter/tweets) into a single CSV file: [data/wrangled/congress-tweets.csv](data/wrangled/congress-tweets.csv). With 500+ legislators and ~200 recent tweets each, we should expect [data/wrangled/congress-tweets.csv](data/wrangled/congress-tweets.csv) to have roughly 100,000 records.


You can see a sample of the intended record layout at: [data/wrangled/sample-congress-tweets.csv](data/wrangled/sample-congress-tweets.csv)

As always, a good place to start is by reading the Twitter API documentation, especially if you're not an active Twitter user yourself:

[https://dev.twitter.com/overview/api/tweets](https://dev.twitter.com/overview/api/tweets)

What's a retweet? What's a reply? What fields can be used to tell the difference? There's a lot of tedious detail that's tedious to explain but pretty [straightforward in the documentation](https://dev.twitter.com/overview/api/tweets), though it really helps if you've actually used Twitter.


Even though there is much more data to work with here, the task is simpler than the [profile-wrangling exercise](WRANGLE-PROFILES.md). The main priorities are to:

- add bioguide_id to each tweet so we can link each tweet to its Congressmember
- extract the text content and author identification
- keep the metrics, such as creation time, number of retweets, and favorites
- if the tweet is actually a reply or retweet, keep track of the tweet (and its author) that was replied to/retweeted.


TK more details...
