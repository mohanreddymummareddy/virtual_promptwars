"""
StadiaSync Backend Application
A lightweight Flask API to serve live event metrics and physical event dashboard routing.
"""

import logging
from typing import Dict, Any

from flask import Flask, render_template, jsonify

# Configure standard logging to meet professional backend requirements
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Simulated in-memory database representation
VENUE_STATUS_DB: Dict[str, Any] = {
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
def index() -> str:
    """
    Serve the main StadiaSync dashboard.
    
    Returns:
        str: Rendered HTML template containing the application UI.
    """
    logger.info("Serving main dashboard index.")
    return render_template('index.html')


@app.route('/api/status')
def get_status() -> Any:
    """
    Retrieve current venue zones and status parameters.
    
    Returns:
        JSON response containing the list of zones and their active congestion states.
        In case of generic failure, returns 500 Internal Server Error.
    """
    try:
        logger.info("Fetching venue status metrics.")
        return jsonify(VENUE_STATUS_DB)
    except Exception as e:
        logger.error(f"Failed to fetch venue status: {e}")
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


if __name__ == '__main__':
    # Local development server (HTTPS enabled for camera access)
    try:
        logger.info("Starting up StadiaSync local development server...")
        app.run(debug=True, host='0.0.0.0', port=8080, ssl_context='adhoc')
    except Exception as server_err:
        logger.critical(f"Server crashed during initialization: {server_err}")
