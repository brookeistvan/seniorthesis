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
dates = []
# for tweet_file in tweet_files:
#     with open(tweet_file, 'r') as f:
#         # Go through each tweet in the tweet file
#         for line in f:
#             # Load tweet (make sure to strip newline character from end of line)
#             # `tweet` is a dictionary object with many keys
#             # if line.strip():

#             try:
#                 tweet = json.loads(line.strip("\n"))
#             except:
#                 # print("Load error")
#                 continue

#             if "actor" in tweet:
#                 if "preferredUsername" in tweet["actor"]:
#                     if tweet["actor"]["preferredUsername"] in users:
#                         users[tweet["actor"]["preferredUsername"]] += 1
#                     else:
#                         users.update({tweet["actor"]["preferredUsername"]:1})


# commonusers = {}
# for user, count in users.items():
#     if count > 50:
#         commonusers.update({user:count})

datecount = 0 
rasterusers = {}
for tweet_file in tweet_files:
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
infectedcount_by_day = []
durations = []
durationdict = {}

## To plot number still infected
# stillinfected = {}
# for i in range(1,427):
#     stillinfected.update({i:0})
# print(stillinfected)

# to find long duration
for user1, activedays in rasterusers.items():
    duration = 0
    duration += (activedays[-1] - activedays[0])
    durations.append(duration)
    if duration in durationdict:
        durationdict[duration] += 1
    else:
        durationdict.update({duration:1})

###
# # to find short duration
# shortdurations = []
# for user1, activedays in rasterusers.items():
#     for k, g in groupby(enumerate(activedays), lambda (i, x): i-x):
#         shortdurations.append(len(map(itemgetter(1), g)))

# print(np.mean(shortdurations))
# print(len(shortdurations))

# for d in shortdurations:
#     if d not in durationdict:
#         durationdict.update({d:1})
#     else:
#         durationdict[d] += 1

# print(durationdict)

# # avg of tweeters for a day who did not tweet the day before
# print(sum(k*v for k,v in durationdict.items()))
# print(sum(durationdict.values()))

###
# # to calculate and plot number still infected
#     for day in range(activedays[0], (activedays[-1]+1)):
#         stillinfected[day] += 1
# print(stillinfected)
# del stillinfected[1]
# dates.remove('')
# x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]
# print(len(x))
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
# plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
# plt.plot(x, stillinfected.values())
# plt.xlabel("time")
# plt.ylabel("number of users still infected")
# plt.show()

# to find users who are still infected
# for i in range(1,427):
#     infectedcount = 0
#     for user, activedays in rasterusers.items():
#        if i in activedays: 
#             infectedcount += 1
#     infectedcount_by_day.append(infectedcount)
#     print(infectedcount_by_day)


# Remove people who only appear on one day
newdurationdict = {"0":0, "Everything >0":0}
onedaypeople = 0
greatthanhundredpeople = 0
for k,v in durationdict.items():
    # if k == 0:
    #     onedaypeople = v
    #     del durationdict[k]

    # if k > 50:
    #     greatthanhundredpeople += v 
    #     del durationdict[k]
    if k == 0:
        newdurationdict["0"] = v
    if k != 0:
        newdurationdict["Everything >0"] += v


# print(durationdict)
# print(onedaypeople)
print(greatthanhundredpeople)
# print(np.mean(durations))
print(newdurationdict)

# graph key as x and value as y
plt.bar(range(len(newdurationdict)), list(newdurationdict.values()), align='center')
plt.xticks(range(len(newdurationdict)), list(newdurationdict.keys()))
plt.xlabel("number of days infected")
plt.ylabel("number of users infected x days")
plt.show()

