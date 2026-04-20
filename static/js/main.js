// Global variables for AI
let globalModel = null;
let peopleCount = 0;

async function fetchStatus() {
    try {
        const response = await fetch('/api/status');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        
        // Update announcement
        document.getElementById('announcementTitle').textContent = data.announcement.title;
        document.getElementById('announcementMessage').textContent = data.announcement.message;
        
        // Update zones
        const zoneGrid = document.getElementById('zoneGrid');
        zoneGrid.innerHTML = '';
        
        data.zones.forEach(zone => {
            // Inject AI data dynamically over the dummy backend for the user's camera zone
            if (zone.id === 'A') {
                zone.name = "Local Sector (Camera)";
                zone.congestion = Math.min(100, peopleCount * 25); // Set 4 people = 100% capacity for demo purposes
                zone.wait_time_mins = peopleCount * 5;
                if (zone.congestion > 70) zone.status = 'Red';
                else if (zone.congestion > 30) zone.status = 'Yellow';
                else zone.status = 'Green';
            }

            const colorClass = zone.status.toLowerCase();
            const card = document.createElement('div');
            card.className = `zone-card ${colorClass}`;
            
            card.innerHTML = `
                <div class="zone-header">
                    <span class="zone-id">Zone ${zone.id}</span>
                    <span class="status-indicator"></span>
                </div>
                <h3>${zone.name}</h3>
                <div class="metrics">
                    <div class="metric">
                        <span class="label">Wait Time</span>
                        <span class="value">${zone.wait_time_mins} min</span>
                    </div>
                    <div class="metric">
                        <span class="label">Congestion</span>
                        <span class="value">${zone.congestion}%</span>
                    </div>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill ${colorClass}-bg" style="width: ${zone.congestion}%"></div>
                </div>
            `;
            zoneGrid.appendChild(card);
        });
        
    } catch (error) {
        console.error("Error fetching status:", error);
    }
}

// Initialize Camera and AI Model
async function initCamera() {
    try {
        // Request camera permission
        const stream = await navigator.mediaDevices.getUserMedia({ video: true });
        const videoEl = document.getElementById('crowdCamera');
        videoEl.srcObject = stream;
        
        // Wait for video dimensions to load before setting up canvas
        videoEl.onloadedmetadata = async () => {
            // Load the AI model
            try {
                globalModel = await cocoSsd.load();
                
                // Update UI status
                const statusBadge = document.getElementById('aiStatus');
                statusBadge.style.color = '#10b981';
                statusBadge.style.borderColor = '#10b981';
                statusBadge.innerHTML = `<span class="pulse-dot green" style="width: 6px; height: 6px; display: inline-block; border-radius: 50%; background: #10b981;"></span> Crowd Detection Active`;
                
                // Start detection loop
                detectFrame();
            } catch (modelErr) {
                console.error("Model failed to load:", modelErr);
                document.getElementById('aiStatus').innerHTML = `❌ Model Error`;
            }
        };
    } catch (err) {
        console.error("Camera access denied or unavailable", err);
        const statusBadge = document.getElementById('aiStatus');
        if (statusBadge) {
            statusBadge.innerHTML = `❌ Camera Error`;
            statusBadge.style.color = '#ef4444';
            statusBadge.style.borderColor = '#ef4444';
        }
    }
}

async function detectFrame() {
    if (!globalModel) return;
    
    const videoEl = document.getElementById('crowdCamera');
    const canvas = document.getElementById('overlay');
    if (!videoEl || !canvas) return;
    
    const ctx = canvas.getContext('2d');
    
    if (videoEl.readyState === 4) {
        // Ensure canvas matches video dimensions exactly
        canvas.width = videoEl.videoWidth;
        canvas.height = videoEl.videoHeight;
        
        // Run inference
        const predictions = await globalModel.detect(videoEl);
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        let detectedPeople = 0;
        
        predictions.forEach(prediction => {
            // We only care about people for crowd detection
            if (prediction.class === 'person') {
                detectedPeople++;
                const [x, y, width, height] = prediction.bbox;
                
                // Draw glowing box
                ctx.strokeStyle = '#10b981';
                ctx.lineWidth = 3;
                ctx.strokeRect(x, y, width, height);
                
                // Draw label background
                ctx.fillStyle = '#10b981';
                ctx.fillRect(x, y > 25 ? y - 25 : 0, 110, 25);
                
                // Draw text
                ctx.fillStyle = '#111';
                ctx.font = '14px Outfit, sans-serif';
                ctx.fontWeight = 'bold';
                ctx.fillText(`Person (${Math.round(prediction.score * 100)}%)`, x + 5, y > 10 ? y - 8 : 17);
            }
        });
        
        // Update global count for the dashboard
        peopleCount = detectedPeople;
    }
    
    // Loop recursively tailored to browser repaints
    requestAnimationFrame(detectFrame);
}

// Start execution
window.addEventListener('load', () => {
    fetchStatus();
    initCamera();
    setInterval(fetchStatus, 3000); // Polling faster to show AI responsiveness
});
