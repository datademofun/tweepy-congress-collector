# data is here:
# https://github.com/unitedstates/congress-legislators/blob/master/legislators-social-media.yaml
from os.path import join, basename
import yaml
import csv
import requests
SOURCE_URL = 'https://raw.githubusercontent.com/unitedstates/congress-legislators/master/legislators-social-media.yaml'
CSV_HEADERS = ['bioguide_id', 'twitter_id']

DATA_DIR = 'data'
OUTPUT_YAMLNAME = join(DATA_DIR, 'legislators-social-media.yaml')
OUTPUT_CSVNAME = join(DATA_DIR, 'legislators-on-twitter.csv')

# Download the file
print("Downloading", SOURCE_URL)
resp = requests.get(SOURCE_URL)
# save it to disk for safe keeping
with open(OUTPUT_YAMLNAME, 'w') as wf:
    wf.write(resp.text)

# now prepare the CSV to write to
wf = open(OUTPUT_CSVNAME, 'w')
wcsv = csv.DictWriter(wf, fieldnames=CSV_HEADERS)
wcsv.writeheader()

# deserialize the data into a list of dicts:
datarows = yaml.load(resp.text)
for row in datarows:
    d = {}
    d['bioguide_id'] = row['id']['bioguide']
    # we use .get() because not everyone has twitter
    # and we don't want to raise a KeyError in those cases
    d['twitter_id'] = row['social'].get('twitter_id')
    # write the row
    wcsv.writerow(d)


print("Wrote", len(datarows), 'rows to:', OUTPUT_CSVNAME)
wf.close()





