import sys
import json
import argparse

# arguments
parser = argparse.ArgumentParser()
#parser.add_argument('-f', '--file', required=True,
    #help = 'name of file with tweets in json format')
parser.add_argument('-v', '--variable', default='text',
    help = 'element of tweet to summarize', 
    choices=['hashtags', 'users', 'retweets'])
parser.add_argument('-k', '--count', default=50, type=int,
    help = 'number of results to display in console')
parser.add_argument('-n', '--minimum', default=5, type=int,
    help = 'count threshold for reporting summary statistics')
args = parser.parse_args()



output = args.variable
tweetfile = 'metoo copy'
k = args.count
n = args.minimum

def top_hashtags(tweetfile, k, n):
    hashtag_list = []
    fh = open(tweetfile,'r')
    # loop over lines in file
    for line in fh:
        # load json data
        try:
            tweet = json.loads(line)
        except:
            continue       
        if 'text' not in tweet:
            continue
        # extract hashtags entities    
        hts = tweet['twitter_entities']['hashtags']['text']
        hashtag_list.append(hts)
        # for hinfo in hts:
        #     h = hinfo['text']
        #     # add hashtag to list
        #     hashtag_list[h] = 1 + hashtag_list.get(h,0)
    # sort list of hashtags
    print(hashtag_list)
    #hts = hashtag_list.items()
    hashtag_list.sort(cmp=lambda x,y: -cmp(x[1],y[1]))
    # display top k hashtags
    for ht,a in hts[:k]:
        if a>n:
            print( ht.encode('utf-8')  + "," + str(a))


def top_users(tweetfile, k, n):
    user_list = {}
    fh = open(tweetfile,'r')
    # loop over lines in file
    for line in fh:
        # load json data
        try:
            tweet = json.loads(line)
        except:
            continue       
        if 'text' not in tweet:
            continue
        # extract hashtags entities    
        u = tweet['actor']['perferredUsername']
        user_list[u] = 1 + user_list.get(u, 0)
    # sort list of hashtags
    users = user_list.items()
    users.sort(cmp=lambda x,y: -cmp(x[1],y[1]))
    # display top k hashtags
    for u,a in users[:k]:
        if a>n:
            print(u + "," + str(a))

if output == 'hashtags':
    top_hashtags(tweetfile, k, n)

if output == 'users':
    top_users(tweetfile, k, n)