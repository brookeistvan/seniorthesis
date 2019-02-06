import os
import pytz
import tarfile
import numpy as np
import scipy.sparse as ss
from datetime import datetime
from itertools import combinations
import nltk
from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
exclude = set(punctuation)
exclude.remove('#')
stop_words = stopwords.words('english')
tknzr = TweetTokenizer(preserve_case=False,strip_handles=True,reduce_len=False)


# ------------------------------------------------------------------------------
# ------------------------------ GENERAL FUNCTIONS -----------------------------
# ------------------------------------------------------------------------------
def update_key2freq(key2freq, key, freq=1):
    if key in key2freq:
        key2freq[key] += freq
    else:
        key2freq[key] = freq

def add_to_dict(key2value, key, value):
    """
    OUTPUT
    ------
    Adds value to key2value[key] if key exists, else initializes key2value[key]
    with that value as a set. If value is a list, updates the set with the list
    """
    if key in key2value:
        if type(value) is not list:
            key2value[key].add(value)
        else:
            key2value[key].update(value)
    else:
        key2value[key] = set()
        if type(value) is not list:
            key2value[key].add(value)
        else:
            key2value[key].update(value)

def enumerate_pairs(values, ordered=False):
    if len(values) > 1:
        pairs = combinations(values, 2)
        if ordered:
            pairs = [tuple(list(pair)) for pair in pairs]
        else:
            pairs = [tuple(sorted(list(pair))) for pair in pairs]
        return pairs
    else:
        return list()

def load_paths(paths_file='data/paths.csv'):
    """
    INPUT
    -----
    paths_file: str, filename of CSV containing path_name,path pairs. File must
                be newline delimited

    OUTPUT
    ------
    path_name2path: dict, keys are names for necessary paths, values are the
                    file paths
    """
    path_name2path = dict()
    with open(paths_file, 'r') as f:
        for line in f:
            path_name,path = line.strip().split(',')
            path_name2path[path_name] = path
    return path_name2path

def tar_and_cleanup(archive_name, file_names, write='gz'):
    with tarfile.open(archive_name, 'w:gz') as t:
        for filename in file_names:
            t.add(filename)
    for filename in file_names:
        os.remove(filename)

# ------------------------------------------------------------------------------
# ------------------------------- TWEET FUNCTIONS ------------------------------
# ------------------------------------------------------------------------------
def is_valid_tweet(tweet):
    """
    INPUT
    -----
    tweet: str, not necessarily a tweet

    OUTPUT
    ------
    bool, returns False if tweet hasn't been decoded to a dict
    """
    if type(tweet) is not dict:
        return False
    else:
        return True

def get_tweet_time(tweet, timezone_before=None, timezone_after=None):
    """
    INPUT
    -----
    tweet: dict, Twitter tweet object
    timezone_before: pytz.timezone, expected timezone of tweet time
    timezone_after: pytz.timezone, desired timezone of tweet time

    OUTPUT
    ------
    tweet_datetime: datetime, tweet time as a datetime. If timezone_before and
                    timezone_after are not None, returns datetime with timezone
    """
    tweet_time = tweet['postedTime'] #'created_at'
    try:
        tweet_datetime = datetime.strptime(tweet_time,'%Y-%m-%dT%H:%M:%S.000Z')
    except:
        print('date time error')
        tweet_datetime = ""
    if timezone_before is not None and timezone_after is not None:
        tweet_datetime = timezone_before.localize(tweet_datetime)
        tweet_datetime = tweet_datetime.astimezone(timezone_after)
    return tweet_datetime

def get_tweet_urls(tweet):
    try:
        link_dicts = tweet['twitter_entities']['urls']
    except KeyError:
        return list()
    if len(link_dicts) == 0:
        return list()

    links = set()
    for link_dict in link_dicts:
        try:
            link = link_dict['expanded_url']
        except KeyError:
            link = link_dict['url']
        links.add(link)
    return links

def get_tweet_hashtags(tweet):
    try:
        hashtag_dicts = tweet['twitter_entities']['hashtags']
    except KeyError:
        return list()
    if len(hashtag_dicts) == 0:
        return list()

    hashtags = {hashtag_dict['text'].lower() for hashtag_dict in hashtag_dicts}
    return hashtags

def is_retweet(tweet, retweet_type='retweet'):
    """
    INPUT
    -----
    tweet: dict, Twitter tweet object
    retweet_type: str, type of retweet interaction. Options: 'retweet','quote'

    OUTPUT
    ------
    bool, whether the given tweet is a retweet
    """
    if retweet_type == 'retweet':
        retweet_field = 'retweeted_status'
    elif retweet_type == 'quote':
        retweet_field = 'quoted_status'
    if retweet_field in tweet:
        return True
    else:
        return False

