from flask import Flask, jsonify
from flask_cors import CORS
from flask import request, session

app = Flask(__name__)
CORS(app)

app.secret_key = 'supersecretkey'

@app.route('/gps', methods=['POST'])
def gps():
    data = request.get_json()
    session['gps'] = data
    return jsonify(message="GPS coordinates stored successfully")

@app.route('/alert', methods=['GET'])
def alert():
    return jsonify(message="successful! the authorities have been contacted")

if __name__ == '__main__':
    app.run(debug=True)