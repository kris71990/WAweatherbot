# weatherbot.py
# A twitter bot that interacts with the weather underground and twitter apis to tweet regularly about weather conditions from various locations around
# Washington State.

import os, tweepy, random, time

from dotenv import load_dotenv
from json import loads
from urllib.request import urlopen
from locations import locations

load_dotenv()


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


cities = []
# loop generates random numbers and determines locations to tweet about based on the random numbers
for x in range(0, int(round(len(locations)/10))):
    rand = random.randint(0, len(locations))
    
    if rand == 0:
        city = locations['0']
    elif rand == 1:
        city = locations['1']
    elif rand == 2:
        city = locations['2']
    elif rand == 3:
        city = locations['3']
    elif rand == 4:
        city = locations['4']
    elif rand == 5:
        city = locations['5']
    elif rand == 6:
        city = locations['6']
    elif rand == 7:
        city = locations['7']
    elif rand == 8:
        city = locations['8']
    elif rand == 9:
        city = locations['9']
    elif rand == 10:
        city = locations['10']
    elif rand == 11:
        city = locations['11']
    elif rand == 12:
        city = locations['12']
    elif rand == 13:
        city = locations['13']
    elif rand == 14:
        city = locations['14']
    elif rand == 15:
        city = locations['15']
    elif rand == 16:
        city = locations['16']
    elif rand == 17:
        city = locations['17']
    elif rand == 18:
        city = locations['18']
    elif rand == 19:
        city = locations['19']
    elif rand == 20:
        city = locations['20']
    elif rand == 21:
        city = locations['21']
    elif rand == 22:
        city = locations['22']
    elif rand == 23:
        city = locations['23']
    elif rand == 24:
        city = locations['24']
    elif rand == 25:
        city = locations['25']
    elif rand == 26:
        city = locations['26']
    elif rand == 27:
        city = locations['27']
    elif rand == 28:
        city = locations['28']
    elif rand == 29:
        city = locations['29']
    elif rand == 30:
        city = locations['30']
    elif rand == 31:
        city = locations['31']
    elif rand == 32:
        city = locations['32']
    elif rand == 33:
        city = locations['33']
    elif rand == 34:
        city = locations['34']
    elif rand == 35:
        city = locations['35']
    elif rand == 36:
        city = locations['36']
    elif rand == 37:
        city = locations['37']
    elif rand == 38:
        city = locations['38']
    elif rand == 39:
        city = locations['39']
    elif rand == 40:
        city = locations['40']
    elif rand == 41:
        city = locations['41']
    elif rand == 42:
        city = locations['42']
    elif rand == 43:
        city = locations['43']
    elif rand == 44:
        city = locations['44']
    elif rand == 45:
        city = locations['45']
    elif rand == 46:
        city = locations['46']
    elif rand == 47:
        city = locations['47']
    elif rand == 48:
        city = locations['48']
    elif rand == 49:
        city = locations['49']
    else:
        city = locations['50']

    #prevents duplicate status updates for the same location
    if city not in cities:
        cities.append(city)

    x+=1


# connect with twitter api, loop through tweet locations in list generated above and create a status for each
# post the status, wait a given time until posting the next tweet
if __name__ == '__main__':
    auth = tweepy.OAuthHandler(classifiedInfo.consumer_key, classifiedInfo.consumer_secret)
    auth.set_access_token(classifiedInfo.access_token, classifiedInfo.access_secret)
    api = tweepy.API(auth)
    
    for city in cities:
        time.sleep(20)
        current_data = get_current_data(city)
        forecast_data = get_forecast(city)
        
        if city.startswith('pws'):
            status = (current_data['current_observation']['observation_location']['city'] + ': Currently ' + current_data['current_observation']['weather'] + ' with a temperature of ' +
                      current_data['current_observation']['temperature_string'] + ', and a relative humidity of ' +
                      current_data['current_observation']['relative_humidity'] +
                      '. Today\'s forecast: ' + forecast_data['forecast']['txt_forecast']['forecastday'][0]['fcttext'] + ' ' + current_data['current_observation']['forecast_url'])
        else:
            status = (current_data['current_observation']['display_location']['city'] + ': Currently ' + current_data['current_observation']['weather'] + ' with a temperature of ' +
                  current_data['current_observation']['temperature_string'] + ', and a relative humidity of ' +
                  current_data['current_observation']['relative_humidity'] +
                  '. Today\'s forecast: ' + forecast_data['forecast']['txt_forecast']['forecastday'][0]['fcttext'] + ' ' + current_data['current_observation']['forecast_url'])
    
        try:
            api.update_status(status)
        except tweepy.TweepError:
            pass
        
        print(status)

