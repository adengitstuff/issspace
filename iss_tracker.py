import requests
import folium
from datetime import datetime

# -- get people with the open-notify api
# Future upgrades can include their photos!
def get_people_in_space():
    url = "http://api.open-notify.org/astros.json"
    response = requests.get(url)
    data = response.json()
    
    crews = {}
    for person in data['people']:
        craft = person['craft']
        if craft not in crews:
            crews[craft] = []
        crews[craft].append(person['name'])
    return crews, data['number']

# -- get iss position as floats -- 
# 
#  To-do: Add movement of the ISS over time and a better visualizer.
#  
# #
def get_iss_position():
    url = "http://api.open-notify.org/iss-now.json"
    response = requests.get(url)
    data = response.json()
    
    latitude = float(data['iss_position']['latitude'])
    longitude = float(data['iss_position']['longitude'])
    timestamp = datetime.fromtimestamp(data['timestamp'])
    
    return latitude, longitude, timestamp

def create_dashboard():
    crews, total_people = get_people_in_space()
    lat, lon, timestamp = get_iss_position()
    
    # Create fullscreen map
    m = folium.Map(location=[lat, lon], zoom_start=4)
    
    # Add ISS marker - custom markers possible w Folium too.
    #
    folium.Marker(
        [lat, lon],
        popup=f'ISS at {timestamp}',
       icon=folium.Icon(color='red', icon='info-sign')
     ).add_to(m)
    
    
     # Tried custom icons:
    #iss_icon_html = """
    #    <div style="font-size: 45px;">🛰️</div>
    #"""

    # Alternative icon options:
    # 🛰️ (satellite)
    # 🚀 (rocket)

    #iss_icon = folium.DivIcon(
    #    html=iss_icon_html,
    #    icon_size=(45, 45),
    #    icon_anchor=(15, 15),
   # )

    # Add ISS marker with custom icon
    # folium.Marker(
    #    [lat, lon],
    #    popup=f'ISS at {timestamp}',
    #    icon=iss_icon
    #).add_to(m)

    
    # Get map HTML and create dashboard
    map_html = m._repr_html_()
    
    # Create crew info HTML
    crew_html = ""
    for craft, crew in crews.items():
        crew_html += f"<div class='craft-section'><h3>{craft}</h3><ul>"
        for astronaut in crew:
            crew_html += f"<li>{astronaut}</li>"
        crew_html += "</ul></div>"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>ISS Tracking Dashboard</title>
        <style>
            body, html {{
                margin: 0;
                padding: 0;
                height: 100%;
                font-family: Arial, sans-serif;
            }}
            #map-container {{
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                z-index: 1;
            }}
            #info-panel {{
                position: absolute;
                top: 20px;
                right: 20px;
                background: rgba(255, 255, 255, 0.9);
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                z-index: 2;
                max-width: 300px;
                backdrop-filter: blur(5px);
            }}
            h2, h3 {{
                margin: 0 0 10px 0;
                color: #2c3e50;
            }}
            .craft-section {{
                margin-top: 15px;
                padding-top: 15px;
                border-top: 1px solid #eee;
            }}
            .craft-section:first-child {{
                border-top: none;
                margin-top: 0;
                padding-top: 0;
            }}
            ul {{
                margin: 5px 0;
                padding-left: 20px;
            }}
            li {{
                margin: 3px 0;
            }}
            .timestamp {{
                font-size: 0.8em;
                color: #666;
                margin-top: 15px;
            }}
        </style>
    </head>
    <body>
        <div id="map-container">
            {map_html}
        </div>
        <div id="info-panel">
            <h2>Current Space Population: {total_people}</h2>
            {crew_html}
            <div class="timestamp">Last updated: {timestamp}</div>
        </div>
    </body>
    </html>
    """
    
    with open('space_dashboard.html', 'w') as f:
        f.write(html)
    
    print(f"Dashboard created! Open 'space_dashboard.html' in your browser")

if __name__ == "__main__":
    create_dashboard()