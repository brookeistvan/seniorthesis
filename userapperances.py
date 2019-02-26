import os
import json
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.dates as mdates

# Specify which directory the day tweet files are in
tweet_files_dir = 'metoo copy'
# Get all the tweet filenames
tweet_files = sorted(os.listdir(tweet_files_dir))
# Prepend directory to each tweet filename
tweet_files = [tweet_files_dir+'/'+filename for filename in tweet_files]

users = {}

# # Loop over all tweet files
dates = []
for tweet_file in tweet_files:
    dates.append(str((tweet_file.split(".")[0]).split("/")[1]))
    with open(tweet_file, 'r') as f:
        # Go through each tweet in the tweet file
        linenumber = 1
        for line in f:
            try:
                tweet = json.loads(line.strip("\n"))
            except:
                print("Load error")
                continue

            if "actor" in tweet:
                if "preferredUsername" in tweet["actor"]:
                    if tweet["actor"]["preferredUsername"] in users:
                        users[tweet["actor"]["preferredUsername"]] += 1
                    else:
                        users.update({tweet["actor"]["preferredUsername"]:1})
print(len(users))
# print(users)

# get a dictionary of key = # of tweet times and value = a list of users 
tweettimes_listofusers = {}
for k,v in users.items():
    tweettimes_listofusers.setdefault(v, []).append(k)
print(len(tweettimes_listofusers))

# change dict^ to key = # of tweet times and value = len of list of users
numtweets_numusers = {}
for key,value in tweettimes_listofusers.items():
    numtweets_numusers.update({key:len(value)})
print(len(numtweets_numusers))

# drop entries with key >10 
for k1, v1 in numtweets_numusers.items():
    if k1 > 10:
        del numtweets_numusers[k1]

# graph key as x and value as y
plt.bar(range(len(numtweets_numusers)), list(numtweets_numusers.values()), align='center')
plt.xticks(range(len(numtweets_numusers)), list(numtweets_numusers.keys()))
plt.xlabel("number of tweets sent by user")
plt.ylabel("number of users who sent x number of tweets")
plt.show()
