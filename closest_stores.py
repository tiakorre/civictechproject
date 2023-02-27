import requests
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# Set up the Google Maps API request
api_key = 'your API here'
url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

# Get the user's location
geolocator = Nominatim(user_agent='my_application')
address = input('Enter your address or ZIP code: ')
location = geolocator.geocode(address)
user_lat, user_lon = location.latitude, location.longitude

# Make the Places API request
stores = []
params = {
    'key': api_key,
    'location': f'{user_lat},{user_lon}',
    'radius': 8046.72,  # 5 miles in meters
    'type': 'grocery_or_supermarket'
}
response = requests.get(url, params=params)
results = response.json()['results']
for result in results:
    lat, lon = result['geometry']['location']['lat'], result['geometry']['location']['lng']
    store_location = (lat, lon)
    distance = geodesic((user_lat, user_lon), store_location).miles
    if distance <= 5:
        place_id = result['place_id']
        details_url = 'https://maps.googleapis.com/maps/api/place/details/json'
        details_params = {
            'key': api_key,
            'place_id': place_id,
            'fields': 'name,website'
        }
        details_response = requests.get(details_url, params=details_params)
        details_result = details_response.json()['result']
        if 'website' in details_result:
            store_name = details_result['name']
            store_url = details_result['website']
            stores.append((store_name, distance, store_url))

# Sort the list of stores by distance
sorted_stores = sorted(stores, key=lambda x: x[1])

# Print the name, distance, and URL for each store within 5 miles, sorted by distance
for store in sorted_stores:
    print(f'{store[0]} ({store[1]:.2f} miles away): {store[2]}')
