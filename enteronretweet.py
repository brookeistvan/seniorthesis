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

users = {}
new_users_by_day = []
retweetenter_by_day = []
quoteenter_by_day = []
replyenter_by_day = []

# # Loop over all tweet files
dates = []
for tweet_file in tweet_files:
    newusercount = 0
    retweetenter = 0 
    quoteenter = 0 
    replyenter = 0 
    dates.append(str((tweet_file.split(".")[0]).split("/")[1]))
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
                    if tweet["actor"]["preferredUsername"] in users:
                        users[tweet["actor"]["preferredUsername"]] += 1
                    else: 
                        newusercount += 1
                        users.update({tweet["actor"]["preferredUsername"]:1})
                        if "verb" in tweet:
                            if tweet["verb"] == "share":
                                retweetenter += 1 
                        if "twitter_quoted_status" in tweet:
                            quoteenter += 1 
                        if "inReplyTo" in tweet: 
                            replyenter += 1
     
    new_users_by_day.append(newusercount)
    retweetenter_by_day.append(retweetenter)
    replyenter_by_day.append(replyenter)
    quoteenter_by_day.append(quoteenter)


new_users_by_day.remove(0)
retweetenter_by_day.remove(0)
replyenter_by_day.remove(0)
quoteenter_by_day.remove(0)
# print(new_users_by_day)
# print(retweetenter_by_day)
# print(replyenter_by_day)
# print(quoteenter_by_day)

d = np.array(new_users_by_day, dtype=np.float)
a = np.array(retweetenter_by_day, dtype=np.float)
b = np.array(quoteenter_by_day, dtype=np.float)
c = np.array(replyenter_by_day, dtype=np.float)

fraction_of_retweets = a/d
fraction_of_quotes = b/d
fraction_of_replies = c/d 

dates.remove('')
x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
# plt.plot(x, np.log(new_users_by_day), label="new users")
plt.plot(x, fraction_of_retweets, label="entered on a retweet")
plt.plot(x, fraction_of_replies, label="entered on a reply")
plt.plot(x, fraction_of_quotes, label="entered on a quote")
plt.gcf().autofmt_xdate()
plt.xlabel("time")
plt.ylabel("percent of new users")
plt.legend()
plt.show()