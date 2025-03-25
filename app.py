from flask import Flask, request, render_template_string, jsonify
import time
import json
from user_agents import parse  # For parsing user agent
import os

app = Flask(__name__)

# Store collected data
visitor_data = []

@app.route('/track')
def track():
    # Server-side data collection
    ip_address = request.remote_addr
    raw_user_agent = request.headers.get('User-Agent', 'Unknown')
    headers = dict(request.headers)

    # Parse user agent for device details
    ua = parse(raw_user_agent)
    visitor_info = {
        'ip': ip_address,
        'user_agent': raw_user_agent,
        'device': ua.device.family if ua.device.family else 'Unknown',
        'device_brand': ua.device.brand if ua.device.brand else 'Unknown',
        'os': ua.os.family if ua.os.family else 'Unknown',
        'os_version': ua.os.version_string if ua.os.version_string else 'Unknown',
        'browser': ua.browser.family if ua.browser.family else 'Unknown',
        'browser_version': ua.browser.version_string if ua.browser.version_string else 'Unknown',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'headers': headers
    }
    visitor_data.append(visitor_info)

    # HTML with JavaScript for client-side data
    html = """
    <html>
    <body>
        <h1>Tracking Active</h1>
        <p>Data collected successfully. Check server logs for details.</p>
        <script>
            // Collect client-side data
            const deviceInfo = {
                screenWidth: screen.width,
                screenHeight: screen.height,
                windowWidth: window.innerWidth,
                windowHeight: window.innerHeight,
                colorDepth: screen.colorDepth,
                pixelRatio: window.devicePixelRatio,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                languages: navigator.languages || [navigator.language || navigator.userLanguage],
                platform: navigator.platform,
                memory: navigator.deviceMemory || 'Not available',
                cpuCores: navigator.hardwareConcurrency || 'Not available',
                connection: (navigator.connection || navigator.mozConnection || navigator.webkitConnection) ? {
                    effectiveType: navigator.connection.effectiveType,
                    downlink: navigator.connection.downlink,
                    rtt: navigator.connection.rtt
                } : 'Not available',
                cookiesEnabled: navigator.cookieEnabled,
                doNotTrack: navigator.doNotTrack || window.doNotTrack || 'Not set'
            };

            // Send data to server
            fetch('/log', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(deviceInfo)
            }).catch(err => console.log('Error sending data:', err));
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
        print("Full visitor info:", json.dumps(visitor_data[-1], indent=2))
    return jsonify({'status': 'success'})

@app.route('/')
def root():
    return "Welcome to the tracker. Visit /track to collect data."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
