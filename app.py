from flask import Flask, request, jsonify, render_template
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

app = Flask(__name__)

# Initialize geolocator
geolocator = Nominatim(user_agent="bus_tracker")

# Store bus locations
bus_locations = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track/<bus_no>')
def track(bus_no):
    return render_template('track.html')

def get_area_name(latitude, longitude):
    """Reverse geocode to get the area name from latitude and longitude."""
    try:
        location = geolocator.reverse((latitude, longitude), exactly_one=True, language="en")
        return location.address if location else "Unknown"
    except GeocoderTimedOut:
        return "Geocoder Timed Out"
    except Exception as e:
        print(f"Geocoding Error: {str(e)}")
        return "Unknown"

@app.route('/update_location', methods=['POST'])
def update_location():
    try:
        data = request.get_json()
        print("Received Data:", data)  # Debugging

        if not data or 'bus_no' not in data or 'latitude' not in data or 'longitude' not in data:
            return jsonify({"error": "Missing required fields"}), 400

        bus_no = data['bus_no']
        latitude = data['latitude']
        longitude = data['longitude']

        # Get area name from coordinates
        area_name = get_area_name(latitude, longitude)

        if bus_no not in bus_locations:
            bus_locations[bus_no] = []

        bus_locations[bus_no].append({
            'latitude': latitude,
            'longitude': longitude,
            'area': area_name
        })

        return jsonify({"status": "success", "area": area_name}), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Invalid request"}), 400

@app.route('/get_locations/<bus_no>')
def get_locations(bus_no):
    locations = bus_locations.get(bus_no, [])
    print(f"Bus: {bus_no}, Data in Server: {locations}")  # Debugging
    return jsonify(locations)

if __name__ == '__main__':
    app.run(debug=True)
