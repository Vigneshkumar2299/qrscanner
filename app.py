from flask import Flask, render_template, jsonify
import qrcode
from google.cloud import bigquery
import os

app = Flask(__name__)

# Specify the path to your JSON key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gkey.json"

# Initialize BigQuery client
client = bigquery.Client()

# Example machine data
MACHINE_DATA = [
    {"DeviceID": "1001"},
    {"DeviceID": "1002"},
    {"DeviceID": "1003"},
    {"DeviceID": "1004"},
    {"DeviceID": "1005"},
    {"DeviceID": "1006"},
    {"DeviceID": "1007"},
    {"DeviceID": "1008"},
    {"DeviceID": "1009"},
    {"DeviceID": "1010"},
    {"DeviceID": "1011"},
    {"DeviceID": "1012"},
]

# Generate and save QR codes for each machine
for machine in MACHINE_DATA:
    data = f"Machine Name: {machine['DeviceID']}"
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code image
    img.save(f"static/{machine['DeviceID'].replace(' ', '_')}_QRCode.png")


@app.route('/')
def index():
    return render_template('index.html', machine_data=MACHINE_DATA)


@app.route('/machine_details/<device_id>')
def machine_details(device_id):
    # Extract numeric part from device_id
    device_id_numeric = device_id.split(':')[1].strip()

    try:
        # Convert numeric part to integer
        device_id_int = int(device_id_numeric)

        # Query BigQuery for machine details based on DeviceID
        query = f"""
            SELECT Machine_No, Unit
            FROM `shining-wharf-418413.bq_idle.machine_status`
            WHERE DeviceID = {device_id_int}
        """
        query_job = client.query(query)
        results = query_job.result()
        machine_details = [dict(row) for row in results]
        return jsonify(machine_details)
    except ValueError:
        # Handle the case where device_id_numeric is not a valid integer
        return "Invalid device ID", 400




if __name__ == '__main__':
    app.run(debug=True)
