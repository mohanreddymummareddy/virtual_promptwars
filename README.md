# StadiaSync 🏟️
**Virtual PromptWars Submission**

StadiaSync is a dynamic, smart-routing and crowd-control dashboard designed to improve the physical event experience at large-scale sporting venues. By leveraging real-time Computer Vision via Edge AI, it analyzes crowd congestion to accurately predict wait times and optimally route attendees to less crowded checkpoints.

## 🚀 Features

- **Real-Time Edge AI Detection:** Utilizing `TensorFlow.js` and the `Coco-SSD` object detection model, StadiaSync harnesses the device's camera stream directly in the browser to accurately identify crowd volumes.
- **Dynamic Heatmapping:** The UI transforms data organically based on spatial tracking. When crowd density increases locally, congestion alerts (Red/Yellow/Green statuses) reflect instantly.
- **Smart Routing:** Algorithmically suggests the fastest available local pathways (e.g., restrooms, gates, concessions) to minimize line dwell time based on cross-venue data.
- **Premium Interface:** A fully responsive Custom Glassmorphism UI that acts as an all-in-one coordination point.

## 🛠️ Technology Stack

- **Backend Architecture:** Python, Flask, Gunicorn
- **Frontend Layer:** HTML5, CSS3 Variables (No heavy frameworks), Vanilla JavaScript
- **Computer Vision:** `@tensorflow/tfjs`, `@tensorflow-models/coco-ssd`
- **Deployment:** Dockerized for Google Cloud Run

## 💻 Local Installation

To run StadiaSync locally on your machine:

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd Virtual_PromptWars
   ```

2. **Create a Python Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Server (HTTPS Enabled):**
   ```bash
   python app.py
   ```
   *Note: Ensure to browse to `https://127.0.0.1:8080/` (HTTPS, not HTTP) and accept the self-signed certificate. HTTPS is required by all modern web browsers in order to grant access to the `navigator.mediaDevices` web camera API out of the box.*

## ☁️ Cloud Deployment (Google Cloud Run)

StadiaSync comes fully bundled with a highly lightweight Alpine/Slim Python Dockerfile configuration.

To deploy via Google Cloud Shell:
```bash
gcloud run deploy stadiasync \
  --source . \
  --allow-unauthenticated \
  --port 8080 \
  --region us-central1 \
  --project <YOUR_GCP_PROJECT_ID>
```
