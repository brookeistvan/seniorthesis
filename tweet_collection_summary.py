import os
import csv
import json
from datetime import datetime

from helper_funcs import *

# ------------------------------------------------------------------------------
# ------------------------------- Preliminaries --------------------------------
# ------------------------------------------------------------------------------
hashtags = ['metoo'] #blacklivesmatter

# Assumed that there is a directory of data, which contains directories of
# hashtags. In each hashtag directory are tweet files for that hashtag
#. ex. data/blacklivesmatter contains tweet files of JSON tweet objects
data_dir = 'dec 11'      # data   # where hashtag directories are
summary_dir = 'dec 11 summary' #output_dir # where to output summaries (make sure directory exists)

# Make output folder for each hashtag
for hashtag in hashtags:
    if hashtag not in os.listdir(summary_dir):
        os.mkdir(summary_dir+'/'+hashtag)

# ------------------------------------------------------------------------------
# ------------------------------- Main Statistics ------------------------------
# ------------------------------------------------------------------------------
for hashtag in hashtags:
    hashtag_dir = '{}/{}'.format(data_dir, hashtag)
    hashtag_files = sorted(os.listdir(data_dir))
    hashtag_files = [data_dir+'/'+f for f in hashtag_files]

    date_n_tweets = []
    term2freq = dict()
    url2freq = dict()
    mention2freq = dict()
    interaction2freq = dict()
    hashtag2freq = dict()
    hashtag_pair2freq = dict()


    # ------------------------ 1st pass for statistics -------------------------
    print('Summarizing {} tweets'.format(hashtag))
    for day_file in hashtag_files:
    #day_file = 'metoo/2017-20-16.txt'
        n_tweets = 0
        with open(day_file, 'r') as f:
            for line in f:
                try:
                    tweet = json.loads(line.strip("\n"))
                except:
                    print("parse error")
                    continue
                #tweet = json.loads(line.strip())

                # tweet_date = get_tweet_time(tweet)
                # if tweet_date is not "":
                #     day_date = tweet_date.strftime('%y-%m-%d')

                n_tweets += 1

                # Get words
                terms = clean_tweet(tweet)
                for term in terms:
                    update_key2freq(term2freq, term)
                # Get URLs
                urls = get_tweet_urls(tweet)
                for url in urls:
                    update_key2freq(url2freq, url)

                # Get interactions in tweet
                retweets,mentions,quotes = get_tweet_interaction_ids(tweet, unique_id=False)
                for mention in mentions:
                    update_key2freq(mention2freq, mention)
                if "actor" in tweet:
                    tweet_user = tweet['actor']['preferredUsername']
                interactions = list(retweets.union(mentions).union(quotes))
                directed_interactions = [(tweet_user, j) for j in interactions]
                for interaction in directed_interactions:
                    update_key2freq(interaction2freq, interaction)

                # Get hashtags and hashtag co-occurrences
                tweet_hashtags = get_tweet_hashtags(tweet)
                for tweet_hashtag in tweet_hashtags:
                    update_key2freq(hashtag2freq, tweet_hashtag)
                hashtag_pairs = enumerate_pairs(tweet_hashtags)
                for hashtag_pair in hashtag_pairs:
                    update_key2freq(hashtag_pair2freq, hashtag_pair)

                # date_n_tweets.append((day_date, n_tweets)) # originally two tabs left

    # --------------------------- Output statistics ----------------------------
    output_dir = '{}/{}'.format(summary_dir, hashtag)
    timeline_f = '{}/timeline.csv'.format(output_dir)
    # with open(timeline_f, 'w') as outfile:
    #     for date,n_tweets in date_n_tweets:
    #         outfile.write('{},{}\n'.format(date, n_tweets))

    freq_files = ['top_terms', 'top_urls', 'top_mentions', 'top_hashtags',
                  'edgelist', 'top_hashtag_pairs']
    freq_dicts = [term2freq, url2freq, mention2freq, hashtag2freq,
                  interaction2freq, hashtag_pair2freq]
    for key2freq,freq_file in zip(freq_dicts, freq_files):
        key_freqs = sorted(key2freq.items(), key=lambda x:x[1], reverse=True)
        out_f = '{}/{}.csv'.format(output_dir, freq_file)
        with open(out_f, 'w') as outfile:
            if freq_file == 'top_hashtag_pairs':
                for n,((p1,p2), freq) in enumerate(key_freqs):
                    outfile.write(str(u'{},{},{},{}\n'.format(n+1,p1,p2,freq).encode('utf-8')))
            elif freq_file == 'edgelist':
                for (i,j), w in key_freqs:
                    outfile.write(str(u'{},{},{}\n'.format(i,j,w).encode('utf-8')))
            else:
                for n,(key,freq) in enumerate(key_freqs):
                    outfile.write(str(u'{},{},{}\n'.format(n+1,key,freq).encode('utf-8')))
