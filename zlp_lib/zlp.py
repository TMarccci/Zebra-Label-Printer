import os
import sys
import socket
import json

CURRENT_PROGRAM_VERSION = "1.1.2"
USER = os.getenv("USERNAME")
APP_FOLDER = f"C:\\Users\\{USER}\\Zebra Label Printer"
CONFIG_FILE = os.path.join(APP_FOLDER, "gui_config.json")

DEFAULT_CONFIG = {
    "server_port": "5000",
    "printer_ip": "127.0.0.1",
    "printer_port": "9100",
    "currency": "HUF",
    "show_decimals": False,
    "decimal_places": 2,
    "price_suggestion_type": "Hungary",
    "start_server_on_launch": True
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
        return True
    except:
        print(f"Failed to send test print to IP: {ip}")
        return False
    
def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        print("Config file missing. Created default config.")
        return DEFAULT_CONFIG.copy()
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def save_config(cfg):
    if not os.path.exists(APP_FOLDER):
        os.makedirs(APP_FOLDER)
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=4)
        print("Config saved!")