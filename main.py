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

targets = [dict(client.get_user(username=u))['data'] for u in target_users]

print(f'{len(targets)} accounts to source users from')

tweets = [
    dict(client.get_users_tweets(id=u['id'], max_results=5))['data']
    for u in targets
]

print(f'{len(tweets)} tweets to target likers on')

likers = [
    client.get_liking_users(id=t['id'], max_results=10)
    for sublist in tweets
    for t in sublist
]

if len(likers) < 1:
    print('No likers found.')
    sys.exit(
        'No users found liking tweets of accounts listed. Try accounts with more followers'
    )

print(f'{len(likers)} users to like tweets on')

names = [
    u['name'] for sublist in likers if dict(sublist).get('data') is not None
    for u in sublist.get('data')
]

liker_tweets = [
    client.get_users_tweets(id=u['id'], max_results=5) for sublist in likers
    if dict(sublist).get('data') is not None for u in sublist.get('data')
]

print(f'{len(liker_tweets)} tweets found, will only like 1 tweet per user')

like_tweets = [
    client.like(tweet_id=t.get('meta')['newest_id'])
    for t in liker_tweets
    if t.get('meta')['result_count'] > 0
]

print(f'{len(like_tweets)} tweets liked!')

reply_to_users = [
    client.create_tweet(
        text=
        f"Follow me here {name} you won't regret it! I have something special for you: https://t.co/mZR4yg3g6h",
        in_reply_to_tweet_id=t.get('meta')['newest_id'])
    for (t, name) in zip(liker_tweets[:10], names[:10])
    if t.get('meta')['result_count'] > 0
]

print(f'{len(reply_to_users)} tweets replied, all done!')