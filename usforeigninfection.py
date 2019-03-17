import os
import json
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.dates as mdates
from itertools import groupby
from operator import itemgetter

# Specify which directory the day tweet files are in
tweet_files_dir = 'metoo copy'
# Get all the tweet filenames
tweet_files = sorted(os.listdir(tweet_files_dir))
# Prepend directory to each tweet filename
tweet_files = [tweet_files_dir+'/'+filename for filename in tweet_files]

users = {}
usretweetforeign_by_day = []
foreignretweetus_by_day = []
usretweetus_by_day = []
foreignretweetforeign_by_day =[]
betweenusers_by_day = []

# # Loop over all tweet files
dates = []
rasterusers = {}
# betweenusers = {"removeme"}
datecount = 0 
for tweet_file in tweet_files:
    usretweetforeign = 0 
    foreignretweetus = 0 
    usretweetus = 0 
    foreignretweetforeign = 0 
    datecount += 1

    dates.append(str((tweet_file.split(".")[0]).split("/")[1]))
    with open(tweet_file, 'r') as f:
        betweenusers = {"removeme"}
        # Go through each tweet in the tweet file
        for line in f:
            try:
                tweet = json.loads(line.strip("\n"))
            except:
                # print("Load error")
                continue

            if "actor" in tweet:
                if "preferredUsername" in tweet["actor"]:
                    # to find avg number from between groups who did not tweet on day before
                    if tweet["actor"]["preferredUsername"] in rasterusers:
                        rasterusers[tweet["actor"]["preferredUsername"]].append(datecount)
                    else:
                        rasterusers.update({tweet["actor"]["preferredUsername"]: [datecount]})

                    if tweet["actor"]["preferredUsername"] not in users:
                        if "languages" in tweet["actor"]:
                            users.update({tweet["actor"]["preferredUsername"]:tweet["actor"]["languages"]})
                            if "en" in tweet["actor"]["languages"]:
                                if "verb" in tweet:
                                    if tweet["verb"] == "share":
                                        if "object" in tweet: 
                                            if "actor" in tweet["object"]:
                                                if "languages" in tweet["object"]["actor"]:
                                                    if "en" not in tweet["object"]["actor"]["languages"]:
                                                        usretweetforeign += 1
                                                        betweenusers.add(tweet["actor"]["preferredUsername"])
                                                    else:
                                                        usretweetus += 1
                            else:
                                if "verb" in tweet:
                                    if tweet["verb"] == "share":
                                        if "object" in tweet: 
                                            if "actor" in tweet["object"]:
                                                if "languages" in tweet["object"]["actor"]:
                                                    if "en" in tweet["object"]["actor"]["languages"]:
                                                        foreignretweetus += 1
                                                        betweenusers.add(tweet["actor"]["preferredUsername"])
                                                    else:
                                                        foreignretweetforeign += 1

    betweenusers_by_day.append(len(betweenusers) - 1)

    usretweetforeign_by_day.append(usretweetforeign)
    foreignretweetus_by_day.append(foreignretweetus)
    usretweetus_by_day.append(usretweetus)
    foreignretweetforeign_by_day.append(foreignretweetforeign)
betweenusers.remove("removeme")
lis = list(betweenusers)
print(lis)
# avg number of users retweeting a between group user
# print(np.mean(lis))

# shortdurations = []
# for user1, activedays in rasterusers.items():
#     if user1 in betweenusers:
#         for k, g in groupby(enumerate(activedays), lambda (i, x): i-x):
#             shortdurations.append(len(map(itemgetter(1), g)))
# print(np.mean(shortdurations))
# print(len(shortdurations))
# durationdict = {}
# for d in shortdurations:
#     if d not in durationdict:
#         durationdict.update({d:1})
#     else:
#         durationdict[d] += 1
# print(durationdict)

# usretweetus_by_day.remove(0)
# foreignretweetforeign_by_day.remove(0)
# usretweetforeign_by_day.remove(0)
# foreignretweetus_by_day.remove(0)
# print(usretweetforeign_by_day)
# print(foreignretweetus_by_day)
# print(usretweetus_by_day)
# print(foreignretweetforeign_by_day)
# print(sum(usretweetforeign_by_day))
# print(sum(foreignretweetus_by_day))
# print(sum(usretweetus_by_day))
# print(sum(foreignretweetforeign_by_day))
print(sum(usretweetforeign_by_day)+sum(foreignretweetus_by_day))
print((sum(usretweetforeign_by_day)+sum(foreignretweetus_by_day))/(len(usretweetforeign_by_day)))
# print(sum(usretweetus_by_day)+sum(foreignretweetforeign_by_day))

# d = np.array(new_users_by_day, dtype=np.float)
# a = np.array(retweetenter_by_day, dtype=np.float)
# b = np.array(quoteenter_by_day, dtype=np.float)
# c = np.array(replyenter_by_day, dtype=np.float)

# fraction_of_retweets = a/d
# fraction_of_quotes = b/d
# fraction_of_replies = c/d 

# dates.remove('')
# x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
# plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
# # plt.plot(x, np.log(new_users_by_day), label="new users")
# plt.plot(x, usretweetforeign_by_day, label="us retweet foreign")
# plt.plot(x, foreignretweetus_by_day, label="foreign retweet us")
# plt.gcf().autofmt_xdate()
# plt.xlabel("time")
# plt.ylabel("number of users entering dataset")
# plt.legend()
# plt.show()