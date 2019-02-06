import os
import json
from pprint import pprint

# Specify which directory the day tweet files are in
tweet_files_dir = 'metoo'
# Get all the tweet filenames
tweet_files = sorted(os.listdir(tweet_files_dir))
# Prepend directory to each tweet filename
tweet_files = [tweet_files_dir+'/'+filename for filename in tweet_files]

# Loop over all tweet files
for tweet_file in tweet_files:

# tweet_file = 'metoo '
    # Open individual day tweet file
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

                    #print(tweet["id"])

                # print(linenumber)
                linenumber +=1

                if "twitter_entities" in tweet:
                    if "urls" in tweet['twitter_entities']:
                        for k,v in tweet['twitter_entities'].items():
                            if k == 'urls':
                                for url in v:
                                    if url == 'https://drive.google.com/open?id=1Eee4aFavPGM3KVk5Wi9qQzveyeF8Yre6':
                                        print(tweet['body'])
                                        print(tweet['actor']['preferredUsername'])
                              
                # if "actor" in tweet:
                #     #if tweet["actor"]["postedTime"] == "2017-m-dT%H:%M:%S.000Z":
                #     print(tweet["actor"]["postedTime"])
                #     #     if tweet["verb"] == "post":
                    #         print(tweet["body"])



                # Print out the tweet (add breaks in the for loop if you uncomment below)
                # pprint(tweet)
                # Print out keys
                # print(tweet.keys())
