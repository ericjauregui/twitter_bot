import tweepy as tw
import secret_keys as sk
import sys

creds = sk.global_credentials['twitter']

client = tw.Client(bearer_token=creds['bearer_token'],
                   access_token=creds['access_token'],
                   access_token_secret=creds['access_secret'],
                   consumer_key=creds['consumer_key'],
                   consumer_secret=creds['consumer_secret'],
                   return_type=dict,
                   wait_on_rate_limit=True)

target_users = input('Enter the target user(s) (separated by commas): ')

if len(target_users) > 0:
    target_users = target_users.split(',')
    target_users = [u.strip() for u in target_users]
else:
    print('No target users entered.')
    sys.exit('No target users entered.')

targets = [client.get_user(username=u)['data'] for u in target_users]

print(f'{len(targets)} accounts to target')

tweets = [
    client.get_users_tweets(id=u['id'], max_results=3)['data'] for u in targets
]

print(f'{len(tweets)} tweets to target likers on')

likers = [
    client.get_liking_users(id=t['id'], max_results=10)
    for sublist in tweets
    for t in sublist
]

print(f'{len(likers)} users to like tweets on')

liker_tweets = [{
    'tweets': client.get_users_tweets(id=u['id'], max_results=3),
    'user_id': u['id']
} for sublist in likers if sublist.get('data') is not None
                for u in sublist.get('data')]

print(f'{len(liker_tweets)} tweets found, will only like 3 tweets per user')

like_tweets = [
    client.like(tweet_id=t['id']) for sublist in liker_tweets
    if sublist['tweets'].get('data') is not None
    for t in sublist['tweets'].get('data')[:3]
]

print(f'{len(like_tweets)} tweets liked!')

reply_to_users = [
    client.create_tweet(
        text=
        "Follow me here you won't regret it! I have something special for you: https://t.co/mZR4yg3g6h",
        in_reply_to_tweet_id=t['id'])
    for sublist in liker_tweets[:5]
    for t in sublist['tweets'].get('data')[0]
    if sublist['tweets'].get('data') is not None
]

print(f'{len(reply_to_users)} tweets replied, all done!')