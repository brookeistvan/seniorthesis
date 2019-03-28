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
import math
 

# Specify which directory the day tweet files are in
tweet_files_dir = 'metoo'
# Get all the tweet filenames
tweet_files = sorted(os.listdir(tweet_files_dir))
# Prepend directory to each tweet filename
tweet_files = [tweet_files_dir+'/'+filename for filename in tweet_files]



# # Loop over all tweet files
users = {}
dates = []
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
newuserandduration ={}

# # bootstrap long duration
# count = 0
# for user1, activedays in rasterusers.items():
#     count += 1
#     newuserandduration.update({count:activedays})

# means = []
# for s in range(0, len(rasterusers), 10000):
#     sampleusers = set(random.sample(newuserandduration.keys(), s))

#     for user, activedays in newuserandduration.items():
#         if user in sampleusers:
#             duration = 0
#             duration += (activedays[-1] - activedays[0])
#             durations.append(duration)
#     means.append(np.mean(durations))
#     for i in means: 
#         if math.isnan(i) is True: 
#             means.remove(i)
# m = np.array(means)
# print(np.mean(m))
# print(np.std(m))
# print(len(m))

###
# # to find short duration
# count = 0
# for user1, activedays in rasterusers.items():
#     count += 1
#     newuserandduration.update({count:activedays})

# means = []
# for s in range(0, len(rasterusers), 10000):
#     shortdurations = []
#     sampleusers = set(random.sample(newuserandduration.keys(), s))
#     for user, activedays in newuserandduration.items():
#         if user in sampleusers:
#             for k, g in groupby(enumerate(activedays), lambda (i, x): i-x):
#                 shortdurations.append(len(map(itemgetter(1), g)))
#     means.append(np.mean(shortdurations))
#     for i in means: 
#         if math.isnan(i) is True: 
#             means.remove(i)
# m = np.array(means)
# print(np.mean(m))
# print(np.std(m))
# print(len(m))

###
# Bootstrap find average times till infection
count = 0
for user1, activedays in rasterusers.items():
    count += 1
    newuserandduration.update({count:activedays})

means = []
for s in range(0, len(rasterusers), 10000):
    sampleusers = set(random.sample(newuserandduration.keys(), s))
    consecutives = []
    for user, activedays in newuserandduration.items():
        # if len(activedays) > 1:
            if user in sampleusers:
                userconsecutives = []
                for k, g in groupby(enumerate(activedays), lambda (i, x): i-x):
                    userconsecutives.append(map(itemgetter(1), g))
                consecutives.append(userconsecutives[0])

    timestillfistinfection = []
    for i in consecutives:
        timestillfistinfection.append(i[0])
    means.append(np.mean(timestillfistinfection))
    for i in means: 
        if math.isnan(i) is True: 
            means.remove(i)
m = np.array(means)
print(np.mean(m))
print(np.std(m))
print(len(m))
print(means)

# ###
# ## Bootstrap find average times between infection
# count = 0
# for user1, activedays in rasterusers.items():
#     count += 1
#     newuserandduration.update({count:activedays})
# # print(newuserandduration)
# means = []
# for s in range(100, len(newuserandduration), 10000): #range(0, len(rasterusers), 300):
#     sampleusers = set(random.sample(newuserandduration.keys(), s))
#     # print(sampleusers)
#     consecutives = []
#     for user, activedays in newuserandduration.items():
#         if len(activedays) > 1:
#             if user in sampleusers:
#                 userconsecutives = []
#                 for k, g in groupby(enumerate(activedays), lambda (i, x): i-x):
#                     userconsecutives.append(map(itemgetter(1), g))
#                     # print(userconsecutives)
#                 consecutives.append(userconsecutives)
#     # print(consecutives)
#     allsetperiod =[]
#     for i in consecutives: 
#         lastactiveday = 0
#         setperiods = []
#         for sets in i:
#             period = sets[0] - lastactiveday 
#             if period > 0:
#                 setperiods.append(period)
#             lastactiveday = sets[-1]
#         # print(setperiods)
#         del setperiods[0]
#         if len(setperiods) > 0:
#             allsetperiod.append(setperiods)
#     # print(allsetperiod)
#     # print(len(allsetperiod))
#     sumbetweensettime = 0
#     for i in allsetperiod:
#         for j in i: 
#             sumbetweensettime += j
#     mean = (sumbetweensettime/len(allsetperiod))
#     means.append(mean)
#     for i in means: 
#         if math.isnan(i) is True: 
#             means.remove(i)
# m = np.array(means)
# print(np.mean(m))
# print(np.std(m))
# print(len(m))
# print(means)




