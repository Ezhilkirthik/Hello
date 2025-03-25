from flask import Flask, request, render_template_string, jsonify
import time
import json
from user_agents import parse  # For parsing user agent
import os
import requests
import socket

app = Flask(__name__)

# Store collected data
visitor_data = []

# Replace with your Render.com endpoint
RENDER_ENDPOINT = "https://hello-b8qv.onrender.com/log"

@app.route('/track')
def track():
    # Server-side data collection
    ip_address = request.remote_addr
    raw_user_agent = request.headers.get('User-Agent', 'Unknown')
    headers = dict(request.headers)

    # Parse user agent
    ua = parse(raw_user_agent)
    
    # Attempt reverse DNS lookup for hostname
    try:
        hostname = socket.gethostbyaddr(ip_address)[0]
    except (socket.herror, socket.gaierror):
        hostname = 'Unknown'

    # Create a "browser profile name" from key attributes
    browser_profile_name = (
        f"{ua.browser.family or 'Unknown'}-{ua.browser.version_string or 'Unknown'}_"
        f"{ua.os.family or 'Unknown'}-{ua.os.version_string or 'Unknown'}_"
        f"{ua.device.family or 'Unknown'}-{ua.device.brand or 'Unknown'}"
    ).replace(" ", "-")

    visitor_info = {
        'ip': ip_address,
        'hostname': hostname,
        'user_agent': raw_user_agent,
        'browser_profile_name': browser_profile_name,  # Added browser profile name
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

    # HTML with extensive client-side data collection
    html = """
    <html>
    <body>
        <h1>Data Collection in Progress</h1>
        <p>Your information has been recorded.</p>
        <script>
            // Collect extensive client-side data
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
                doNotTrack: navigator.doNotTrack || window.doNotTrack || 'Not set',
                plugins: Array.from(navigator.plugins || []).map(p => ({
                    name: p.name,
                    version: p.version,
                    description: p.description
                })),
                mimeTypes: Array.from(navigator.mimeTypes || []).map(m => ({
                    type: m.type,
                    description: m.description
                })),
                webgl: (function() {
                    try {
                        const canvas = document.createElement('canvas');
                        const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
                        if (gl) {
                            const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                            return {
                                vendor: debugInfo ? gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL) : gl.getParameter(gl.VENDOR),
                                renderer: debugInfo ? gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER)
                            };
                        }
                        return 'Not supported';
                    } catch (e) {
                        return 'Error: ' + e.message;
                    }
                })(),
                fonts: (function() {
                    const baseFonts = ['monospace', 'sans-serif', 'serif'];
                    const testString = 'abcdefghijklmnopqrstuvwxyz0123456789';
                    const testSize = '72px';
                    const canvas = document.createElement('canvas');
                    const ctx = canvas.getContext('2d');
                    const detectedFonts = [];
                    baseFonts.forEach(base => {
                        const baseWidth = ctx.measureText(testString).width;
                        ['Arial', 'Times New Roman', 'Courier New', 'Verdana', 'Georgia', 'Comic Sans MS', 'Trebuchet MS', 'Impact'].forEach(font => {
                            ctx.font = `${testSize} ${font}, ${base}`;
                            if (ctx.measureText(testString).width !== baseWidth) {
                                detectedFonts.push(font);
                            }
                        });
                    });
                    return detectedFonts.length > 0 ? detectedFonts : 'Not detectable';
                })(),
                touchSupport: 'ontouchstart' in window || navigator.maxTouchPoints > 0 || navigator.msMaxTouchPoints > 0,
                performance: {
                    timing: window.performance.timing ? {
                        navigationStart: window.performance.timing.navigationStart,
                        loadEventEnd: window.performance.timing.loadEventEnd
                    } : 'Not available',
                    memory: window.performance.memory ? {
                        totalJSHeapSize: window.performance.memory.totalJSHeapSize,
                        usedJSHeapSize: window.performance.memory.usedJSHeapSize,
                        jsHeapSizeLimit: window.performance.memory.jsHeapSizeLimit
                    } : 'Not available'
                }
            };

            // Send data to server
            fetch('/log', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(deviceInfo)
            }).then(response => {
                if (response.ok) {
                    console.log('Data sent successfully');
                }
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
        send_to_render(visitor_data[-1])
    return jsonify({'status': 'success'})

def send_to_render(data):
    try:
        response = requests.post(RENDER_ENDPOINT, json=data, timeout=5)
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
