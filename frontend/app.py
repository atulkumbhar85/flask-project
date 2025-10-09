
from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'simple-signup-key'  # Needed for flash messages

# Backend API URL
BACKEND_API_URL = 'http://localhost:5001'
@app.route('/submittodoitem', methods=['POST'])
def submittodoitem():
    """Handle to-do item creation form submission"""
    try:
        item_name = request.form.get('item_name')
        item_description = request.form.get('item_description')

        if not item_name or not item_description:
            flash('Item name and description are required', 'error')
            return redirect(url_for('index'))

        print(f"New To-Do Item: {item_name} - {item_description}")

        response = requests.post(f"{BACKEND_API_URL}/api/todoitems", json={
            'name': item_name,
            'description': item_description
        })

        if response.status_code == 201:
            # Redirect to success page
            return redirect(url_for('success'))
        else:
            flash('Failed to add to-do item', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        flash('An error occurred while adding the to-do item', 'error')
        print(f"To-Do item error: {e}")
        return redirect(url_for('index'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/success')
def success():
    return render_template('success.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)