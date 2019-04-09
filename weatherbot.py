# weatherbot.py
# A twitter bot that interacts with the weather underground and twitter apis to tweet regularly about weather conditions from various locations around
# Washington State.

import os, tweepy, random, time, requests
from dotenv import load_dotenv
from json import loads
from locations import locations

load_dotenv()

# fetch json data from the weather.gov api
def get_forecast(location):
  url = 'https://api.weather.gov/points/' + location
  res = requests.get(url)
  res.raise_for_status()
  json = res.json()
  props = json['properties']['forecast']
  loc = json['properties']['relativeLocation']['properties']['city']
  resFore = requests.get(props)
  resFore.raise_for_status()
  return { 'city': loc, 'data': resFore.json() }


# generates random numbers and determines locations to tweet about based on the random numbers
def getCities():
  locales = list(locations.keys())
  cities = []
  for x in range(0, 5):
    rand = random.randint(0, len(locales) - 1)
    city = locales[rand]
    
    #prevents duplicate status updates for the same location
    if city not in cities:
      cities.append(city)
  return cities


# connect with twitter api, loop through tweet locations in list generated above and create a status for each
# post tweet, wait a given time until posting the next tweet
if __name__ == '__main__':
  auth = tweepy.OAuthHandler(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'))
  auth.set_access_token(os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_SECRET'))
  api = tweepy.API(auth)
  
  cities = getCities()
  print(cities)

  for city in cities:
    coords = locations[city]
    time.sleep(2)
    info = get_forecast(coords)
    forecast = info['data']
    locale = info['city']

    current = forecast['properties']['periods'][0]
    forecast = forecast['properties']['periods'][1]

    statusFull = '%s: %sF - %s' % (city, current['temperature'], current['detailedForecast'])
    statusShort = '%s: %sF - %s %s: %s.' % (city, current['temperature'], current['shortForecast'], forecast['name'], forecast['shortForecast'])

    try:
      if len(statusFull) <= 280:
        print(statusFull)
        api.update_status(statusFull)
      else:
        print(statusShort)
        api.update_status(statusShort)
    except tweepy.TweepError:
      pass
