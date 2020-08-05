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
OPENWEATHERMAP_API_KEY = "f7fc9317623016c29feedd9488e0bbee"
KEYWORDS = ["location:"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def send_api_request(location, units="metric"):
    call = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHERMAP_API_KEY}&units={units}"
    response = requests.get(call)
    data = json.loads(response.text)
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


def check_mentions(api, keywords, since_id, city_data):
    logger.info("Retrieving mentions")
    new_since_id = since_id

    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to {tweet.user.name}")
            status = tweet.text.lower().split()
            try:
                location_index = status.index(keywords[0]) + 1
                # if status[location_index] not in city_data:
                #     raise Exception
                api_answer = send_api_request(status[location_index])
                tweet_string = parse_api_response(api_answer)
            except Exception as e:
                print(e)
                logger.error("Invalid tweet received")
                tweet_string = f"Unfortunately there is no available forecast for: {status[location_index]}\nThe current forcast for the Moon is: Clear skies with a 0% chance of precipitation"

            api.update_status(
                status=tweet_string,
                in_reply_to_status_id=tweet.id,
                auto_populate_reply_metadata=True
            )
    return new_since_id


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
        with open(path) as f:
            data = json.load(f)
    except Exception as e:
        logger.error(e)
        return -1
    return data


def main():
    api = create_api()
    city_data = read_json(JSON_PATH)
    since_id = 1
    while True:
        since_id = check_mentions(api, KEYWORDS, since_id, city_data)
        logger.info("Waiting...")
        time.sleep(60)


if __name__ == "__main__":
    main()
