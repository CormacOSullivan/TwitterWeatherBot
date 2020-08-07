#!/usr/bin/env python
# tweepy-bots/bots/autoreply.py

import json
import requests
from datetime import datetime


class WeatherAPI:
    temp_units = {"imperial": "°F", "metric": "°C"}

    def __init__(self, api_key, json_path, logger=None):
        self.key = api_key
        self.json_path = json_path
        self.logger = logger

    def send_api_request(self, location, units="metric"):
        try:
            call = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.key}&units={units}"
            response = requests.get(call)
            data = json.loads(response.text)
        except requests.exceptions.RequestException as e:
            self.logger.error("An Unexpected requests error has occurred: ", e)
            return -1
        except json.JSONDecodeError as f:
            self.logger.error("An Unexpected JSON error has occurred: ", f)
            return -1
        return data

    def parse_api_response(self, data, units="metric"):
        try:
            location = data["name"]
            description = data["weather"][0]["description"].title()
            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            temp_min = data["main"]["temp_min"]
            temp_max = data["main"]["temp_max"]
            humidity = data["main"]["humidity"]
            timezone = data["timezone"]
            sunrise = datetime.utcfromtimestamp(data["sys"]["sunrise"] + timezone).strftime('%H:%M')
            sunset = datetime.utcfromtimestamp(data["sys"]["sunset"] + timezone).strftime('%H:%M')

            info_string = f"Here is the weather results for {location}:\n\nDescription: {description}\nTemperature: {temp}{WeatherAPI.temp_units[units]}\nFeels like: {feels_like}{WeatherAPI.temp_units[units]}\nMin: {temp_min}{WeatherAPI.temp_units[units]}\nMax: {temp_max}{WeatherAPI.temp_units[units]}\nHumidity: {humidity}%\nSunrise: {sunrise}\nSunset: {sunset}"
        except LookupError as e:
            self.logger.error(e)
            return -1
        return info_string

    def read_json(self):
        try:
            with open(self.json_path, encoding='utf-8') as f:
                data = json.load(f)
        except (IOError, ValueError, EOFError) as e:
            self.logger.error(e)
            return -1
        except Exception as f:
            self.logger.error("An Unexpected error has occurred: ", f)
            return -1
        return data
