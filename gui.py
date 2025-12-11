import sys
import os
import subprocess
import psutil
import webbrowser
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QCheckBox, QSpinBox,
    QRadioButton
)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtNetwork import QLocalServer
import requests
import qrcode


# ---------------------------------------
# MARK: CONFIG
# ---------------------------------------
APP_FOLDER = os.path.join(os.path.expanduser("~"), "Documents", "Zebra Label Printer")
os.makedirs(APP_FOLDER, exist_ok=True)
print(f"App folder ensured at: {APP_FOLDER}")

CONFIG_FILE = os.path.join(APP_FOLDER, "gui_config.json")

DEFAULT_CONFIG = {
    "server_port": "5000",
    "printer_ip": "172.19.81.218",
    "printer_port": "9100",
    "currency": "HUF",
    "show_decimals": False,
    "decimal_places": 2,
    "price_suggestion_type": "Hungary",
    "start_server_on_launch": False
}

def load_config():
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        print("Config file missing. Created default config.")
        return DEFAULT_CONFIG.copy()
    with open(CONFIG_FILE, "r") as f:
        print("Config loaded!")
        return json.load(f)

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=4)
        print("Config saved!")


# ---------------------------------------
# MARK: HELPERS
# ---------------------------------------
def resource_path(relative_path):
    try:
        base = sys._MEIPASS
        print(f"Base path (frozen): {base}")
    except:
        base = os.path.abspath(".")
        print(f"Base path: {base}")
    return os.path.join(base, relative_path)

def get_server_path():
    try:
        base = sys._MEIPASS
        print(f"Base path (frozen): {base}")
    except:
        base = os.path.abspath(".")
        print(f"Base path: {base}")
    
    if "--dev" in sys.argv:
        print("Development mode detected.")
        return os.path.join(base, "zebra-server.py")
    return os.path.join(base, "zebra-server.exe")

def kill_all_servers():
    cfg = load_config()
    try:
        print("Sending stop request to server...")
        requests.get(f"http://127.0.0.1:{cfg.get('server_port')}/stop", timeout=1)
    except requests.exceptions.ConnectionError:
        print("Server stopped.")
    except requests.exceptions.ReadTimeout:
        print("Server stopped (timeout).")

def server_running():
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"]:
            if proc.info["name"].lower() == "zebra-server.exe":
                return True
            if "--dev" in sys.argv:
                if proc.info["name"].lower() in ["python.exe", "python3.exe", "python"]:
                    try:
                        # Accessing cmdline can race if the process exits; handle gracefully.
                        for cmd in proc.cmdline():
                            if "zebra-server.py" in cmd:
                                return True
                    except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
                        # Process disappeared or denied; just skip this one.
                        continue
    return False


# ---------------------------------------
# MARK: SINGLE INSTANCE
# ---------------------------------------
def check_single_instance():
    server = QLocalServer()
    if not server.listen("label_printer_gui_single_instance"):
        print("Another instance is already running.")
        QMessageBox.warning(None, "Already Running", "Another instance of the GUI is already running.")
        return False
    return True


