#!/usr/bin/env python
# tweepy-bots/bots/autoreply.py

import tweepy


class TweepyAPI:
    temp_units = {"imperial": "°F", "metric": "°C"}

    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, logger=None,
                 tweet_id_path=None):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.logger = logger
        self.tweet_id_path = tweet_id_path
        self.api = self.create_api()

    def check_user_data(self, tweet, keywords, city_list):
        """
        Parses the tweet received for correct formatting and values for location and units and returns the location
        and units values parsed from the tweet
        :param tweet: the object of the latest tweet received by the system
        :param keywords: list of keywords that are used to check that the tweet has corrected formatting and parameters
        :param city_list: dictionary that holds the data parsed from the city_list.json file
        :return: location -> string representing the users requested location if it was found in city_list
                 units -> string representing the users requested units from their tweet
                 -1 -> If an error has occurred
        """
        units = ""
        status = tweet.text.lower().split()
        try:
            location_index = status.index(keywords[0]) + 1
            cnt = 0
            location_name = ""
            while True:
                location_name += status[location_index + cnt] + " "
                if "!" in status[location_index + cnt]:
                    break
                cnt += 1
            location_name = location_name[:-2].title()
            if not any(d['name'].title() == location_name for d in city_list): # Check tweet contained a valid location
                self.logger.error(f"Invalid location name received: {location_name}")
                return location_name, -1
        except (IndexError, TypeError) as e:
            self.logger.error(e)
            self.logger.error(f"Invalid tweet received: {tweet.text}")
            return -1, -1

        try:
            units_index = status.index(keywords[1]) + 1
            units = status[units_index]
        except IndexError as e:
            self.logger.error(f"Invalid units value received")
        finally:
            if units != "imperial" and units != "metric":
                units = "metric"
        return location_name, units

    def check_mentions(self, keywords, last_id, city_data):
        """
        Checks if the bot's twitter account has been mentioned in any new tweets, then checks the list until a tweet
        containing the required keywords are found. If they are found calls check_user_data to parse the tweet for the
        required information to be used in openweathermapapi call
        :param keywords: list of strings representing keywords that should be found in compatible tweets
        :param last_id: The id number of the last tweet the system replied to
        :param city_data: dictionary of data read from city_list.json file
        :return: location -> string representing the users requested location name parsed from check_user_data call
                 units -> string representing the users requested units parsed from check_user_data call
                 -1 -> If an error has occurred
        """
        self.logger.info("Retrieving mentions")
        try:
            # Loops through mentioned tweets that are after the latest bot replied tweets id (last_id) for a tweet
            # that contains the required keywords and then begins parsing that tweet
            for tweet in tweepy.Cursor(self.api.mentions_timeline, since_id=last_id).items():
                last_id = max(tweet.id, last_id)
                if tweet.in_reply_to_status_id is not None:
                    continue
                if any(keyword in tweet.text.lower() for keyword in keywords):
                    self.logger.info(f"Answering to {tweet.user.name}")
                    location_name, units = self.check_user_data(tweet, keywords, city_data)
                    return location_name, units, last_id

        except Exception as e:
            self.logger.error("An unexpected error has occurred")
            self.logger.error(e)
        return -1, -1, last_id

    def reply_to_tweet(self, tweet_string, tweetID):
        """
        Sends a reply of tweet_string to the tweet that was sent to the bot with an ID of tweetID
        :param tweet_string: Body of the reply tweet being sent
        :param tweetID: ID of the tweet to be replied to
        :return:
        """
        self.api.update_status(
            status=tweet_string,
            in_reply_to_status_id=tweetID,
            auto_populate_reply_metadata=True
        )

    def create_api(self):
        """
        Creates the api object using the keys and tokens environment variable's values and returns the object
        :return: api -> object used for tweepy interaction with the twitter bot's account
        """
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True,
                         wait_on_rate_limit_notify=True)
        try:
            api.verify_credentials()
        except Exception as e:
            self.logger.error("Error creating API", exc_info=True)
            return -1

        self.logger.info("API created")
        return api

    def save_tweet_id(self, tweet_id):
        """
        Saves the latest replied tweet's ID to a file to prevent errors with duplicate reply attempts
        :param tweet_id: ID number of latest replied tweet
        :return:
        """
        try:
            with open(self.tweet_id_path, 'w') as f:
                f.write(str(tweet_id))
        except (IOError, ValueError, EOFError) as e:
            self.logger.error(e)
        except Exception as f:
            self.logger.error("An Unexpected error has occurred: ", f)

    def read_tweet_id(self):
        """
        Reads in the last replied tweet's ID from the storage file so the system knows the starting point of the required
        replies
        :return: tweet_id -> ID number of the last replied tweet
                 -1 -> If an error has occurred
        """
        try:
            with open(self.tweet_id_path, 'r') as f:
                tweet_id = f.read()
        except (IOError, ValueError, EOFError) as e:
            self.logger.error(e)
            return -1
        except Exception as f:
            self.logger.error("An Unexpected error has occurred: ", f)
            return -1
        return int(tweet_id)
