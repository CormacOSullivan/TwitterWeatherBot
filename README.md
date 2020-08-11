# TwitterWeatherBot

This project is a Python based Twitter bot that will reply to formatted tweets that are requesting the current weather forecast for world locations. 
The project uses Tweepy & OpenWeatherMap APIs.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

This project was implemented using Python 3.7.6 and the module versions listed in the requirements.txt file
A free Twitter Developer account is needed for access to the twitter api that is used in this project. Sign up can be done [here](https://developer.twitter.com/en)
Once an account is setup, create a new project and app.

OpenWeatherMap API also requires a free sign up to access their api. A guide for this process can be found [here](https://openweathermap.org/guide)
Once an account is setup, generate a new API key to be used by the project

After creating the two required accounts above, you should now have a API Key & Secret pair and an Access Token & Secret pair for the Twitter API as well as an OpenWeatherMap API key
 

### Installing

1. First, clone the most recent master branch commit from the [TwitterWeatherBot](https://github.com/CormacOSullivan/TwitterWeatherBot) GitHub repo 
2. To install the required modules into the environment use the following command: pip3 install -r requirements.txt
3. TwitterWeatherBot uses system environment variables for accessing the API keys and secrets so the next step is to add these variables to the environment. This can be done via the control panel in Windows or in Linux via the command: $ export NAME=VALUE
   The environment variables should be named as follows: ACCESS_TOKEN, ACCESS_TOKEN_SECRET, CONSUMER_KEY & CONSUMER_SECRET
4. To start the system, run the Main.py file 


The bot requires correctly formatted tweets to parse the location (and units) from the tweet sent by a user. The user should provide a city, town, village etc. parameter and can also provide an optional unit parameter . 
The users tweet should be formatted in the following way:

@TweetWeatherBot location: Location Name! units: units type

The bot uses two keywords and a delimiter character (!) to parse the information from the tweet. The bot takes the information between the "location:" keyword and the ! character as the location name, and the word after the "units:" keyword as the unit type. Currently the bot can provide imperial or metric measurements with metric being the default if no unit is provided


#### Example 1
User Tweet:
@TweetWeatherBot location: New York City! units: imperial

Bot Reply:
Here is the weather results for New York:

Description: Broken Clouds
Temperature: 86.74°F
Feels like: 87.28°F
Min: 84.2°F
Max: 89.6°F
Humidity: 66%
Sunrise: 06:02
Sunset: 19:59

#### Example 2
User Tweet:
@TweetWeatherBot location: Cork!

Bot Reply:
Here is the weather results for Cork:

Description: Few Clouds
Temperature: 20°C
Feels like: 19.79°C
Min: 20°C
Max: 20°C
Humidity: 82%
Sunrise: 06:12
Sunset: 21:05


## Deployment

This Section is a work in progress

## Built With

* [OpenWeatherMap](https://openweathermap.org/api) - The weather api used
* [Tweepy](http://docs.tweepy.org/en/latest/api.html) - Twitter API access


## Authors

* **Cormac O'Sullivan** - *Initial work* - [CormacOSullivan](https://github.com/CormacOSullivan)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

Thank you to Miguel Garcia whose [tutorial](https://realpython.com/twitter-bot-python-tweepy/) I followed when creating this project