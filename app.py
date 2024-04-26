from flask import Flask, render_template, jsonify
import qrcode
from google.cloud import bigquery
import os

app = Flask(__name__)

# Initialize BigQuery client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gkey.json"
client = bigquery.Client()

# Example machine data
MACHINE_DATA = [{"DeviceID": f"100{i}"} for i in range(1, 13)]

@app.route('/')
def index():
    return render_template('index.html', machine_data=MACHINE_DATA)

@app.route('/machine_details/<device_id>')
def machine_details(device_id):
    try:
        device_id_numeric = device_id.split(':')[1].strip()
        device_id_int = int(device_id_numeric)

        # Query BigQuery for machine details based on DeviceID
        query = "SELECT Machine_No, Unit FROM `shining-wharf-418413.bq_idle.machine_status` WHERE DeviceID = @device_id"
        job_config = bigquery.QueryJobConfig(query_parameters=[bigquery.ScalarQueryParameter("device_id", "INT64", device_id_int)])
        query_job = client.query(query, job_config=job_config)
        results = query_job.result()
        machine_details = [dict(row) for row in results]
        return jsonify(machine_details)
    except (ValueError, IndexError):
        return "Invalid device ID", 400

@app.route('/qr_code/<device_id>')
def generate_qr_code(device_id):
    try:
        data = f"Machine Name: {device_id}"
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(data)
        qr_image = qr.make_image(fill_color="black", back_color="white")

        # You might want to save the QR code image or return it directly based on your requirements
        # qr_image.save(f"static/{device_id.replace(' ', '_')}_QRCode.png")

        # For simplicity, returning the image as a response
        return qr_image
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
