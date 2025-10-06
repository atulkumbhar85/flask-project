from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

# Path to your backend file
DATA_FILE = 'data.json'

@app.route('/api', methods=['GET'])
def api():
    if not os.path.exists(DATA_FILE):
        # If the file doesn't exist, return an empty list
        return jsonify([])

    # Read data from the file and return as JSON
    with open(DATA_FILE, 'r') as file:
        data = json.load(file)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
