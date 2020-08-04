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

try:
    print("this is a test")
    raise Exception
except Exception as e:
    print("excpeted")