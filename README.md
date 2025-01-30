# ISS Position Tracker

Simple project that builds a real-time visualization system for tracking the International Space Station's orbital position. Uses Python and Folium to spit out an interactive map of the ISS's current position. 

Future upgrades could include more satellites and even orbit predictions, and even displaying the people in space and aircraft names (open-notify API provides this)

Using venv
## Features
- Real-time ISS position tracking
- Interactive map visualization
- Geospatial data integration
- Space object monitoring

## Setup
1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment: `source venv/bin/activate`
4. Install requirements: `pip install -r requirements.txt`
5. Run tracker: `python iss_tracker.py`

## Technologies
- Python
- Folium for mapping
- Open Notify API for ISS data
