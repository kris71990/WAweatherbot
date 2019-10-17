# weatherbot.py
# A twitter bot that interacts with the weather underground and twitter apis to tweet regularly about weather conditions from various locations around
# Washington State.

import os, twitter, random, time, requests
from dotenv import load_dotenv
from json import loads
from locations import locations

load_dotenv()

# fetch json data from the weather.gov api
def get_forecast(cityCoordinates):
  url = 'https://api.weather.gov/points/' + cityCoordinates
  res = requests.get(url)
  res.raise_for_status()
  json = res.json()
  props = json['properties']['forecast']
  location = json['properties']['relativeLocation']['properties']['city']
  resForecast = requests.get(props)
  resForecast.raise_for_status()
  return { 'city': location, 'data': resForecast.json() }


# generates random numbers and determines locations to tweet about based on the random numbers
def getCities():
  locales = list(locations.keys())
  cities = []
  for i in range(0, 5):
    rand = random.randint(0, len(locales) - 1)
    city = locales[rand]
    
    #prevents duplicate status updates for the same location
    if city not in cities:
      cities.append(city)
  return cities


# connect with twitter api, loop through tweet locations in list generated above and create a status for each
# post tweet, wait a given time until posting the next tweet
if __name__ == '__main__':
  twitterConnection = twitter.Api(os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET'), os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_SECRET'))
  
  cities = getCities()
  print(cities)

  for city in cities:
    cityCoordinates = locations[city]
    time.sleep(2)
    forecastRes = get_forecast(cityCoordinates)
    forecast = forecastRes['data']
    locale = forecastRes['city']

    currentConditions = forecast['properties']['periods'][0]
    forecast = forecast['properties']['periods'][1]

    statusFull = '%s: %sF - %s' % (city, currentConditions['temperature'], currentConditions['detailedForecast'])
    statusShort = '%s: %sF - %s %s: %s.' % (city, currentConditions['temperature'], currentConditions['shortForecast'], forecast['name'], forecast['shortForecast'])

    try:
      if len(statusFull) <= 280:
        print(statusFull)
        twitterConnection.PostUpdate(statusFull)
      else:
        print(statusShort)
        twitterConnection.PostUpdate(statusShort)
    except twitter.error.TwitterError:
      print('Error - Tweet unable to post')