def is_related_to_seen_tweet(tweet, seen_tweets):
    """
    INPUT
    -----
    tweet: dict, Twitter tweet object
    seen_tweets: dict, tweets to check relation to

    OUTPUT
    ------
    bool, whether tweet is a retweet of, in reply to, or a quote of any tweet in
          seen_tweets
    """
    in_reply_to_id = str(tweet['inReplyTo'].split('/')[5])
    if (in_reply_to_id is not None) and (in_reply_to_id in seen_tweets):
        return True
    elif (verb == "share") and (tweet['object']['id']) in seen_tweets:
        return True
    elif ('twitter_quoted_status' in tweet) and (tweet['twitter_quoted_status']['id']) in seen_tweets:
        return True
    else:
        return False

def get_tweet_interaction_ids(tweet, unique_id=True):
    """
    INPUT
    -----
    tweet: dict, Twitter tweet object

    OUTPUT
    ------
    retweets,mentions,quotes: set, user IDs of those interacted with in tweet
                              through each interaction type
    """
    retweets = get_retweet_interaction_ids(tweet, retweet_type='retweet',
                                           unique_id=unique_id)
    quotes = get_retweet_interaction_ids(tweet, retweet_type='quote',
                                         unique_id=unique_id)
    mentions = get_mention_interaction_ids(tweet, unique_id=unique_id)
    return retweets,mentions,quotes

def get_retweet_interaction_ids(tweet, retweet_type='retweet', unique_id=True):
    """
    INPUT
    -----
    tweet: dict, Twitter tweet object
    retweet_type: str, type of retweet interaction. Options: 'retweet','quote'

    OUTPUT
    ------
    user_ids: set, user IDs of those interactions
    """
    if retweet_type == 'retweet':
        retweet_field = 'retweeted_status'
    elif retweet_type == 'quote':
        retweet_field = 'quoted_status'
    if retweet_field in tweet:
        if unique_id:
            user_id = tweet[retweet_field]['object']['actor']['id']
        else:
            user_id = tweet[retweet_field]['object']['actor']['preferedUsername']
        user_ids = {user_id}
    else:
        user_ids = set()
    return user_ids

def get_mention_interaction_ids(tweet, only_reply=False, unique_id=True):
    """
    INPUT
    -----
    tweet: dict, Twitter tweet object
    only_reply: bool, If true only returns the ID of the in reply to user

    OUTPUT
    ------
    user_ids: set, user IDs of those mentioned in tweet (including in reply)
    """
    user_ids = set()
    # Get in reply to user (is this user in mentions?)
    if "verb" in tweet:
            if tweet["verb"] == "share":
                if unique_id:
                    in_reply_to_user_id = tweet['object']['actor']['id'.split(':')[2]]
                else:
                    if "object" in tweet:
                        in_reply_to_user_id = tweet['object']['actor']['preferredUsername']
                    else:
                        in_reply_to_user_id = ""
                if in_reply_to_user_id is not None:
                    user_ids.add(in_reply_to_user_id)
                    if only_reply:
                        return user_ids
    # Get all mentioned users
    if "twitter_entities" in tweet:
        user_mentions = tweet['twitter_entities']['user_mentions']
    else:
        user_mentions = ""
    if len(user_mentions) > 0:
        for user_mention in user_mentions:
            if unique_id:
                mentioned_id = user_mention['id_str']
            else:
                try:
                    mentioned_id = user_mention['screen_name']
                except:
                    print('user mentions error')
                    mentioned_id = ""
            user_ids.add(mentioned_id)
    return user_ids

def clean_tweet(tweet, stop_removal=True):
    """
    INPUT
    -----
    Cleans tweet text for extracting unigrams. Steps for cleaning:
    1. Tokenize text using NLTK tweet tokenizer
        a. Remove handles
        b. Tokenize tweet
        c. Lowercase unigrams (except emoticons)
    2. Do basic filtering of 'rt' and URLs from tweet (not extensive)
    3. Remove stop tokens (unicode punctuation not captured Python defaults),
       tokens of less than length 2 if they are not stop words or digits, and
       lone hashtag symbols ('#')
    4. Remove stop words from tweet if desired (NLTK stop word list)
    5. Remove punctuation from tweet, except hashtag (#) symbol

    OUTPUT
    ------
    cleaned_text, list of strings
        List of unigrams from tweet following above processing steps
    """
    try:
        tweet_text = tweet['body']
    except KeyError:
        print('tweet text error')
        # tweet_text = tweet['text']
    # Stop tokens: left/right quote,right apostrophes,ellipse,em dash
    stop_tokens = set(['\u201c','\u201d','\u2018','\u2019','\u2026','\u2013'])
   
    # Tokenize the tweet text using NLTK
    tokenized_text = tknzr.tokenize(tweet_text)
    # Remove 'rt', links, stop tokens, tokens less than length two that are not
    # stop words or digits, and lone hashtag symbols
    filtered_text = [gram for gram in tokenized_text if (gram != 'rt')
                    and ('http' not in gram) and ('//t.co' not in gram)
                    and (gram not in stop_tokens) and (len(gram) > 2
                    or (gram in stop_words or gram.isdigit())) and (gram != '#')]
    # Remove stop words
    if stop_removal is True:
        filtered_text = [gram for gram in filtered_text if gram not in stop_words]
    # Remove multiple instances of '#' in front of a hashtag
    for gram_n,gram in enumerate(filtered_text):
        try:
            if gram[0] == '#' and gram[1] == '#':
                last_hashtag_index = max([i for i,c in enumerate(gram) if c=='#'])
                filtered_text[gram_n] = gram[last_hashtag_index:]
        except IndexError:
            continue
    # Join text to one string, remove punctuation, join back to list
    text = ' '.join(filtered_text)
    text_chars_noPunct = [char for char in text if char not in exclude]
    text_noPunct = "".join(text_chars_noPunct)
    # Split back to list of words
    cleaned_text = text_noPunct.strip().split()
    return cleaned_text


