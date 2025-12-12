import sys
import os
import subprocess
import psutil
import webbrowser
import requests
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtNetwork import QLocalServer, QLocalSocket
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QCheckBox, QSpinBox,
    QRadioButton, QMenuBar, QVBoxLayout
)

from zlp_lib.zlp import resource_path, load_config, save_config, show_qr, CURRENT_PROGRAM_VERSION, APP_FOLDER, USER
from zlp_gui.printerscan import PrinterScanFlow
from zlp_gui.update import CheckforUpdate

# ---------------------------------------
# MARK: HELPERS
# ---------------------------------------
def get_server_path():
    APP_FOLDER = f"C:\\Users\\{USER}\\Zebra Label Printer\\zlp-server.exe"
    
    if "--dev" in sys.argv:
        print("Development mode detected.")
        base = os.path.abspath(".")
        return os.path.join(base, "zlp-server.py")
    
    return APP_FOLDER

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
            if proc.info["name"].lower() == "zlp-server.exe":
                return True
            if "--dev" in sys.argv:
                if proc.info["name"].lower() in ["python.exe", "python3.exe", "python"]:
                    try:
                        # Accessing cmdline can race if the process exits; handle gracefully.
                        for cmd in proc.cmdline():
                            if "zlp-server.py" in cmd:
                                return True
                    except (psutil.AccessDenied, psutil.NoSuchProcess, psutil.ZombieProcess):
                        # Process disappeared or denied; just skip this one.
                        continue
    return False

# ---------------------------------------
# MARK: SINGLE INSTANCE
# ---------------------------------------
def ensure_single_instance(app):
    name = "zlp_gui_single_instance"

    # Try connecting to an existing server; if successful, another instance is running
    socket = QLocalSocket()
    socket.connectToServer(name)
    if socket.waitForConnected(100):
        QMessageBox.warning(None, "Already Running", "Another instance of the GUI is already running.")
        socket.close()
        return None
    socket.close()

    # Clean up any stale server (e.g., leftover after crash) and listen
    try:
        QLocalServer.removeServer(name)
    except Exception:
        pass

    server = QLocalServer()
    if not server.listen(name):
        QMessageBox.warning(None, "Already Running", "Another instance of the GUI is already running.")
        return None

    # Keep a strong reference so it isn't garbage-collected
    app._single_instance_server = server
    return server

# ---------------------------------------
# MARK: GUI
# ---------------------------------------
class ControlGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zebra Label Printer")
        self.resize(350, 500)
        self.setFixedSize(self.size())

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
        
        # Add MenuBar
        menubar = QMenuBar(self)
        file_menu = menubar.addMenu("File")
        file_menu.addAction("Check for Updates", self.check_for_updates)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About", lambda: QMessageBox.information(self, "About", f"Zebra Label Printer<br>Version {CURRENT_PROGRAM_VERSION}<br><br>Made with ❤️ by Marcell Tihanyi" +
            "<br><br><a href='https://tmarccci.hu'>tmarccci.hu</a>" +
            " | <a href='https://github.com/TMarccci'>GitHub</a>"),)
        layout.setMenuBar(menubar)

        # Status
        self.status_label = QLabel("🔴 Server Stopped")
        self.status_label.setStyleSheet("font-size: 16px")
        layout.addWidget(self.status_label)

        layout.addSpacing(20)

        # Server settings
        layout.addWidget(QLabel("Server Settings:"))
        layout.addLayout(self._row("Webserver Port:", "server_port"))
        hl = QHBoxLayout()
        hl.addWidget(QLabel("Printer IP:"))
        self.printer_ip_input = QLineEdit(self.config["printer_ip"])
        hl.addWidget(self.printer_ip_input)
        hl.addWidget(self.button("Find Printers", "find_printers_btn"))
        layout.addLayout(hl)        
        layout.addLayout(self._row("Printer Port:", "printer_port"))
        self.autostart_checkbox = QCheckBox("Start server on launch")
        self.autostart_checkbox.setChecked(self.config.get("start_server_on_launch"))
        layout.addWidget(self.autostart_checkbox)
        
        layout.addSpacing(20)
        
        # Currency settings
        layout.addWidget(QLabel("Currency Settings:"))
        layout.addLayout(self._radio_row("Price Suggestion Type:", ["Hungary", "Poland", "Czech"], "price_suggestion_type"))
        layout.addLayout(self._row("Visible Currency:", "currency"))

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

        # Server control
        hl2 = QHBoxLayout()
        hl2.addWidget(self.button("Start Server", "start_btn"))
        hl2.addWidget(self.button("Stop Server", "stop_btn"))
        layout.addLayout(hl2)


        # Open web interface
        layout.addWidget(self.button("Open Printer Page", "open_web_btn"))

        # QR Code
        layout.addWidget(self.button("QR Code", "qr_btn"))

        self.setLayout(layout)

    # UI HELPERS
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
        self.qr_btn.clicked.connect(lambda: show_qr(self))
        self.find_printers_btn.clicked.connect(self.find_zebra_printers)

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
                print(f"Server started on port {port} with PID {self.server_process.pid}")
            except Exception as e:
                QMessageBox.critical(self, "Start Error", str(e))
        else:
            QMessageBox.warning(self, "Warning!", "Server is already running!")

    def stop_server(self):
        kill_all_servers()
        self.server_process = None
        self.update_status()

    # ---------------------------------------
    # MARK: FUNCTIONS
    # ---------------------------------------
    def update_status(self):
        if server_running():
            self.status_label.setText("🟢 Server Running")
        else:
            self.status_label.setText("🔴 Server Stopped")
    
    def find_zebra_printers(self):
        flow = PrinterScanFlow()
        flow.start_scan(self)
        
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
        
    def open_web(self):
        print("Opening web interface...")
        port = self.server_port_input.text().strip()
        webbrowser.open(f"http://127.0.0.1:{port}")
        
    def check_for_updates(self):       
        if not hasattr(self, "update_checker") or self.update_checker is None:
            self.update_checker = CheckforUpdate()
        self.update_checker.start_check(self)
        
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

    # Prevent launching if another instance is already running
    if ensure_single_instance(app) is None:
        sys.exit(0)

    gui = ControlGUI()
    gui.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    run_gui()
