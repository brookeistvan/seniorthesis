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
users_by_day = []
foreign_by_day = []
us_by_day = []

# # Loop over all tweet files
dates = []
for tweet_file in tweet_files:
    daytweets = []
    dayusercount = 0
    repeaters = 0
    uscount = 0 
    foreigncount = 0 
    dayusers={"removeme"}
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
                    if tweet["actor"]["preferredUsername"] not in dayusers:
                        dayusers.add(tweet["actor"]["preferredUsername"])
                        dayusercount += 1
                        if "languages" in tweet["actor"]:
                            if "en" in tweet["actor"]["languages"]:
                                uscount += 1
                            else:
                                foreigncount += 1
                    else:
                        repeaters +=1
        
            # daytweets.append(tweet)
    dayusers.remove("removeme")
    users_by_day.append(len(dayusers))
    foreign_by_day.append(foreigncount)
    us_by_day.append(uscount)

users_by_day.remove(0)
foreign_by_day.remove(0)
us_by_day.remove(0)

print(users_by_day)
print(foreign_by_day)
print(us_by_day)

dates.remove('')
x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
# plt.plot(x, users_by_day, label="infected users")
plt.plot(x, foreign_by_day, label = "foregin users", color='r')
plt.plot(x, us_by_day, label = "U.S. domestic users", color='b')
plt.xlabel("time")
plt.ylabel("number of users")
plt.gcf().autofmt_xdate()
plt.legend()
plt.show()