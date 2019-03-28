from __future__ import division
import os
import json
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.dates as mdates
import random
from itertools import groupby
from operator import itemgetter
 

# Specify which directory the day tweet files are in
tweet_files_dir = 'metoo'
# Get all the tweet filenames
tweet_files = sorted(os.listdir(tweet_files_dir))
# Prepend directory to each tweet filename
tweet_files = [tweet_files_dir+'/'+filename for filename in tweet_files]

# # Loop over all tweet files
users = {}
users_by_day = []
dates = []
datecount = 0 
rasterusers = {}
for tweet_file in tweet_files:
    dayusers = {"removeme"}
    date = str((tweet_file.split(".")[0]).split("/")[1])
    dates.append(date)
    datecount += 1
    with open(tweet_file, 'r') as f:
        # Go through each tweet in the tweet file
        for line in f:
            try:
                tweet = json.loads(line.strip("\n"))
            except:
                # print("Load error")
                continue

            if "actor" in tweet:
                if "preferredUsername" in tweet["actor"]:
                    # if tweet["actor"]["preferredUsername"] in commonusers:
                    if tweet["actor"]["preferredUsername"] in rasterusers:
                        rasterusers[tweet["actor"]["preferredUsername"]].append(datecount)
                    else:
                        rasterusers.update({tweet["actor"]["preferredUsername"]: [datecount]})
                    if tweet["actor"]["preferredUsername"] not in dayusers:
                        dayusers.add(tweet["actor"]["preferredUsername"])
    dayusers.remove("removeme")
    users_by_day.append(len(dayusers))
users_by_day.remove(0)

infectedcount_by_day = []
durations = []
durationdict = {}

# to find short duration
#time till infection
consecutives = []
for user1, activedays in rasterusers.items():
    userconsecutives = []
    for k, g in groupby(enumerate(activedays), lambda (i, x): i-x):
        userconsecutives.append(map(itemgetter(1), g))
    consecutives.append(userconsecutives)

shortrecovereddict = {}
for i in range(1,426):
    shortrecovereddict.update({i:0})

for userconsec in consecutives:
    for j in range(1,426):
        # for day in userconsec:
        if j > userconsec[0][0]: 
            if j not in userconsec:
                shortrecovereddict[j] += 1
print(shortrecovereddict)
print(len(shortrecovereddict))

dates.remove('')
x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.plot(x, shortrecovereddict.values(), label="recoverd users", color='g')
plt.plot(x, users_by_day, label="infected users", color = 'r')
plt.xlabel("time")
plt.ylabel("total number of users")
plt.gcf().autofmt_xdate()
plt.show()