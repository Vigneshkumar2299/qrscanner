from flask import Flask, render_template
import qrcode

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

# Generate and save QR codes for each machine
for machine in machine_data:
    data = f"Machine Name: {machine['name']}\nSerial Number: {machine['serial_number']}"
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the QR code image
    img.save(f"static/{machine['name'].replace(' ', '_')}_QRCode.png")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
 
