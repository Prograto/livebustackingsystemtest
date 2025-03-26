from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Store bus locations in a dictionary {bus_no: [{'lat': xx, 'lng': yy, 'area': 'xyz'}]}
bus_locations = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/track/<bus_no>')
def track(bus_no):
    return render_template('track.html')

@app.route('/update_location', methods=['POST'])
def update_location():
    data = request.json
    bus_no = data.get('bus_no')
    lat = data.get('lat')
    lng = data.get('lng')
    area = data.get('area', 'Unknown')

    if bus_no:
        if bus_no not in bus_locations:
            bus_locations[bus_no] = []
        bus_locations[bus_no].append({'lat': lat, 'lng': lng, 'area': area})

        # Keep only the last 20 locations for each bus
        if len(bus_locations[bus_no]) > 20:
            bus_locations[bus_no].pop(0)

        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "Invalid data"}), 400

@app.route('/get_locations/<bus_no>')
def get_locations(bus_no):
    data = bus_locations.get(bus_no, [])
    print(f"Requested Bus: {bus_no}, Data: {data}")  # Debugging
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
