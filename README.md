__Summary:__ Fetching, wrangling, analyzing, and visualizing Twitter and Congress data with Python 3.5, tweepy, pandas, and matplotlib.


# Twitter and Congress Mashup

This repo contains data and several walkthroughs for fetching, wrangling, and visualizing the data, as a means to practice general Python programming as well as learn a bit of pandas and matplotlib.


## About the data

The data comes from two sources:

- The [unitedstates/congress-legislators](https://github.com/unitedstates/congress-legislators) Github repo, which contains crowdsourced lists of biographical data for every U.S. congressmember, including their known social media accounts.
- The [Twitter Public REST API](https://dev.twitter.com/rest/public), specifically, the [users/lookups](statuses/user_timeline) and [statuses/user_timeline](https://dev.twitter.com/rest/reference/get/statuses/user_timeline) endpoints.

## Programming environment requirements

This code was written and tested using the __Python 3.5.0__ installation provided by [Anaconda](https://www.continuum.io/downloads). I try to use as few non-standard libraries as possible, but in general, Anaconda creates an environment with has just about everything you'd need, including [python-dateutil](https://labix.org/python-dateutil)

If you [plan on trying to fetch the data for yourself and following my fetch-code to the letter](FETCH-DATA.md), you'll need to install [tweepy](https://github.com/tweepy/tweepy) on your own.


## Lesson manifest


- [Fetching the data](FETCH-DATA.md) - how did the data in [data/twitter](data/twitter) show up in the repo? Not by magic, but by using the Twitter API and mashing it with crowdsourced Congress data. Note: you don't actually have to _do_ these steps to get data; this repo comes packaged with all the fetched data so that you can focus on the wrangling and visualization.
- [Wrangling the Twitter profiles](WRANGLE-PROFILES.md) - The data structure of a Twitter user profile, as Twitter's API provides it, is pretty complicated. Complicated enough that it needs to be serialized as a nested JSON, which makes it hard to throw all the data in [data/twitter/profiles](data/twitter/profiles) into a spreadsheet for easy comparison. So let's make our own data file by picking the interesting data points from each Twitter profile and saving as a flat, easy-to-use CSV [data/wrangled/congress-twitter-profiles.csv](data/wrangled/congress-twitter-profiles.csv)
- [Wrangling the Twitter tweets](WRANGLE-TWEETS.md) - Same deal as above, except not as lengthy of a walkthrough.
- [Analyzing the wrangled data with pandas](PANDAS-FUN.md) - with the data in convenient-to-read CSV files, let's use pandas to do some data analysis.
- [Visualizing the wrangled data](VIZ-FUN.md) - When you've spent time to think through the structure of data and how to organize it, visualizations become very easy to produce.
