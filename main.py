import tweepy as tw
import secret_keys as sk
import sys

creds = sk.global_credentials['twitter']

client = tw.Client(bearer_token=creds['token'],
                   return_type='requests.Response',
                   wait_on_rate_limit=True)

api = tw.API(client)

target_users = input('Enter the target user(s) (separated by commas): ')

if len(target_users) > 0:
    target_users = target_users.split(',')
    target_users = [u.strip() for u in target_users]
else:
    print('No target users entered.')
    sys.exit('No target users entered.')

targets = [api.get_user(screen_name=u) for u in target_users]

#TODO figure out how to get a users tweets and pull the tweet ids of most recent tweets
tweets = []

#TODO get specific tweet's replies -> closest to the top of the thread

#TODO like replies of tweets with x specification -> closest to the top of the thread

#TODO post OF link in replies or as reply to someone?