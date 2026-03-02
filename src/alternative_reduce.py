#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_folder', default='outputs')
parser.add_argument('--hashtags', nargs='+', required=True)
parser.add_argument('--output_path', default='alternative_plot.png')
args = parser.parse_args()

# imports
import os
import json
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# collect daily counts
# structure: {hashtag: {date: count}}
data = {h: {} for h in args.hashtags}

# scan through all .lang files
for filename in os.listdir(args.input_folder):
    if not filename.endswith('.lang'):
        continue
    if filename.startswith('total'):
        continue

    # extract date from filename
    # example: geoTwitter2020-03-15.zip.lang
    date_str = filename.replace('geoTwitter', '').replace('.zip.lang', '')
    date = datetime.datetime.strptime(date_str, "%y-%m-%d").date()

    with open(os.path.join(args.input_folder, filename)) as f:
        counts = json.load(f)

    for hashtag in args.hashtags:
        if hashtag in counts:
            # sum across all languages
            total = sum(counts[hashtag].values())
        else:
            total = 0
        data[hashtag][date] = total

# sort dates
all_dates = sorted(next(iter(data.values())).keys())

# plotting
plt.figure()

for hashtag in args.hashtags:
    values = [data[hashtag].get(d, 0) for d in all_dates]
    plt.plot(all_dates, values, label=hashtag)

plt.xlabel('Date')
plt.ylabel('Tweet Count')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(args.output_path)
