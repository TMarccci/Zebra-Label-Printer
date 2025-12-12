import os
import sys
import socket
import json
import qrcode
from PyQt5.QtWidgets import QMessageBox, QLabel
from PyQt5.QtGui import QPixmap

CURRENT_PROGRAM_VERSION = "1.0.0"
USER = os.getenv("USERNAME")
APP_FOLDER = f"C:\\Users\\{USER}\\Zebra Label Printer"
CONFIG_FILE = os.path.join(APP_FOLDER, "gui_config.json")

DEFAULT_CONFIG = {
    "server_port": "5000",
    "printer_ip": "172.0.0.1",
    "printer_port": "9100",
    "currency": "HUF",
    "show_decimals": False,
    "decimal_places": 2,
    "price_suggestion_type": "Hungary",
    "start_server_on_launch": False
}

def resource_path(relative_path):
    try:
        base = sys._MEIPASS
    except:
        base = os.path.abspath(".")
    return os.path.join(base, relative_path)

def test_print(ip):
    try:
        print(f"Testing print to IP: {ip}")
        sock = socket.create_connection((str(ip), 9100), timeout=1)
        sock.sendall(b"^XA^FO50,50^ADN,36,20^FDTest Print^FS^XZ")
        sock.close()
        QMessageBox.information(None, "Test Print", f"Test print sent to {ip} successfully.")
        return True
    except:
        print(f"Failed to send test print to IP: {ip}")
        QMessageBox.warning(None, "Test Print", f"Failed to send test print to {ip}.")
        return False
    
def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        print("Config file missing. Created default config.")
        return DEFAULT_CONFIG.copy()
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=4)
        print("Config saved!")
        
def show_qr(self):
    print("Generating QR code...")
    port = self.server_port_input.text().strip()
    url = f"http://192.168.137.1:{port}"

    # Generate QR
    qr = qrcode.QRCode(box_size=6, border=2)
    qr.add_data(url)
    qr.make()
    img = qr.make_image(fill_color="black", back_color="white")

    temp_path = os.path.join(APP_FOLDER, "qrcode_temp.png")
    img.save(temp_path)

    msg = QMessageBox(self)
    msg.setWindowTitle("QR Code")
    msg.setIcon(QMessageBox.Information)

    qr_label = QLabel()
    pix = QPixmap(temp_path)
    qr_label.setPixmap(pix)

    msg.layout().addWidget(qr_label, 1, 1)
    msg.exec_()