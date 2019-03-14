import os
import json
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.dates as mdates
import random
 

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
stillinfected = {}
for i in range(1,427):
    stillinfected.update({i:0})
print(stillinfected)

for user1, activedays in rasterusers.items():
    # duration = 0
    # duration += (activedays[-1] - activedays[0])
    # durations.append(duration)
    # if duration in durationdict:
    #     durationdict[duration] += 1
    # else:
    #     durationdict.update({duration:1})
    for day in range(activedays[0], (activedays[-1]+1)):
        stillinfected[day] += 1
print(stillinfected)
del stillinfected[1]

dates.remove('')
x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]
print(len(x))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.plot(x, stillinfected.values())
plt.xlabel("time")
plt.ylabel("number of users still infected")
plt.show()

# to find users who are still infected
# for i in range(1,427):
#     infectedcount = 0
#     for user, activedays in rasterusers.items():
#        if i in activedays: 
#             infectedcount += 1
#     infectedcount_by_day.append(infectedcount)
#     print(infectedcount_by_day)

# print(infectedcount_by_day)

# # Remove people who only appear on one day
# onedaypeople = 0
# greatthanhundredpeople = 0
# for k,v in durationdict.items():
#     if k == 0:
#         onedaypeople = v
#         del durationdict[k]

#     if k > 50:
#         greatthanhundredpeople += v 
#         del durationdict[k]


# print(durationdict)
# print(onedaypeople)
# print(greatthanhundredpeople)
# print(np.mean(durations))

# # graph key as x and value as y
# plt.bar(range(len(durationdict)), list(durationdict.values()), align='center')
# plt.xticks(range(len(durationdict)), list(durationdict.keys()))
# plt.xlabel("number of days infected")
# plt.ylabel("number of users infected x days")
# plt.show()

