#!/usr/bin/env python

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
        """
        Sends a request including the user requested location and units to the openweathermapapi  and then
        decodes the response
        :param location: String representing a place name for requesting the current weather
        :param units: String representing the units required by the user
        :return: data -> Dictionary containing the weather information received from the api request sent
                 -1 -> If an error occurred
        """
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
        """
        Parses the required data from the openweatherapi response's dictionary and returns a formatted  tweet string
        :param data: dictionary from openweatherapi call
        :param units: String that holds the type of units to be used in tweet string
        :return: info_string -> The string containing the parsed weather results for replying to the request
                 -1 -> if an error has occurred during the parse
        """
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
        """
        Reads the information found in the city_list.json file for checking the users requested weather location
        and returns the data after decoding
        :return: data -> A dictionary contain all the information for locations compatible with openweatherapi
                 -1 -> If an error occurred
        """
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
