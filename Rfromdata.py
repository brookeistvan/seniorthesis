# loop through tweets
# create dict of dicts for each day of all users on that day
# loop through tweets again 
# for each user
# if user does not appear in any future days, recoveredcount += 1 
# plot recovered count by day

import os
import json
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.dates as mdates

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


# key would be date or day number and value is set us users appearing then
users_by_day = {}
user_num_by_day = []
tweets_by_day = []

# # Loop over all tweet files
dates = []
daycount = 0
for tweet_file in tweet_files:
    day_tweets = []
    daycount += 1
    todaysusers = {"removeme"}
    dates.append(str((tweet_file.split(".")[0]).split("/")[1]))
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
                    user = tweet["actor"]["preferredUsername"]
                    if user not in todaysusers:
                        todaysusers.add(user)
        
            day_tweets.append(tweet)
        tweets_by_day.append(len(day_tweets))
    todaysusers.remove("removeme")
    users_by_day.update({daycount:todaysusers})
    user_num_by_day.append(len(todaysusers))
# print(users_by_day)

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
# print(recoverdcount_by_day)
# print(user_num_by_day)
# print(tweets_by_day)

recoverdcount_by_day.remove(0)
user_num_by_day.remove(0)

count = 0
totalrecoved_by_day = []
for r in recoverdcount_by_day: 
    count += r 
    totalrecoved_by_day.append(count)

# count = 0 
# for i in totalrecoved_by_day:
#     count += 1
#     if i > 394767:
#         print(count)



# #         new_users_by_day.append(newusercount)
# #         old_users_by_day.append(olderusercount)

# # new_users_by_day.remove(0)
# # old_users_by_day.remove(0)

# a = np.array(recoverdcount_by_day, dtype=np.float)
# b = np.array(user_num_by_day, dtype=np.float)

# fractionrecovered = a/b

# # total_users_by_day = a + b 

# # c = np.array(total_users_by_day, dtype=np.float)

# # fraction_new = a/c
# # fraction_old = b/c
# # print(dates)
# dates.remove('')
# x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
# plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
# plt.plot(x, totalrecoved_by_day)
# # plt.plot(x, fraction_old, label="old users")
# plt.xlabel("time")
# plt.ylabel("total number of users recovered")
# # plt.legend(loc='upper left')
# plt.gcf().autofmt_xdate()
# plt.show()
