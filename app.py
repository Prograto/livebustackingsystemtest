from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Store bus locations in a dictionary {bus_no: [{'latitude': xx, 'longitude': yy, 'area': 'xyz'}]}
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

        if not data:
            return jsonify({"error": "No data received"}), 400
        if 'bus_no' not in data or 'latitude' not in data or 'longitude' not in data:
            return jsonify({"error": "Missing required fields"}), 400

        if not isinstance(data.get('latitude'), (int, float)) or not isinstance(data.get('longitude'), (int, float)):
            return jsonify({"error": "Invalid latitude or longitude"}), 400

        bus_no = data['bus_no']
        if bus_no not in bus_locations:
            bus_locations[bus_no] = []
        bus_locations[bus_no].append(data)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": "Invalid request"}), 400

@app.route('/get_locations/<bus_no>')
def get_locations(bus_no):
    data = bus_locations.get(bus_no, [])
    print(f"Bus: {bus_no}, Data in Server: {data}")  # Debugging
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
