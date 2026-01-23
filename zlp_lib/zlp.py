import os
import sys
import socket
import json
from zebra import Zebra

CURRENT_PROGRAM_VERSION = "1.2.1"
USER = os.getenv("USERNAME")
APP_FOLDER = f"C:\\Users\\{USER}\\Zebra Label Printer"
CONFIG_FILE = os.path.join(APP_FOLDER, "gui_config.json")

DEFAULT_CONFIG = {
    "server_port": "5000",
    "printer_ip": "127.0.0.1",
    "printer_port": "9100",
    # Printing mode:
    # - "NET/TCP": print to a network printer via IP:9100
    # - "USB": print to a locally connected USB printer
    "print_mode": "NET/TCP",
    # Selected USB printer name (only used when print_mode == "USB")
    "usb_printer": "",
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
    
def test_usb_print(printer_name):
    try:
        print(f"Testing USB print to printer: {printer_name}")
        zebra = Zebra(printer_name)
        zebra.output("^XA^FO50,50^ADN,36,20^FDTest Print^FS^XZ")
        return True
    except Exception as e:
        print(f"Failed to send test print to USB printer {printer_name}: {e}")
        return False
    
def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        print("Config file missing. Created default config.")
        return DEFAULT_CONFIG.copy()

    with open(CONFIG_FILE, "r") as f:
        cfg = json.load(f)

    # Non-destructive migration: add any missing default keys without
    # touching existing user values.
    changed = False
    for k, v in DEFAULT_CONFIG.items():
        if k not in cfg:
            cfg[k] = v
            changed = True

    if changed:
        save_config(cfg)

    return cfg

def save_config(cfg):
    if not os.path.exists(APP_FOLDER):
        os.makedirs(APP_FOLDER)

    # Preserve unknown keys: merge into existing config (if any)
    merged = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                merged = json.load(f) or {}
        except Exception:
            merged = {}
    if not isinstance(merged, dict):
        merged = {}

    merged.update(cfg)

    with open(CONFIG_FILE, "w") as f:
        json.dump(merged, f, indent=4)
        print("Config saved!")
        
def get_usb_printers():
    """Return a list of connected USB Zebra printers."""
    printers = []
    try:
        zebra = Zebra()
        usb_printers = zebra.getqueues()
        for p in usb_printers:
            printers.append(p)
    except Exception as e:
        print(f"Error enumerating USB printers: {e}")
    return printers