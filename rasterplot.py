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



# # Loop over all tweet files
users = {}
dates = []
for tweet_file in tweet_files:
    with open(tweet_file, 'r') as f:
        # Go through each tweet in the tweet file
        for line in f:
            # Load tweet (make sure to strip newline character from end of line)
            # `tweet` is a dictionary object with many keys
            # if line.strip():

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
                        users.update({tweet["actor"]["preferredUsername"]:1})


commonusers = {}
for user, count in users.items():
    if count > 100:
        commonusers.update({user:count})

rasterusers = {}
for tweet_file in tweet_files:
    date = str((tweet_file.split(".")[0]).split("/")[1])
    dates.append(date)
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
                    if tweet["actor"]["preferredUsername"] in commonusers:
                        if tweet["actor"]["preferredUsername"] in rasterusers:
                            rasterusers[tweet["actor"]["preferredUsername"]].append(date)
                        else:
                            rasterusers.update({tweet["actor"]["preferredUsername"]: [date]})

print(len(rasterusers))

orderednames = []
for key,value in rasterusers.items():
    orderednames.append(key)

datamatrix = np.array([rasterusers[i] for i in orderednames])

# print(datamatrix)

lineSize = [.3]*len(rasterusers)

# colorCodes = np.array([[0,0,0],
#     [0,0,0],
#     [0,0,0],
#     [0,0,0]])

# colorCodes = np.array([[0, 0, 0],

#                         [1, 0, 0],

#                         [0, 1, 0],

#                         [0, 0, 1]])  

plt.eventplot(datamatrix, linelengths = lineSize)
plt.show()

# to remove u: name = str(lang.split("'")[0])

# # Set the random seed for data generation

# np.random.seed(2)
# # Create rows of random data with 50 data points simulating rows of spike trains

# neuralData = np.random.random([8, 50])

 

# # Set different colors for each neuron
# colorCodes = np.array([[0, 0, 0],

#                         [1, 0, 0],

#                         [0, 1, 0],

#                         [0, 0, 1],

#                         [1, 1, 0],

#                         [1, 0, 1],

#                         [0, 1, 1],

#                         [1, 0, 1]])     

# # Set spike colors for each neuron
# lineSize = [0.4, 0.3, 0.2, 0.8, 0.5, 0.6, 0.7, 0.9]                                  

     
# # Draw a spike raster plot
# plt.eventplot(neuralData, color=colorCodes, linelengths = lineSize)     

 
# # Provide the title for the spike raster plot
# plt.title('Spike raster plot')


# # Give x axis label for the spike raster plot
# plt.xlabel('username')


# # Give y axis label for the spike raster plot
# plt.ylabel('days')

# # Display the spike raster plot
# plt.show()