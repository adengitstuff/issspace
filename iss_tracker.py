import requests
import folium
from datetime import datetime
import time
from pprint import pprint

def get_people_in_space():
    url = "http://api.open-notify.org/astros.json"
    response = requests.get(url)
    data = response.json()
    
    print(f"\nCurrent People in Space: {data['number']}")
    print("\nCrew Details:")
    # Group people by craft
    crews = {}
    for person in data['people']:
        craft = person['craft']
        if craft not in crews:
            crews[craft] = []
        crews[craft].append(person['name'])
    
    # Print organized by spacecraft
    for craft, crew in crews.items():
        print(f"\n{craft}:")
        for astronaut in crew:
            print(f"  • {astronaut}")
    return data

def get_iss_position():
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url)
    data = response.json()
    
    latitude = float(data['iss_position']['latitude'])
    longitude = float(data['iss_position']['longitude'])
    timestamp = datetime.fromtimestamp(data['timestamp'])
    
    return latitude, longitude, timestamp

def create_map():
    # Get current ISS position
    lat, lon, timestamp = get_iss_position()
    
    # Create map centered on ISS
    m = folium.Map(location=[lat, lon], zoom_start=4)
    
    # Add ISS marker
    folium.Marker(
        [lat, lon],
        popup=f'ISS at {timestamp}',
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    
    # Save map
    m.save('iss_position.html')
    print(f"\nISS Position at {timestamp}:")
    print(f"Latitude: {lat}")
    print(f"Longitude: {lon}")
    print("\nMap saved as 'iss_position.html'")

if __name__ == "__main__":
    print("Space Tracking System")
    print("===================")
    get_people_in_space()
    create_map()