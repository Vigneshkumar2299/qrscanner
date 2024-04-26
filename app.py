# Import necessary libraries
import cv2
import numpy as np
from flask import Flask, request, render_template

# Initialize Flask app
app = Flask(__name__)

# Route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for uploading file and decoding QR code
@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        decoded_data = decode_qr(uploaded_file)
        return f"Decoded data: {decoded_data}"
    return "No file uploaded"

# Function to decode QR code from uploaded image
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
# Route for scanning QR code using webcam
@app.route('/scan')
def scan_qr():
    detector = cv2.QRCodeDetector()
    
    # Try different camera indices
    for index in range(4):
        cap = cv2.VideoCapture(index)
        if not cap.isOpened():
            continue  # Try the next index if the camera is not opened
        while True:
            ret, img = cap.read()
            if not ret:
                continue  # Skip empty frames
            data, _, _ = detector.detectAndDecode(img)
            if data:
                cap.release()
                cv2.destroyAllWindows()
                return f"Scanned QR data: {data}"
            cv2.imshow('Scan QR Code', img)
            if cv2.waitKey(1) == ord('q'):
                break
        cap.release()

    cv2.destroyAllWindows()
    return "No QR code detected"


if __name__ == '__main__':
    app.run(debug=True)
