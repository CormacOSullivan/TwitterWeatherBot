#!/usr/bin/env python
# tweepy-bots/bots/autoreply.py

import tweepy
import logging
#from config import create_api
import time
import json
import requests
import os




BOT_HANDLE = ""
JSON_PATH = "venv/Include/city.list.json"
OPENWEATHERMAP_API_KEY = "f7fc9317623016c29feedd9488e0bbee"
KEYWORDS = ["location:"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def send_api_request(location):
    print(location)
    call = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHERMAP_API_KEY}"
    response = requests.get(call)
    data = json.loads(response.text)
    return data

def parse_api_response(data):
    print(data)
    location = data["name"]
    description = data[0]["weather"]["description"]
    temp = data[0]["main"]["temp"]
    feels_like = data[0]["main"]["feels_like"]
    temp_min = data[0]["main"]["temp_min"]
    temp_max = data[0]["main"]["temp_max"]
    humidity = data[0]["main"]["humidity"]
    sunrise = data[0]["main"]["sunrise"]
    sunset = data[0]["main"]["sunset"]
    info_string = f"Here is the weather results for {location} are as follows:\nDescription: {description}\nTemperature: {temp}\nFeels like: {feels_like}\nMin: {temp_min}\nMax: {temp_max}\nHumidity: {humidity}\nSunrise: {sunrise}\nSunset: {sunset}"
    print(info_string)
    return info_string

def check_mentions(api, keywords, since_id,city_data):
    logger.info("Retrieving mentions")
    new_since_id = since_id

    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        print("Mentioned")
        print("new since id:",new_since_id)
        print("tweet.id",tweet.id)
        new_since_id = max(tweet.id, new_since_id)
        print("new since id:",new_since_id)

        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
            logger.info(f"Answering to {tweet.user.name}")
            status = tweet.text.lower().split()
            print("\n\nStatus: ",status)
            try:
                location_index = status.index(keywords[0]) + 1
                print("\n\nLocation index",location_index)
                # if status[location_index] not in city_data:
                #     raise Exception
                api_answer = send_api_request(status[location_index])
                tweet_string = parse_api_response(api_answer)
            except Exception as e:
                print(e)
                logger.error("Invalid tweet recived")
                tweet_string = f"Unfortunatly there is no available forcast for: {status[location_index]}\nThe current forcast for the Moon is: Clear skies with a 0% chance of precipitation"
            #tweet_string += f" @{tweet.user}"
            print(len(tweet_string), tweet_string)
            #tweet_string = f" @{tweet.user} TEST"

            api.update_status(
                status=tweet_string,
                in_reply_to_status_id=tweet.id,
                auto_populate_reply_metadata=True
            )
    print("checked")
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
    print(consumer_key,consumer_secret,access_token,access_token_secret)
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