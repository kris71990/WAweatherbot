# waweatherbot.py
# A twitter bot that interacts with the weather underground and twitter apis to tweet regularly about weather conditions in Seattle.
# soon to add weather reports from areas across WA state.


import tweepy
from json import loads
from urllib.request import urlopen
import classifiedInfo

current_url = 'http://api.wunderground.com/api/' + classifiedInfo.weather_key + '/conditions/q/WA/Seattle.json'
current_req = urlopen(current_url)
current_data = loads(current_req.read().decode('utf-8'))

forecast_url = 'http://api.wunderground.com/api/' + classifiedInfo.weather_key + '/forecast/q/WA/Seattle.json'
forecast_req = urlopen(forecast_url)
forecast_data = loads(forecast_req.read().decode('utf-8'))

status = (current_data['current_observation']['display_location']['city'] + ': Currently ' + current_data['current_observation']['weather'] + ' with a temperature of ' +
    current_data['current_observation']['temperature_string'] + ', and a relative humidity of ' +
    current_data['current_observation']['relative_humidity'] +
    '. Today\'s forecast: ' + forecast_data['forecast']['txt_forecast']['forecastday'][0]['fcttext'] + ' ' + current_data['current_observation']['forecast_url'])

if __name__ == '__main__':
    auth = tweepy.OAuthHandler(classifiedInfo.consumer_key, classifiedInfo.consumer_secret)
    auth.set_access_token(classifiedInfo.access_token, classifiedInfo.access_secret)
    api = tweepy.API(auth)

    try:
        api.update_status(status)
    except tweepy.TweepError:
        pass


print(status)
