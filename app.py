from flask import Flask, request, render_template_string, jsonify
import time
import json
from user_agents import parse

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
    device_name = ua.device.family if ua.device.family else 'Unknown'
    # Handle "K" or unclear device names
    if device_name == 'K' or device_name == 'Unknown' or not device_name:
        device_name = f"Undetected Device (UA: {raw_user_agent[:50]})"

    visitor_info = {
        'ip': ip_address,
        'user_agent': raw_user_agent,
        'device': device_name,
        'device_brand': ua.device.brand if ua.device.brand else 'Unknown',
        'os': ua.os.family if ua.os.family else 'Unknown',
        'os_version': ua.os.version_string if ua.os.version_string else 'Unknown',
        'browser': ua.browser.family if ua.browser.family else 'Unknown',
        'browser_version': ua.browser.version_string if ua.browser.version_string else 'Unknown',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'headers': headers,
        'note': 'Wi-Fi SSID or specific network name not accessible via web without native app permissions'
    }
    visitor_data.append(visitor_info)

    # HTML with JavaScript for client-side data
    html = """
    <html>
    <body>
        <h1>Tracking Active</h1>
        <p>Data collected successfully. Visit /view_data to see details.</p>
        <script>
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
                    effectiveType: navigator.connection.effectiveType || 'Unknown',
                    downlink: navigator.connection.downlink || 'Unknown',
                    rtt: navigator.connection.rtt || 'Unknown',
                    type: navigator.connection.type || 'Unknown'
                } : 'Not available',
                cookiesEnabled: navigator.cookieEnabled,
                doNotTrack: navigator.doNotTrack || window.doNotTrack || 'Not set'
            };

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
        # Save to file (temporary on Render)
        with open('visitor_data.json', 'a') as f:
            json.dump(visitor_data[-1], f)
            f.write('\n')
    return jsonify({'status': 'success'})

@app.route('/view_data')
def view_data():
    try:
        with open('visitor_data.json', 'r') as f:
            data = f.readlines()
        return "<pre>" + "".join(data) + "</pre>"
    except FileNotFoundError:
        return "No data collected yet. Open /track to start collecting."

@app.route('/')
def root():
    return "Welcome to the tracker. Visit /track to collect data."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
