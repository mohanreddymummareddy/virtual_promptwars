from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Dummy data for the prototype
venue_status = {
    "zones": [
        {"id": "A", "name": "North Gate", "congestion": 85, "wait_time_mins": 15, "status": "Red"},
        {"id": "B", "name": "East Concessions", "congestion": 45, "wait_time_mins": 5, "status": "Yellow"},
        {"id": "C", "name": "South Restrooms", "congestion": 20, "wait_time_mins": 2, "status": "Green"},
        {"id": "D", "name": "West Merch", "congestion": 60, "wait_time_mins": 10, "status": "Yellow"}
    ],
    "announcement": {
        "title": "Smart Routing Active",
        "message": "Heavy traffic at North Gate. Please use East or South exits for faster departure.",
        "type": "warning"
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    return jsonify(venue_status)

if __name__ == '__main__':
    # Local development server (HTTPS enabled for camera access)
    app.run(debug=True, host='0.0.0.0', port=8080, ssl_context='adhoc')
