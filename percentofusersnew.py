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
old_users_by_day = []

# # Loop over all tweet files
dates = []
for tweet_file in tweet_files:
    newusercount = 0
    olderusercount = 0
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
                    if tweet["actor"]["preferredUsername"] in users:
                        olderusercount +=1
                        users[tweet["actor"]["preferredUsername"]] += 1
                    else:
                        newusercount += 1 
                        users.update({tweet["actor"]["preferredUsername"]:1})
        
        new_users_by_day.append(newusercount)
        old_users_by_day.append(olderusercount)

new_users_by_day.remove(0)
old_users_by_day.remove(0)

a = np.array(new_users_by_day, dtype=np.float)
b = np.array(old_users_by_day, dtype=np.float)

total_users_by_day = a + b 

c = np.array(total_users_by_day, dtype=np.float)

fraction_new = a/c
fraction_old = b/c

print(np.mean(fraction_new))

# dates.remove('')
# x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
# plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
# plt.plot(x, fraction_new, label="new users")
# plt.plot(x, fraction_old, label="old users")
# plt.xlabel("time")
# plt.ylabel("fraction of users")
# plt.legend(loc='upper left')
# plt.gcf().autofmt_xdate()
# plt.show()