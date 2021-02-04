import tweepy
import pandas as pd
import json

consumer_key = "SaWUaGZ0XVb7mdatAjaX9dlu2"
consumer_secret = "6t2nCkudBzbi2zDtApSnxELHLZlhUczY3aPqNMMASJynrZwtwz"
access_token = "977989444253900805-ShRvD2JT238AQ1jnThw9ACzttugDTv9"
access_secret = "aBRPLt7AAUyd2zLj9xuLy8QjkDUdNsm8CKFyrQEcqQTVQ"

twitter_auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
twitter_auth.set_access_token(access_token, access_secret)

twitter_api = tweepy.API(twitter_auth, wait_on_rate_limit=False, wait_on_rate_limit_notify=True)

datarows = pd.read_csv('dataset/SWM-dataset.csv', nrows=1000)
for datarow in datarows.itertuples():
    # print(datarow[1])
    try:
        tweet = twitter_api.get_status(datarow[1])
        with open('data.json', 'a', encoding='utf-8') as f:
            json.dump(tweet._json, f, ensure_ascii=False, indent=4)
    except tweepy.error.TweepError:
        print('protected tweet, skipping')