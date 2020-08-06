#!/usr/bin/env python
# tweepy-bots/bots/autoreply.py

import tweepy
import logging
# from config import create_api
import time
import json
import requests
import os
from datetime import datetime

JSON_PATH = "venv/Include/city.list.json"

KEYWORDS = ["location:", "units:"]
temp_units = {"imperial": "°F", "metric": "°C"}

my_path = os.path.abspath(os.path.dirname(__file__))
abs_file_path = os.path.join(my_path, "Addons", "tweet_id.txt")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def send_api_request(location, units="metric"):
    try:
        OPENWEATHERMAP_API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
        call = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHERMAP_API_KEY}&units={units}"
        response = requests.get(call)
        data = json.loads(response.text)
    except Exception as e:
        print(e)
    return data


def parse_api_response(data, units="°C"):
    try:
        location = data["name"]
        description = data["weather"][0]["description"].title()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        temp_min = data["main"]["temp_min"]
        temp_max = data["main"]["temp_max"]
        humidity = data["main"]["humidity"]
        timezone = data["timezone"]
        # wind_speed = data["wind"]["speed"]
        # wind_deg = data["wind"]["deg"]
        sunrise = datetime.utcfromtimestamp(data["sys"]["sunrise"] + timezone).strftime('%H:%M')
        sunset = datetime.utcfromtimestamp(data["sys"]["sunset"] + timezone).strftime('%H:%M')

        infostring = f"Here is the weather results for {location}:\n\nDescription: {description}\nTemperature: {temp}{units}\nFeels like: {feels_like}{units}\nMin: {temp_min}{units}\nMax: {temp_max}{units}\nHumidity: {humidity}%\nSunrise: {sunrise}\nSunset: {sunset}"
    except Exception as e:
        print(e)
        return ""
    return infostring


def check_user_data(tweet, keywords, city_list):
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
        if not any(d['name'].title() == location_name for d in city_list):
            logger.error(f"Invalid location name received: {location_name}")
            tweet_string = f"Unfortunately there is no available forecast for: {location_name}\nThe current forcast for the Moon is: Clear skies with a 0% chance of precipitation"
            return tweet_string
    except Exception as e:
        print(e)
        return None
    try:
        units_index = status.index(keywords[1]) + 1
        units = status[units_index]
    except Exception as e:
        print(e)
    finally:
        if units != "imperial" and units != "metric":
            units = "metric"

    api_answer = send_api_request(location_name, units)
    tweet_string = parse_api_response(api_answer, temp_units[units])
    return tweet_string


def check_mentions(api, keywords, last_id, city_data):
    logger.info("Retrieving mentions")
    try:
        for tweet in tweepy.Cursor(api.mentions_timeline, since_id=last_id).items():
            last_id = max(tweet.id, last_id)
            if tweet.in_reply_to_status_id is not None:
                continue
            if any(keyword in tweet.text.lower() for keyword in keywords):
                logger.info(f"Answering to {tweet.user.name}")
                tweet_string = check_user_data(tweet, keywords, city_data)
                api.update_status(
                    status=tweet_string,
                    in_reply_to_status_id=tweet.id,
                    auto_populate_reply_metadata=True
                )
    except Exception as e:
        print(e)
    return last_id


def create_api():
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    access_token = os.getenv("ACCESS_TOKEN")
    access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e

    logger.info("API created")
    return api


def read_json(path):
    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        logger.error(e)
        return -1
    return data


def save_tweet_id(id, file_path):
    try:
        with open(file_path, 'w') as f:
            f.write(str(id))

    except Exception as e:
        logger.error(e)
        return 0
    return -1


def read_tweet_id(file_path):
    try:
        with open(file_path, 'r') as f:
            tweet_id = f.read()
    except Exception as e:
        logger.error(e)
        return 1
    return int(tweet_id)


def main():
    api = create_api()
    city_data = read_json(JSON_PATH)
    since_id = read_tweet_id(abs_file_path)
    old_id = since_id
    while True:
        since_id = check_mentions(api, KEYWORDS, since_id, city_data)
        if since_id > old_id:
            save_tweet_id(since_id, abs_file_path)
            old_id = since_id
        logger.info("Waiting...")
        time.sleep(60)


if __name__ == "__main__":
    main()
