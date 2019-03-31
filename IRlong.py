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

def isrecovered(username):
    for key, value in users_by_day.items():
        if key > newdaycount:
            if username in users_by_day[key]:
                return False
    return True

# # Loop over all tweet files
users = {}
users_by_day = {}
usernum_by_day = []
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
    usernum_by_day.append(len(dayusers))
    users_by_day.update({datecount:dayusers})
usernum_by_day.remove(0)

recoverdcount_by_day= []
newdaycount = 0
for tweet_file in tweet_files:
    newdaycount += 1
    recoverdcount = 0

    # dates.append(str((tweet_file.split(".")[0]).split("/")[1]))
    with open(tweet_file, 'r') as f:
        # Go through each tweet in the tweet file
        for line in f:
            try:
                tweet = json.loads(line.strip("\n"))
            except:
                print("Load error")
                continue

            if "actor" in tweet:
                if "preferredUsername" in tweet["actor"]:
                    if isrecovered(tweet["actor"]["preferredUsername"]) is True:
                        recoverdcount += 1

        recoverdcount_by_day.append(recoverdcount)

recoverdcount_by_day.remove(0)
#usernum_by_day.remove(0)

count = 0
totalrecoved_by_day = []
for r in recoverdcount_by_day: 
    count += r 
    totalrecoved_by_day.append(count)


# To plot number still infected
stillinfected = {}
for i in range(1,427):
    stillinfected.update({i:0})
print(stillinfected)

# to calculate and plot number still infected
for user, activedays in rasterusers.items():
    for day in range(activedays[0], (activedays[-1]+1)):
        stillinfected[day] += 1
print(stillinfected)
del stillinfected[1]

dates.remove('')
x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]


fig, ax1 = plt.subplots()
color = 'red'
ax1.set_xlabel('time')
ax1.set_ylabel('number of users infected')
ax1.plot(x, stillinfected.values(), color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'green'
ax2.set_ylabel('number of users recoverd')
ax2.plot(x, totalrecoved_by_day, color=color)
ax2.tick_params(axis='y', labelcolor=color)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gcf().autofmt_xdate()
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()

# dates.remove('')
# x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]
# print(len(x))
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
# plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
# plt.plot(x, stillinfected.values())
# plt.xlabel("time")
# plt.ylabel("number of users still infected")
# plt.show()