import os
import json
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.dates as mdates

# Specify which directory the day tweet files are in
tweet_files_dir = 'metoocopy'
# Get all the tweet filenames
tweet_files = sorted(os.listdir(tweet_files_dir))
# Prepend directory to each tweet filename
tweet_files = [tweet_files_dir+'/'+filename for filename in tweet_files]

all_tweet_count = []

# # Loop over all tweet files
dates = []
for tweet_file in tweet_files:
    dates.append(str((tweet_file.split(".")[0]).split("/")[1]))
    day_tweets = []
    with open(tweet_file, 'r') as f:
        # Go through each tweet in the tweet file
        linenumber = 1
        for line in f:
            # Load tweet (make sure to strip newline character from end of line)
            # `tweet` is a dictionary object with many keys
            # if line.strip():

                try:
                    tweet = json.loads(line.strip("\n"))
                except:
                    print("Load error")
                    continue

                if 



                day_tweets.append(tweet)
        all_tweet_count.append(len(day_tweets))
all_tweet_count.remove(0)
dates.remove('')
x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
print(all_tweet_count)
print(x)
plt.plot(x, np.log(all_tweet_count))
plt.gcf().autofmt_xdate()
plt.show()