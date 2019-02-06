import os
import json
from pprint import pprint
import networkx as nx 
import matplotlib.pyplot as plt
import codecs
import time
import datetime
import random
import time
import sys
import io
from networkx.algorithms import community

outputDir = "/Users/jayistvan/Documents/Thesis/" #Output directory
#os.system("mkdir -p %s"%(outputDir)) #Create directory if doesn't exist

def parse(graph,tweet):
	if "actor" in tweet:
		author=tweet["actor"]["preferredUsername"]		
		followers=tweet["actor"]["followersCount"]
		friends=tweet["actor"]["friendsCount"]
		if "location" in tweet["actor"]:
			if tweet["actor"]["location"]:
				location=tweet["actor"]["location"] 
			else:
				location= ""
		else: 
			location=""
		timezone=tweet["actor"]["twitterTimeZone"] if tweet["actor"]["twitterTimeZone"] else ""
		utc=tweet["actor"]["utcOffset"]  if tweet["actor"]["utcOffset"] else ""

		#print(tweet["verb"])
		#return 0
		other_users=[]
		if "verb" in tweet:
			if tweet["verb"] == "share":
				other_users.append(tweet["object"]["actor"]["preferredUsername"])
				#print(other_users)
			#sys.exit(1)

		try:
			graph.node[author]["tweets"]+=1
		except: #if not author in graph.node:
			graph.add_node(author,followers="followers") #remember still have to add back the other pieces of info
		
		for target in other_users:
			try:
				graph[author][target]["weight"]+=1
			except:
				graph.add_edge(author,target,weight=1)


graph = nx.DiGraph()

# # Specify which directory the day tweet files are in
# tweet_files_dir = 'dayonemetoo'
# # Get all the tweet filenames
# tweet_files = sorted(os.listdir(tweet_files_dir))
# # Prepend directory to each tweet filename
# tweet_files = [tweet_files_dir+'/'+filename for filename in tweet_files]

tweet_file = 'metoohistorical/2018-03-06.txt'

# Loop over all tweet files
# for tweet_file in tweet_files:
    # Open individual day tweet file
    with open(tweet_file, 'r') as f:
   # io.open(tweet_file, 'r', encoding='windows-1252') as f:
        # print(f)
        #print(f.name)
        # Go through each tweet in the tweet file
        linenumber = 1
        for line in f:
            # print(line)
            # Load tweet (make sure to strip newline character from end of line)
            # `tweet` is a dictionary object with many keys
            try:
                tweet = json.loads(line.strip("\n"))
            except:
                print("parse error on line " + str(linenumber))

            linenumber += 1
            #print("about to parse")
            parse(graph,tweet)
            #day_tweets.append(tweet)
        #all_tweets.append(day_tweets)

 communities_generator = communities.label_propagation_communities(graph)
        
filename=outputDir+"overall_%s.graphml"%int(time.time())
print("Writing graphml file to {0}...".format(filename))
nx.write_graphml(graph,filename,prettyprint=True)
print("Done.")