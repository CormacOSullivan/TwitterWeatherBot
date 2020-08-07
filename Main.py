#!/usr/bin/env python

import logging
import time
import os

import TweepyAPI
import WeatherAPI

KEYWORDS = ["location:", "units:"]


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    current_path = os.path.abspath(os.path.dirname(__file__))
    tweet_file_path = os.path.join(current_path, "Addons", "tweet_id.txt")
    json_file_path = os.path.join(current_path, "Addons", "city.list.json")

    openweathermap_api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
    tweepyAPI = TweepyAPI.TweepyAPI(consumer_key, consumer_secret, access_token, access_token_secret, logger,
                                    tweet_file_path)
    weatherAPI = WeatherAPI.WeatherAPI(openweathermap_api_key, json_file_path, logger)

    city_data = weatherAPI.read_json()

    since_id = tweepyAPI.read_tweet_id()
    old_id = since_id
    while True:
        location_name, units, since_id = tweepyAPI.check_mentions(KEYWORDS, since_id, city_data)
        if location_name != "" and units == "" and since_id > old_id:
            tweet_string = f"Unfortunately there is no available forecast for: {location_name}\nHere is the current forecast for the Moon:\n\nClear skies with a 0% chance of precipitation"
            tweepyAPI.reply_to_tweet(tweet_string, since_id)
        elif location_name != "" and units != "" and since_id > old_id:
            api_answer = weatherAPI.send_api_request(location_name, units)
            tweet_string = weatherAPI.parse_api_response(api_answer, units)
            tweepyAPI.reply_to_tweet(tweet_string, since_id)
        else:
            logger.info("No weather update required")
        if since_id > old_id:
            tweepyAPI.save_tweet_id(since_id)
            old_id = since_id
        logger.info("Waiting...")
        time.sleep(60)


if __name__ == "__main__":
    main()
