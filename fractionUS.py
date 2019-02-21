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

all_tweet_count = []
uscounttwittercode_by_day = []
uscountcountrycode_by_day = []
abroadcounttwittercode_by_day = []
abroadcountcountrycode_by_day = []
enlangcount_by_day = []
otherlangcount_by_day = []

# # Loop over all tweet files
dates = []
for tweet_file in tweet_files:
    dates.append(str((tweet_file.split(".")[0]).split("/")[1]))
    day_tweets = []
    uscountcountrycode = 0 
    abroadcountcountrycode = 0
    uscounttwittercode = 0
    abroadcounttwittercode = 0
    enlangcount = 0
    otherlangcount = 0
    with open(tweet_file, 'r') as f:
        # Go through each tweet in the tweet file
        for line in f:
            # Load tweet (make sure to strip newline character from end of line)
            # `tweet` is a dictionary object with many keys
                try:
                    tweet = json.loads(line.strip("\n"))
                except:
                    print("Load error")
                    continue

                if "location" in tweet:
                    if "country_code" in tweet["location"]:
                        if tweet["location"]["country_code"] == "United States":
                            uscountcountrycode += 1 
                        else: 
                            abroadcountcountrycode += 1
                    if "twitter_country_code" in tweet["location"]:
                        if tweet["location"]["twitter_country_code"] == "US":
                            uscounttwittercode += 1 
                        else: 
                            abroadcounttwittercode += 1

                if "actor" in tweet: 
                    if "languages" in tweet["actor"]:
                        for language in tweet["actor"]["languages"]:
                            if language == "en":
                                enlangcount += 1
                            else:
                                otherlangcount += 1



                day_tweets.append(tweet)
        all_tweet_count.append(len(day_tweets))

        uscountcountrycode_by_day.append(uscountcountrycode)
        abroadcountcountrycode_by_day.append(abroadcountcountrycode)
        uscounttwittercode_by_day.append(uscounttwittercode)
        abroadcounttwittercode_by_day.append(abroadcounttwittercode)
        enlangcount_by_day.append(enlangcount)
        otherlangcount_by_day.append(otherlangcount)

print(uscountcountrycode_by_day)
print(uscounttwittercode_by_day)
print(abroadcountcountrycode_by_day)
print(abroadcounttwittercode_by_day)
print(enlangcount_by_day)
print(otherlangcount_by_day)
print(all_tweet_count)

all_tweet_count.remove(0)
enlangcount_by_day.remove(0)
otherlangcount_by_day.remove(0)

d = np.array(all_tweet_count, dtype=np.float)
a = np.array(enlangcount_by_day, dtype=np.float)
b = np.array(otherlangcount_by_day, dtype=np.float)

fraction_of_enlang = a/d
fraction_of_other = b/d

dates.remove('')
x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.plot(x, fraction_of_enlang, label="English primary")
plt.plot(x, fraction_of_other, label="Other primary")
plt.xlabel("time")
plt.ylabel("fraction of user languages")
plt.gcf().autofmt_xdate()
plt.legend()
plt.show()