# ------------------------------------------------------------------------------
# ------------------------------ NETWORK FUNCTIONS -----------------------------
# ------------------------------------------------------------------------------
def write_edgelist(network, filename, weight=False, delimiter='\t'):
    """
    INPUT
    -----
    network: networkx graph object, network to use to update edge

    OUTPUT
    ------
    Writes the edge list of network to filename
    """
    edges = network.edges()
    with open(filename, 'w') as outfile:
        for edge in edges:
            source = edge[0]
            target = edge[1]
            if weight is False:
                outfile.write(source+delimiter+target)
            else:
                weight = str(network[source][target]['weight'])
                outfile.write(source+delimiter+target+delimiter+weight)
            outfile.write('\n')

def update_weighted_edge(network, source, target, weight=1):
    """
    INPUT
    -----
    network: networkx graph object, network to use to update edge

    OUTPUT
    ------
    Updates the weight of the edge from source to target by specified weight.
    If the edge does not exist, adds the edge to the network with given weight.
    """
    if network.has_edge(source, target):
        network[source][target]['weight'] += 1
    else:
        network.add_edge(source, target, weight=1)


# ------------------------------------------------------------------------------
# ----------------------------- DOC-TERM FUNCTIONS -----------------------------
# ------------------------------------------------------------------------------
def save_sparse_csr(filename, matrix, row_label, column_label):
    """
    INPUT
    -----

    OUTPUT
    ------
    """
    np.savez(filename, data=matrix.data ,indices=matrix.indices,
             indptr=matrix.indptr, shape=matrix.shape, row_label=row_label,
             column_label=column_label)

def load_sparse_csr(filename):
    """
    INPUT
    -----

    OUTPUT
    ------

    """
    loader = np.load(filename)
    return ss.csr_matrix((loader['data'], loader['indices'], loader['indptr']),
                          shape=loader['shape']), loader['row_label'],loader['column_label']

def build_doc_term(terms, doc2terms):
    """

    """
    # Index the doc-term matrix
    term2index = {term:j for j,term in enumerate(sorted(list(terms)))}
    doc2index = {doc:i for i,doc in enumerate(sorted(list(doc2terms.keys())))}
    doc_term = ss.dok_matrix((len(doc2terms), len(terms)))
    # Build matrix using indices
    for doc in doc2terms:
        doc_index = doc2index[doc]
        term_indices = [term2index[term] for term in doc2terms[doc]]
        for term_index in term_indices:
            doc_term[doc_index, term_index] += 1
    # Convert sparse matrix to CSR representation
    doc_term = ss.csr_matrix(doc_term)
    return doc_term

def subset_nonzero_columns(doc_term):
    """

    """
    col_sums = np.squeeze(np.asarray(doc_term.sum(axis=0)))
    col_indices = col_sums != 0
    sub_doc_term = doc_term[:,col_indices]
    return sub_doc_term,col_indices

def subset_doc_term_by_rows(doc_term, doc_indices, doc_labels, word_labels):
    """

    """
    # Subset by rows
    sub_doc_term = doc_term[doc_indices]
    # Subset by nonzero columns
    sub_doc_term,word_indices = subset_nonzero_columns(sub_doc_term)
    # Subset the row and column labels
    sub_docs = np.array(doc_labels)[doc_indices]
    sub_words = np.array(word_labels)[word_indices]

    return sub_doc_term,sub_docs,sub_words

def adjust_doc_term(doc_term, col_labels, full_col_labels):
    """
    Adjust size of doc_term with col_labels to fit the size and column labels
    of the document-term matrix with column labels full_col_labels
    """
    adjusted_doc_term = ss.dok_matrix((doc_term.shape[0],len(full_col_labels)))
    full_label2index = {term : index for index,term in enumerate(full_col_labels)}
    # Map the relative indices of sub doc-term to indices of full doc-term
    rel_indices = [n for n,term in enumerate(col_labels) if term in full_label2index]
    adjusted_indices = [full_label2index[col_labels[n]] for n in rel_indices]
    # Expand doc_term by filling in appropriate subset of expanded_doc_term
    adjusted_doc_term[:,adjusted_indices] = doc_term[:,rel_indices]
    return ss.csr_matrix(adjusted_doc_term)
