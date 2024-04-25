import qrcode
from flask import Flask, request, render_template
import cv2
from PIL import Image
import numpy as np

app = Flask(__name__)

# Data for each machine (you can replace this with your actual machine data)
machine_data = [
    {"name": "Machine 1", "serial_number": "123456"},
    {"name": "Machine 2", "serial_number": "789012"},
    {"name": "Machine 3", "serial_number": "345678"},
    {"name": "Machine 4", "serial_number": "901234"},
    {"name": "Machine 5", "serial_number": "567890"},
    {"name": "Machine 6", "serial_number": "234567"},
    {"name": "Machine 7", "serial_number": "890123"},
    {"name": "Machine 8", "serial_number": "456789"},
    {"name": "Machine 9", "serial_number": "012345"},
    {"name": "Machine 10", "serial_number": "678901"},
    {"name": "Machine 11", "serial_number": "345678"},
    {"name": "Machine 12", "serial_number": "901234"}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        decoded_data = decode_qr(uploaded_file)
        return f"Decoded data: {decoded_data}"
    return "No file uploaded"

def decode_qr(uploaded_file):
    image_stream = uploaded_file.read()
    nparr = np.frombuffer(image_stream, np.uint8)
    image_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    qr_decoder = cv2.QRCodeDetector()
    data, bbox, _ = qr_decoder.detectAndDecode(gray)
    if bbox is not None:
        return data
    else:
        return "No QR code detected"

if __name__ == '__main__':
    app.run(debug=True)
