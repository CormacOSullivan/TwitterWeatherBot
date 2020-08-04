# import tweepy
#
# # Authenticate to Twitter
# auth = tweepy.OAuthHandler("EKOaSg962MqCgSq2vCWhiJWMC",
#     "cvBEvjJFRIcnkEvVW1pqGL0PLRrTEVWO704k8o68ZuhJ1do1lY")
# auth.set_access_token("1288894648547598337-Fw6ldmhks4fswO9G427Su9FG5akw2p",
#     "aC40yi31XX35HFFeOhmTLlhbTdvO89sLprdiFWCCJejee")
#
# api = tweepy.API(auth)
#
# try:
#     api.verify_credentials()
#     print("Authentication OK")
# except:
#     print("Error during authentication")
import os
# os.environ['CONSUMER_KEY'] = 'EKOaSg962MqCgSq2vCWhiJWMC'
# os.environ['CONSUMER_SECRET'] = 'cvBEvjJFRIcnkEvVW1pqGL0PLRrTEVWO704k8o68ZuhJ1do1lY'
# os.environ['ACCESS_TOKEN'] = '1288894648547598337-Fw6ldmhks4fswO9G427Su9FG5akw2p'
# os.environ['ACCESS_TOKEN_SECRET'] = 'aC40yi31XX35HFFeOhmTLlhbTdvO89sLprdiFWCCJejee'

consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

print(consumer_key, consumer_secret, access_token, access_token_secret)
