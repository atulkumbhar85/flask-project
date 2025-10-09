from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend-backend communication


# MongoDB connection
MONGODB_URI = os.getenv('MONGODB_URI')
client = MongoClient(MONGODB_URI)
db = client.test_db  
todolist_collection = db.todolist  # New collection for to-do items


@app.route('/submittodoitem', methods=['POST'])
def submittodoitem():
    """Handle to-do item creation and save to MongoDB Atlas"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No data provided'
            }), 400

        item_name = data.get('item_name')
        item_description = data.get('item_description')

        # Validate input
        if not item_name or not item_description:
            return jsonify({
                'success': False,
                'message': 'Item name and description are required'
            }), 400

        new_item = {
            'item_name': item_name,
            'item_description': item_description,
            'created_at': datetime.utcnow()
        }

        result = todolist_collection.insert_one(new_item)

        if result.inserted_id:
            return jsonify({
                'success': True,
                'message': 'To-Do item added successfully',
                'item_id': str(result.inserted_id)
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to add to-do item'
            }), 500
    except Exception as e:
        print(f"Error in submittodoitem: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Internal server error'
        }), 500

if __name__ == '__main__':
    print("Starting Flask backend server...")
    app.run(debug=True, host='0.0.0.0', port=5001)