from flask import Flask, request, jsonify, render_template
from geopy.geocoders import Nominatim

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

@app.route('/update_location', methods=['POST'])
def update_location():
    try:
        data = request.get_json()
        print("Received Data:", data)  # Debugging

        if not data or 'bus_no' not in data or 'latitude' not in data or 'longitude' not in data:
            return jsonify({"error": "Missing required fields"}), 400

        bus_no = data['bus_no']
        if bus_no not in bus_locations:
            bus_locations[bus_no] = []

        bus_locations[bus_no].append({
            'latitude': data['latitude'],
            'longitude': data['longitude'],
            'area': data.get('area', 'Unknown')
        })

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Invalid request"}), 400


@app.route('/get_locations/<bus_no>')
def get_locations(bus_no):
    locations = bus_locations.get(bus_no, [])
    print(f"Bus: {bus_no}, Data in Server: {locations}")  # Debugging
    return jsonify(locations)  # Ensure this returns a proper list


if __name__ == '__main__':
    app.run(debug=True)
