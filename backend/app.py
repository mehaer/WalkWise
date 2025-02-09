from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory storage for demonstration purposes
locations = []

@app.route('/alert', methods=['POST'])
def alert():
    data = request.get_json()
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    
    # Save the location data
    locations.append({'latitude': latitude, 'longitude': longitude})
    
    return jsonify(message=f"Successful! The authorities have been contacted. Location: ({latitude}, {longitude})")

@app.route('/locations', methods=['GET'])
def get_locations():
    return jsonify(locations)

if __name__ == '__main__':
    app.run(debug=True)