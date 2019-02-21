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
languages = {}

# # Loop over all tweet files
dates = []
for tweet_file in tweet_files:
    dates.append(str((tweet_file.split(".")[0]).split("/")[1]))
    day_tweets = []
    # uscountcountrycode = 0 
    # abroadcountcountrycode = 0
    # uscounttwittercode = 0
    # abroadcounttwittercode = 0
    # enlangcount = 0
    # otherlangcount = 0
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
                # if "location" in tweet:
                #     if "country_code" in tweet["location"]:
                #         if tweet["location"]["country_code"] == "United States":
                #             uscountcountrycode += 1 
                #         else: 
                #             abroadcountcountrycode += 1
                #     if "twitter_country_code" in tweet["location"]:
                #         if tweet["location"]["twitter_country_code"] == "US":
                #             uscounttwittercode += 1 
                #         else: 
                #             abroadcounttwittercode += 1

                # if "actor" in tweet: 
                #     if "languages" in tweet["actor"]:
                #         for language in tweet["actor"]["languages"]:
                #             if language == "en":
                #                 enlangcount += 1
                #             else:
                #                 otherlangcount += 1

                if "actor" in tweet:
                    if "languages" in tweet["actor"]:
                        for language in tweet["actor"]["languages"]:
                            if language in languages:
                                languages[language] += 1
                            else:
                                languages.update({language:1})


                day_tweets.append(tweet)
        all_tweet_count.append(len(day_tweets))
plotablelanguages = {}
for lang, count in languages.items():
    if count > 500:
        name = str(lang.split("'")[0])
        plotablelanguages.update({name:count})

print(languages)
print(plotablelanguages)

# graph key as x and value as y
plt.bar(range(len(plotablelanguages)), list(plotablelanguages.values()), align='center')
plt.xticks(range(len(plotablelanguages)), list(plotablelanguages.keys()))
plt.xlabel("language")
plt.ylabel("total number of tweets per language")
plt.show()