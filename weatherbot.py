# weatherbot.py
# A twitter bot that interacts with the weather underground and twitter apis to tweet regularly about weather conditions from various locations around
# Washington State.

import tweepy
from json import loads
from urllib.request import urlopen
import time
import classifiedInfo
from locations import locations

# these methods fetch json data from the wunderground api
def get_current_data(location):
    current_url = 'http://api.wunderground.com/api/' + classifiedInfo.weather_key + '/conditions/q/' + location + '.json'
    current_req = urlopen(current_url)
    current_data = loads(current_req.read().decode('utf-8'))
    return current_data

def get_forecast(location):
    forecast_url = 'http://api.wunderground.com/api/' + classifiedInfo.weather_key + '/forecast/q/' + location + '.json'
    forecast_req = urlopen(forecast_url)
    forecast_data = loads(forecast_req.read().decode('utf-8'))
    return forecast_data


# get current time and use it to determine which location to tweet about
time = time.localtime()
if time.tm_min < 10:
    minute = time.tm_min
elif time.tm_min > 10:
    minute_string = str(time.tm_min)[1:]
    minute = int(minute_string)

# chooses location from locations.py depending on final digit of the minute of the current time, found above
if minute == 0:
    current_data = get_current_data(locations['0'])
    forecast_data = get_forecast(locations['0'])
elif minute == 1:
    current_data = get_current_data(locations['1'])
    forecast_data = get_forecast(locations['1'])
elif minute == 2:
    current_data = get_current_data(locations['2'])
    forecast_data = get_forecast(locations['2'])
elif minute == 3:
    current_data = get_current_data(locations['3'])
    forecast_data = get_forecast(locations['3'])
elif minute == 4:
    current_data = get_current_data(locations['4'])
    forecast_data = get_forecast(locations['4'])
elif minute == 5:
    current_data = get_current_data(locations['5'])
    forecast_data = get_forecast(locations['5'])
elif minute == 6:
    current_data = get_current_data(locations['6'])
    forecast_data = get_forecast(locations['6'])
elif minute == 7:
    current_data = get_current_data(locations['7'])
    forecast_data = get_forecast(locations['7'])
elif minute == 8:
    current_data = get_current_data(locations['8'])
    forecast_data = get_forecast(locations['8'])
else:
    current_data = get_current_data(locations['9'])
    forecast_data = get_forecast(locations['9'])

# generates a status from the appropriate location using api data
status = (current_data['current_observation']['display_location']['city'] + ': Currently ' + current_data['current_observation']['weather'] + ' with a temperature of ' +
    current_data['current_observation']['temperature_string'] + ', and a relative humidity of ' +
    current_data['current_observation']['relative_humidity'] +
    '. Today\'s forecast: ' + forecast_data['forecast']['txt_forecast']['forecastday'][0]['fcttext'] + ' ' + current_data['current_observation']['forecast_url'])

print(status)

# connect with twitter api and post the status
if __name__ == '__main__':
    auth = tweepy.OAuthHandler(classifiedInfo.consumer_key, classifiedInfo.consumer_secret)
    auth.set_access_token(classifiedInfo.access_token, classifiedInfo.access_secret)
    api = tweepy.API(auth)

    try:
        api.update_status(status)
    except tweepy.TweepError:
        pass
