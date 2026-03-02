#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# print the count values
items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]))
# keep only top 10 (highest values)
items = items[-10:]

# separate keys and values
labels = [k for k,v in items]
values = [v for k,v in items]

# plotting
import matplotlib.pyplot as plt

plt.figure()
plt.bar(labels, values)
plt.xticks(rotation=45, ha='right')
plt.xlabel('Key')
plt.ylabel('Value')
plt.title(args.key)

# save figure
output_file = os.path.basename(args.input_path) + '.' + args.key.replace('#','') + '.png'
plt.tight_layout()
plt.savefig(output_file)
