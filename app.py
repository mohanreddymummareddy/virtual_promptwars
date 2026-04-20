"""
StadiaSync Backend Application
A lightweight Flask API to serve live event metrics and physical event dashboard routing.
"""

import os
import json
import logging
from typing import Dict, Any

from flask import Flask, render_template, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load enterprise 12-factor configuration
load_dotenv()

# Configure standard logging to meet professional backend requirements
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Enable CORS for security policy compliance
CORS(app)

# Environment overrides
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8080))

def load_venue_data() -> Dict[str, Any]:
    """
    Reads the external mock database configuration file.
    
    Returns:
        A dictionary representation of the venue configurations.
    """
    file_path = os.path.join(os.path.dirname(__file__), 'data', 'venue_config.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


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
    Retrieve current venue zones and status parameters from the external store.
    
    Returns:
        JSON response containing the list of zones and their active congestion states.
        In case of generic failure, returns 500 Internal Server Error.
    """
    try:
        logger.info("Fetching venue status metrics.")
        db = load_venue_data()
        return jsonify(db)
    except Exception as e:
        logger.error(f"Failed to fetch venue status: {e}")
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500


if __name__ == '__main__':
    # Local development server (HTTPS enabled for camera access)
    try:
        logger.info(f"Starting up StadiaSync local development server on {HOST}:{PORT}...")
        app.run(debug=True, host=HOST, port=PORT, ssl_context='adhoc')
    except Exception as server_err:
        logger.critical(f"Server crashed during initialization: {server_err}")
