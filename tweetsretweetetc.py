import os
import json
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.dates as mdates

# Specify which directory the day tweet files are in
tweet_files_dir = 'metoo copy'
# Get all the tweet filenames
tweet_files = sorted(os.listdir(tweet_files_dir))
# Prepend directory to each tweet filename
tweet_files = [tweet_files_dir+'/'+filename for filename in tweet_files]

all_tweet_count = []
retweet_count_by_day =[]
reply_count_by_day = []
quote_count_by_day = []

# # Loop over all tweet files
dates = []
for tweet_file in tweet_files:
    dates.append(str((tweet_file.split(".")[0]).split("/")[1]))
    day_tweets = []
    retweet_count = 0 
    quote_count = 0 
    reply_count = 0
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

                if tweet["verb"] == "share":
                    retweet_count += 1 

                if "twitter_quoted_status" in tweet:
                    quote_count += 1 

                if "inReplyTo" in tweet: 
                    reply_count += 1

                day_tweets.append(tweet)
        all_tweet_count.append(len(day_tweets))

        retweet_count_by_day.append(retweet_count)
        quote_count_by_day.append(quote_count)
        reply_count_by_day.append(reply_count)

print(retweet_count_by_day)
print(quote_count_by_day)
print(reply_count_by_day)

all_tweet_count.remove(0)
retweet_count_by_day.remove(0)
quote_count_by_day.remove(0)
reply_count_by_day.remove(0)
dates.remove('')
x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
print(all_tweet_count)
print(x)
plt.plot(x, np.log(all_tweet_count))
plt.plot(x, np.log(reply_count_by_day))
plt.plot(x, np.log(quote_count_by_day))
plt.plot(x, np.log(retweet_count_by_day))
plt.gcf().autofmt_xdate()
plt.show()