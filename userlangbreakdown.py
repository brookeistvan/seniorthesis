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
english = 0
other = 0 

# # Loop over all tweet files
# dates = []
for tweet_file in tweet_files:
    # dates.append(str((tweet_file.split(".")[0]).split("/")[1]))

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

                if "actor" in tweet:
                    if "preferredUsername" in tweet["actor"]:
                        if tweet["actor"]["preferredUsername"] not in users: 
                            if "languages" in tweet["actor"]:
                                # for language in tweet["actor"]["languages"]:
                                users.update({tweet["actor"]["preferredUsername"]:tweet["actor"]["languages"]})
                                if "en" in tweet["actor"]["languages"]:
                                    english += 1 
                                else:
                                    other += 1
# print(users)

# english = 0 
# other = 0 

# for k, v in users.items():
#     if "u'en'" in users.values(): 
#         english += 1 
#     else: 
#         other += 1
print(english)
print(other)

# plotablelanguages = {}
# for lang, count in languages.items():
#     if count > 500:
#         name = str(lang.split("'")[0])
#         plotablelanguages.update({name:count})

# print(languages)
# print(plotablelanguages)

# # graph key as x and value as y
# plt.bar(range(len(plotablelanguages)), list(plotablelanguages.values()), align='center')
# plt.xticks(range(len(plotablelanguages)), list(plotablelanguages.keys()))
# plt.xlabel("language")
# plt.ylabel("total number of tweets per language")
# plt.show()


