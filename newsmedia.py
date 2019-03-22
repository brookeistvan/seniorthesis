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

# up to AOL from http://www.journalism.org/2011/05/09/top-25/ and some from https://mashable.com/2013/04/08/breaking-news-twitter/#tGq4d1cjvOqx and https://www.adweek.com/digital/twitter-breaking-news/
newsusernamelist = ["nytimes", "washingtonpost", "USATODAY", "WSJ", "latimes", "NYDailyNews", "nypost", "BostonGlobe", "sfchronicle", "chicagotribune", "DailyMailUK", "MailOnline", "MSNBC", "CNN", "abcnews", "FoxNews", "CBSNews", "BBCNews", "Reuters", "HuffPost", "Yahoo", "people", "AOLNews", "BuzzFeedNews", "AM2DM", "amjoyshow", "cnnbrk", "Newsweek", "BBCBreaking", "WSJbreakingnews", "ReutersLive", "CBSTopNews", "AJELive", "SkyNewsBreak", "ABCNewsLive", "NRO", "SportsCenter", "espn", "BBCWorld", "TheEconomist", "BreakingNews", "CBSTopNews", "BreakingTweets", "BreakingNewsStorm", "diggtop", "ajplus"] 
# many broken up liberal news accounts where as conservatives mainly listen to fox news 

dates = []
news_count_by_day = []
tweet_count_by_day = []
for tweet_file in tweet_files:
    dates.append(str((tweet_file.split(".")[0]).split("/")[1]))
    with open(tweet_file, 'r') as f:
        day_tweets = []
        newsdict = {}
        for name in newsusernamelist:
            newsdict.update({name: 0})

        # Go through each tweet in the tweet file
        for line in f:
                try:
                    tweet = json.loads(line.strip("\n"))
                except:
                    print("Load error")
                    continue

                # if news outlet tweeted add count
                if "actor" in tweet:
                    if "preferredUsername" in tweet["actor"]:
                        if tweet["actor"]["preferredUsername"] in newsdict:
                            newsdict[tweet["actor"]["preferredUsername"]] += 1

                # if someone retweeted news outlet, add to count
                if "verb" in tweet:
                    if tweet["verb"] == "share":
                        if "object" in tweet:
                            if "actor" in tweet["object"]:
                                if "preferredUsername" in tweet["object"]["actor"]:
                                    if tweet["object"]["actor"]["preferredUsername"] in newsdict:
                                        newsdict[tweet["object"]["actor"]["preferredUsername"]] += 1

                # if someone mentioned the news outlet, add to count 
                if "twitter_entities" in tweet:
                    if "user_mentions" in tweet["twitter_entities"]:
                        for mention in tweet["twitter_entities"]["user_mentions"]:
                            if "screen_name" in tweet["twitter_entities"]["user_mentions"]:
                                if tweet["twitter_entities"]["user_mentions"]["screen_name"] in newsdict:
                                    newsdict[tweet["twitter_entities"]["user_mentions"]["screen_name"]] += 1
                day_tweets.append(tweet)
        tweet_count_by_day.append(len(day_tweets))
        news_count_by_day.append(sum(newsdict.values()))


# print(news_count_by_day)
# print(tweet_count_by_day)

del tweet_count_by_day[0]
del news_count_by_day[0]
# retweet_count_by_day.remove(0)
# quote_count_by_day.remove(0)
# reply_count_by_day.remove(0)

d = np.array(tweet_count_by_day, dtype=np.float)
a = np.array(news_count_by_day, dtype=np.float)
# b = np.array(quote_count_by_day, dtype=np.float)
# c = np.array(reply_count_by_day, dtype=np.float)

fraction_of_news = a/d
# fraction_of_quotes = b/d
# fraction_of_replies = c/d 

# dates.remove('')
# x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]
# plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b'))
# plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
# plt.plot(x, fraction_of_news)
# plt.plot(x, np.log(tweet_count_by_day))
# plt.gcf().autofmt_xdate()
# plt.show()
print("mean fraction of news")
print(np.mean(fraction_of_news))

dates.remove('')
x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]

fig, ax1 = plt.subplots()

color = 'red'
ax1.set_xlabel('time')
ax1.set_ylabel('log number of tweets', color=color)
ax1.plot(x, np.log(tweet_count_by_day), color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'blue'
ax2.set_ylabel('log number of tweets from news outlets', color=color)  # we already handled the x-label with ax1
ax2.plot(x, np.log(news_count_by_day), color=color)
ax2.tick_params(axis='y', labelcolor=color)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())
plt.gcf().autofmt_xdate()
fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()