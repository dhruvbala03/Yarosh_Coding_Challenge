
from getpass import getpass
import praw
from secret_stuff import client_keys
import pandas as pd
from textblob import TextBlob
from statistics import mean


# define user agent
user_agent = "praw_scraper_1.0"


# reddit login
print("Enter Reddit username:")
username = input()  # Icy_Paramedic_154
password = getpass(prompt="Enter Reddit password:\n")

# create an instance of reddit class
print("Logging into reddit...")
reddit = praw.Reddit (
    username = username,
    password = password,
    client_id = client_keys.get_client_id(),
    client_secret = client_keys.get_client_secret(),
    user_agent = user_agent
)

# get subreddit instance
subreddit_name = "recovery"
subreddit = reddit.subreddit(subreddit_name)


# define columns
titles = []
authors = []
selftexts = []
scores = []
num_commentss = []


# scrape baseline data
print("Extracting data...")
for submission in subreddit.new(limit=None):
    if submission.author == None:
        continue  # exclude posts with no author
    titles.append(submission.title)
    authors.append(submission.author.name)
    selftexts.append(submission.selftext)
    scores.append(submission.score) #upvotes
    num_commentss.append(submission.num_comments)


# compile data to dataframe
df = pd.DataFrame()
df["Title"] = titles
df["Author"] = authors
df["Post Body"] = selftexts
df["Score (Upvotes-Downvotes)"] = scores
df["Num Comments"] = num_commentss


# filter data
df = df.loc[df["Post Body"] != ""]  # exclude empty posts
df = df.head(100)


# extract post sentiments
post_sentiments = []
for index,row in df.iterrows():
    post = row["Post Body"]
    blob = TextBlob(post)
    post_sentiments.append(blob.sentiment.polarity)  # -1 to 1, more positive means happier sentiment

df["Post Sentiment (-1 to 1)"] = post_sentiments


# export data as csv
df.to_csv("output/recovery_posts.csv")


print("Done!\n\nSee output/recovery_posts.csv\n")
