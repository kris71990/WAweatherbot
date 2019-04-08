# weatherbot.py
# A twitter bot that interacts with the weather underground and twitter apis to tweet regularly about weather conditions from various locations around
# Washington State.

import os, tweepy, random, time, requests
from dotenv import load_dotenv
from json import loads
from locations import locations

load_dotenv()

# these methods fetch json data from the wunderground api
def get_current_data(location):
  url = 'https://api.weather.gov/points/' + location
  res = requests.get(url)
  res.raise_for_status()
  return res.json()

def get_forecast(location):
  url = 'http://api.wunderground.com/api/' + os.getenv('WU_API_KEY') + '/forecast/q/' + location + '.json'
  res = requests.get(url)
  res.raise_for_status()
  return res.json()


# generates random numbers and determines locations to tweet about based on the random numbers
def getCities():
  cities = []
  for x in range(0, int(round(len(locations) / 10))):
    rand = random.randint(0, len(locations) - 1)
    city = locations[rand]
    
    #prevents duplicate status updates for the same location
    if city not in cities:
      cities.append(city)
  return cities


# connect with twitter api, loop through tweet locations in list generated above and create a status for each
# post the status, wait a given time until posting the next tweet
if __name__ == '__main__':
  auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
  auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_SECRET'))
  api = tweepy.API(auth)
  
  # cities = getCities()
  cities = locations

  for city in cities:
    time.sleep(10)
    current_data = get_current_data(city)
    # forecast_data = get_forecast(city)

    print(current_data)
    # print(forecast_data)

    # current_conditions = current_data['current_observation']['weather']
    # current_temp = current_data['current_observation']['temperature_string']
    # current_humidity = current_data['current_observation']['relative_humidity']
    # forecast = forecast_data['forecast']['txt_forecast']['forecastday'][0]['fcttext']
    # forecast_url = current_data['current_observation']['forecast_url']
  
    # if city.startswith('pws'):
    #   location = current_data['current_observation']['observation_location']['city']
    # else:
    #   location = current_data['current_observation']['display_location']['city']


    # status = '%s: Currently %s with a temperature of %s, and a relative humidity of %s. Today\'s forecast: %s %s' % (location, current_conditions, current_temp, current_humidity, forecast, forecast_url)

    # try:
    #   api.update_status(status)
    # except tweepy.TweepError:
    #   pass
    
    # print(status)

