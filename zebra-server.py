import sys
import os
import json
import time
import socket
import signal
from flask import Flask, render_template, request, jsonify

APP_FOLDER = os.path.join(os.path.expanduser("~"), "Documents", "Zebra Label Printer")
CONFIG_FILE = os.path.join(APP_FOLDER, "gui_config.json")

def load_cfg():
    if not os.path.exists(CONFIG_FILE):
        print("ERROR: Config file missing.")
        return {}
    with open(CONFIG_FILE, "r") as f:
        print("Config loaded!")
        return json.load(f)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

app = Flask(__name__,
            template_folder=resource_path("templates"),
            static_folder=resource_path("static"))

cfg = load_cfg()
currency = cfg.get("currency", "HUF")
printer_ip = cfg.get("printer_ip", "127.0.0.1")
printer_port = int(cfg.get("printer_port", 9100))
show_decimals = cfg.get("show_decimals", False)
decimal_places = cfg.get("decimal_places", 2)
price_suggestion_type = cfg.get("price_suggestion_type", "Hungary")

customConfig = {
    'printer_ip': printer_ip,
    'printer_port': printer_port,
    'currency': currency,
    'show_decimals': show_decimals,
    'decimal_places': decimal_places,
    'price_suggestion_type': price_suggestion_type
}

def format_price(value):
    value = float(value)
    return f"{value:.{decimal_places}f}" if show_decimals else str(int(round(value)))

def generate_label(label_type: str, top_text: str, qty: int = 1, bottom_text: str = "", discount: str = "") -> bytes:
    if label_type.lower() == "normal":
        zpl = f"""
        ^XA
        ^CI28
        ^PW248
        ^LL176
        ^LH0,0
        ^FO10,70^FB248,1,0,C^A0N,40,40^FD{top_text}^FS
        ^PQ{qty}
        ^XZ
        """
    elif label_type.lower() == "sale":
        zpl = f"""
        ^XA
        ^CI28
        ^PW248
        ^LL176
        ^LH0,0

        ^FO10,30^FB248,1,0,C^A0N,40,40^FD{top_text}^FS       ; Top price (centered)
        ^FO10,45^GB228,4,4,B,0^FS                           ; Strikethrough line
        ^FO10,67^FB248,1,0,C^A0N,20,20^FD{discount}^FS    ; Percentage
        ^FO10,90^FB248,1,0,C^A0N,40,40^FD{bottom_text}^FS    ; Bottom price (centered)

        ^PQ{qty}
        ^XZ
        """
    else:
        raise ValueError("label_type must be 'normal' or 'sale'")
    return zpl.encode('utf-8')
    
def send_zpl(printer_ip: str, printer_port: int, zpl_code: bytes):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((printer_ip, printer_port))
            s.sendall(zpl_code)
    except Exception as e:
        print(f"Failed to send ZPL code: {e}")

def log(msg, success: bool):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    entry = f"{timestamp} - {'Error: ' if success == False else ''}{msg}"
    print(entry)

    log_file = os.path.join(APP_FOLDER, "log.txt")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(entry + "\n")
        
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", customConfig=customConfig)

    old = float(request.form.get("oldprice", "")) if request.form.get("oldprice", "") else 0.0
    new = request.form.get("newprice", "")
    disc = request.form.get("discount", "")
    qty = int(request.form.get("printqty", 1) or 1)
    
    top_text = f"{format_price(old)} {currency}" if old else f"{format_price(new)} {currency}"
    bottom_text = f"{format_price(float(old) * float(disc))} {currency}" if old and disc else ""
    discount_text = f"- {round((1 - float(disc)) * 100)} %" if old and disc else ""

    if not old and not new:
        log("Empty submission", False)
        return render_template("index.html", customConfig=customConfig)

    if old and disc:
        send_zpl(printer_ip, printer_port, generate_label("sale", f"{top_text}", bottom_text=f"{bottom_text}", qty=qty, discount=f"{discount_text}"))      
        log(f"Printed sale: {top_text} -> {bottom_text} | {discount_text}", True)
        return render_template("index.html", customConfig=customConfig)

    if not old:
        send_zpl(printer_ip, printer_port, generate_label("normal", f"{top_text}", qty=qty))
        log(f"Printed normal: {top_text}", True)
        return render_template("index.html", customConfig=customConfig)

    send_zpl(printer_ip, printer_port, generate_label("sale", f"{top_text}", bottom_text=f"{bottom_text}", qty=qty, discount=f"{discount_text}"))
    log(f"Printed sale: {top_text} -> {bottom_text} | {discount_text}", True)
    return render_template("index.html", customConfig=customConfig)

@app.route('/stop', methods=['GET'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({ "success": True, "message": "Server is shutting down..." })

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(debug=False, host="0.0.0.0", port=port, use_reloader=False)