# ---------------------------------------
# MARK: GUI
# ---------------------------------------
class ControlGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zebra Label Printer")
        self.resize(350, 360)

        self.server_process = None
        self.config = load_config()

        self.setup_ui()
        self.connect_signals()

        # Poll every second
        self.poll = QTimer(self)
        self.poll.timeout.connect(self.update_status)
        self.poll.start(1000)

        # Autostart
        if self.config.get("start_server_on_launch", False):
            print("Autostarting server...")
            QTimer.singleShot(2000, self.start_server)

    # UI
    def setup_ui(self):
        layout = QVBoxLayout()

        self.status_label = QLabel("🔴 Server Stopped")
        self.status_label.setStyleSheet("font-size: 16px")
        layout.addWidget(self.status_label)

        layout.addSpacing(20)

        layout.addWidget(QLabel("Server Settings:"))
        layout.addLayout(self._row("Webserver Port:", "server_port"))
        layout.addLayout(self._row("Printer IP:", "printer_ip"))
        layout.addLayout(self._row("Printer Port:", "printer_port"))
        self.autostart_checkbox = QCheckBox("Start server on launch")
        self.autostart_checkbox.setChecked(self.config.get("start_server_on_launch"))
        layout.addWidget(self.autostart_checkbox)
        
        layout.addSpacing(20)
        
        layout.addWidget(QLabel("Currency Settings:"))
        layout.addLayout(self._radio_row("Price Suggestion Type:", ["Hungary", "Poland", "Czech"], "price_suggestion_type"))
        layout.addLayout(self._row("Visible Currency:", "currency"))

        # decimal settings
        hl = QHBoxLayout()
        self.decimals_checkbox = QCheckBox("Show decimals")
        self.decimals_checkbox.setChecked(self.config["show_decimals"])
        hl.addWidget(self.decimals_checkbox)

        self.decimals_spin = QSpinBox()
        self.decimals_spin.setRange(0, 4)
        self.decimals_spin.setValue(self.config["decimal_places"])
        hl.addWidget(self.decimals_spin)
        layout.addLayout(hl)
        
        layout.addSpacing(20)

        layout.addWidget(self.button("Save Settings", "save_btn"))
        
        layout.addSpacing(30)

        hl2 = QHBoxLayout()
        hl2.addWidget(self.button("Start Server", "start_btn"))
        hl2.addWidget(self.button("Stop Server", "stop_btn"))
        layout.addLayout(hl2)

        layout.addWidget(self.button("Open Printer Page", "open_web_btn"))

        # NEW BUTTON: QR Code
        layout.addWidget(self.button("QR Code", "qr_btn"))

        self.setLayout(layout)

    def _row(self, label, cfg_key):
        hl = QHBoxLayout()
        hl.addWidget(QLabel(label))
        field = QLineEdit(self.config[cfg_key])
        setattr(self, f"{cfg_key}_input", field)
        hl.addWidget(field)
        return hl
    
    def _radio_row(self, label, options, cfg_key):
        hl = QHBoxLayout()
        hl.addWidget(QLabel(label))
        # Radio buttons would go here
        radios = []
        for opt in options:
            rb = QRadioButton(opt)
            if self.config[cfg_key] == opt:
                rb.setChecked(True)
            radios.append(rb)
            hl.addWidget(rb)
        setattr(self, f"{cfg_key}_radios", radios)
        
        return hl

    def button(self, text, attr):
        btn = QPushButton(text)
        setattr(self, attr, btn)
        return btn

    def connect_signals(self):
        self.start_btn.clicked.connect(self.start_server)
        self.stop_btn.clicked.connect(self.stop_server)
        self.save_btn.clicked.connect(self.save_settings)
        self.open_web_btn.clicked.connect(self.open_web)
        self.qr_btn.clicked.connect(self.show_qr)

    # ---------------------------------------
    # MARK: QR CODE POPUP
    # ---------------------------------------
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

    # ---------------------------------------
    # MARK: SERVER CONTROL
    # ---------------------------------------
    def start_server(self):
        if not server_running():
            kill_all_servers()  # ensure clean start

            port = self.server_port_input.text().strip()
            server_path = get_server_path()
            try:
                if server_path.endswith('.py'):
                    self.server_process = subprocess.Popen(
                        [sys.executable, server_path, port],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                else:
                    self.server_process = subprocess.Popen(
                        [server_path, port],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
            except Exception as e:
                QMessageBox.critical(self, "Start Error", str(e))
        else:
            QMessageBox.warning(self, "Warning!", "Server is already running!")

    def stop_server(self):
        kill_all_servers()
        self.server_process = None
        self.update_status()

    # ---------------------------------------
    # MARK: SETTINGS
    # ---------------------------------------
    def save_settings(self):
        cfg = {
            "server_port": self.server_port_input.text(),
            "printer_ip": self.printer_ip_input.text(),
            "printer_port": self.printer_port_input.text(),
            "currency": self.currency_input.text(),
            "show_decimals": self.decimals_checkbox.isChecked(),
            "decimal_places": self.decimals_spin.value(),
            "price_suggestion_type": next(
                (rb.text() for rb in self.price_suggestion_type_radios if rb.isChecked()), "Hungary"
            ),
            "start_server_on_launch": self.autostart_checkbox.isChecked()
        }
        save_config(cfg)
        QMessageBox.information(self, "Saved", "Settings saved.")

    # ---------------------------------------
    # MARK: STATUS
    # ---------------------------------------
    def update_status(self):
        if server_running():
            self.status_label.setText("✔ Server Running")
        else:
            self.status_label.setText("🔴 Server Stopped")

    # ---------------------------------------
    # MARK: OPEN WEB
    # ---------------------------------------
    def open_web(self):
        print("Opening web interface...")
        port = self.server_port_input.text().strip()
        webbrowser.open(f"http://127.0.0.1:{port}")

    # ---------------------------------------
    # MARK: EXIT
    # ---------------------------------------
    def closeEvent(self, ev):
        kill_all_servers()
        QTimer.singleShot(200, QApplication.instance().quit)
        ev.ignore()


# ---------------------------------------
# MARK: ENTRY
# ---------------------------------------
def run_gui():
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("static/icon.ico")))

    if not check_single_instance():
        sys.exit(0)

    gui = ControlGUI()
    gui.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    run_gui()
