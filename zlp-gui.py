import sys
import os
import subprocess
import psutil
import webbrowser
import requests
import shutil
import qrcode
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtNetwork import QLocalServer, QLocalSocket
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QMessageBox, QCheckBox, QSpinBox,
    QRadioButton, QMenuBar, QVBoxLayout, QGroupBox, QFormLayout,
)

from zlp_lib.zlp import resource_path, load_config, save_config, test_print, CURRENT_PROGRAM_VERSION, APP_FOLDER, USER
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
        self.resize(500, 640)
        self.setFixedSize(self.size())

        self.server_process = None
        self.config = load_config()
        self.help_window = None
        self.dirty = False

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
        # High-contrast, larger UI for readability
        self.setStyleSheet(
            """
            QWidget { font-size: 13px; }
            QLabel { font-size: 14px; }
            QGroupBox { font-size: 15px; font-weight: bold; margin-top: 12px; }
            QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 4px 6px; }
            QPushButton { font-size: 14px; padding: 8px 12px; }
            QLineEdit, QSpinBox { font-size: 14px; padding: 6px; }
            QRadioButton, QCheckBox { font-size: 14px; }
            """
        )
        
        # Add MenuBar
        menubar = QMenuBar(self)
        file_menu = menubar.addMenu("File")
        file_menu.addAction("Check for Updates", self.check_for_updates)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("Quick Guide", self.show_help)
        help_menu.addAction("About", lambda: QMessageBox.information(self, "About", f"Zebra Label Printer<br>Version {CURRENT_PROGRAM_VERSION}<br><br>Made with ❤️ by Marcell Tihanyi" +
            "<br><br><a href='https://tmarccci.hu'>tmarccci.hu</a>" +
            " | <a href='https://github.com/TMarccci'>GitHub</a>"),)
        layout.setMenuBar(menubar)

        # Status
        self.status_label = QLabel("✖️ Server Stopped")
        self.status_label.setStyleSheet("font-size: 16px")
        layout.addWidget(self.status_label)

        # Unsaved changes indicator
        self.unsaved_label = QLabel("")
        self.unsaved_label.setStyleSheet("color:#b33; font-weight:bold")
        layout.addWidget(self.unsaved_label)

        layout.addSpacing(8)

        # Server settings group
        server_box = QGroupBox("Server Settings")
        server_form = QFormLayout()
        self.server_port_input = QLineEdit(self.config["server_port"])
        self.server_port_input.setToolTip("Port number for the built-in web interface")
        server_form.addRow("Webserver Port:", self.server_port_input)

        ip_row = QHBoxLayout()
        self.printer_ip_input = QLineEdit(self.config["printer_ip"])
        self.printer_ip_input.setToolTip("Printer IP address (e.g. 192.168.1.100)")
        ip_row.addWidget(self.printer_ip_input)
        self.find_printers_btn = QPushButton("Find Printers")
        self.find_printers_btn.setToolTip("Scan the network for compatible printers")
        ip_row.addWidget(self.find_printers_btn)
        self.test_printer_btn = QPushButton("Test Printer")
        self.test_printer_btn.setToolTip("Try connecting to the printer on port 9100")
        ip_row.addWidget(self.test_printer_btn)
        server_form.addRow(QLabel("Printer IP:"), ip_row)

        self.printer_port_input = QLineEdit(self.config["printer_port"])
        self.printer_port_input.setToolTip("Usually 9100 for Zebra printers")
        server_form.addRow("Printer Port:", self.printer_port_input)

        self.autostart_checkbox = QCheckBox("Start server on launch")
        self.autostart_checkbox.setChecked(self.config.get("start_server_on_launch"))
        self.autostart_checkbox.setToolTip("Automatically start the web server when the app opens")
        server_form.addRow(self.autostart_checkbox)
        server_box.setLayout(server_form)
        layout.addWidget(server_box)
        
        layout.addSpacing(8)
        
        # Currency settings group
        currency_box = QGroupBox("Currency Settings")
        currency_layout = QVBoxLayout()
        currency_layout.addLayout(self._radio_row("Price Suggestion Type:", ["Hungary", "Poland", "Czech"], "price_suggestion_type"))
        currency_layout.addLayout(self._row("Visible Currency:", "currency"))

        hl = QHBoxLayout()
        self.decimals_checkbox = QCheckBox("Show decimals")
        self.decimals_checkbox.setChecked(self.config["show_decimals"])
        self.decimals_checkbox.setToolTip("Turn on to show decimal places in prices")
        hl.addWidget(self.decimals_checkbox)

        self.decimals_spin = QSpinBox()
        self.decimals_spin.setRange(0, 4)
        self.decimals_spin.setValue(self.config["decimal_places"])
        self.decimals_spin.setToolTip("How many decimals to show when enabled")
        hl.addWidget(self.decimals_spin)
        currency_layout.addLayout(hl)
        currency_box.setLayout(currency_layout)
        layout.addWidget(currency_box)
        
        layout.addSpacing(8)

        layout.addWidget(self.button("Save Settings", "save_btn"))
        
        layout.addSpacing(8)

        # Server control group
        actions_box = QGroupBox("Actions")
        actions_layout = QVBoxLayout()
        hl2 = QHBoxLayout()
        self.start_btn = QPushButton("Start Server")
        self.start_btn.setToolTip("Start the web server so phones/tablets can connect")
        self.stop_btn = QPushButton("Stop Server")
        self.stop_btn.setToolTip("Stop the web server")
        hl2.addWidget(self.start_btn)
        hl2.addWidget(self.stop_btn)
        actions_layout.addLayout(hl2)


        # Open web interface
        self.open_web_btn = QPushButton("Open Printer Page")
        self.open_web_btn.setToolTip("Open the local web page for printing")
        actions_layout.addWidget(self.open_web_btn)

        # QR Code and Link helpers
        self.qr_btn = QPushButton("QR Code")
        self.qr_btn.setToolTip("Show a QR code to open the page on the phone")
        actions_layout.addWidget(self.qr_btn)

        actions_box.setLayout(actions_layout)
        layout.addWidget(actions_box)

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
        self.qr_btn.clicked.connect(self.show_qr)
        self.find_printers_btn.clicked.connect(self.find_zebra_printers)
        # if test_print True, show success message; else show failure message
        self.test_printer_btn.clicked.connect(lambda:
            QMessageBox.information(None, "Test Print", f"Test print sent to {self.printer_ip_input.text().strip()} successfully.") 
            if test_print(self.printer_ip_input.text().strip()) 
            else QMessageBox.warning(None, "Test Print", f"Failed to send test print to {self.printer_ip_input.text().strip()}.")
        )

        # Mark dirty on any field change
        self.server_port_input.textChanged.connect(self.mark_dirty)
        self.printer_ip_input.textChanged.connect(self.mark_dirty)
        self.printer_port_input.textChanged.connect(self.mark_dirty)
        self.autostart_checkbox.toggled.connect(self.mark_dirty)
        self.decimals_checkbox.toggled.connect(self.mark_dirty)
        self.decimals_spin.valueChanged.connect(self.mark_dirty)
        for rb in getattr(self, 'price_suggestion_type_radios', []):
            rb.toggled.connect(self.mark_dirty)

    # ---------------------------------------
    # MARK: SERVER CONTROL
    # ---------------------------------------
    def kill_all_servers(self):
        cfg = load_config()
        try:
            print("Sending stop request to server...")
            requests.get(f"http://127.0.0.1:{cfg.get('server_port')}/stop", timeout=1)
        except requests.exceptions.ConnectionError:
            print("Server stopped.")
        except requests.exceptions.ReadTimeout:
            print("Server stopped (timeout).")
    
    def start_server(self):
        if not server_running():
            self.kill_all_servers()  # ensure clean start

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
        self.kill_all_servers()
        self.server_process = None
        self.update_status()

    # ---------------------------------------
    # MARK: FUNCTIONS
    # ---------------------------------------
    def update_status(self):
        if server_running():
            self.status_label.setText("✔️ Server Running")
        else:
            self.status_label.setText("✖️ Server Stopped")
    
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
        QMessageBox.information(self, "Saved", "Settings saved.\nRestarting server...")
        self.stop_server()
        self.start_server()
        self.clear_dirty()
        
    def open_web(self):
        print("Opening web interface...")
        port = self.server_port_input.text().strip()
        webbrowser.open(f"http://127.0.0.1:{port}")
        
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
        
    def check_for_updates(self):       
        if not hasattr(self, "update_checker") or self.update_checker is None:
            self.update_checker = CheckforUpdate()
        self.update_checker.start_check(self)
    
    def show_help(self):
        """Simple, readable guide for remote support and new users."""
        self.help_window = QWidget(None)
        self.help_window.setWindowTitle("Quick Guide")
        self.help_window.resize(520, 480)
        self.help_window.setFixedSize(self.help_window.size())
        v = QVBoxLayout()
        steps = [
            "1. Enter the Printer IP (or click Find Printers).",
            "2. Click Test Printer to check the connection.",
            "3. Save Configuration.",
            "4. Click Start Server.",
            "5. Open the web interface with the Open Web button.",
        ]
        for s in steps:
            lbl = QLabel(s)
            lbl.setWordWrap(True)
            v.addWidget(lbl)
        v.addSpacing(8)
        v.addWidget(QLabel("Tips:"))
        tips = [
            "- If something doesn't work, restart the application.",
            "- Save Settings to keep your changes for next time."
        ]
        for t in tips:
            tl = QLabel(t)
            tl.setWordWrap(True)
            v.addWidget(tl)
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.help_window.close)
        v.addSpacing(12)
        v.addWidget(close_btn)
        self.help_window.setLayout(v)
        self.help_window.show()

    def mark_dirty(self):
        self.dirty = True
        self.unsaved_label.setText("Unsaved changes")
        self.save_btn.setStyleSheet("background-color:#ffd966")

    def clear_dirty(self):
        self.dirty = False
        self.unsaved_label.setText("")
        self.save_btn.setStyleSheet("")
        
    def closeEvent(self, ev):
        self.kill_all_servers()
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
        
    # Check if updater got an update ready, it as when updater_temp exists
    updater_temp_dir = os.path.join(APP_FOLDER, "updater_temp")
    if os.path.exists(updater_temp_dir):
        try:
            for name in os.listdir(updater_temp_dir):
                src = os.path.join(updater_temp_dir, name)
                dst = os.path.join(APP_FOLDER, name)
                shutil.copy2(src, dst)
            shutil.rmtree(updater_temp_dir)
            print("Applied pending update from updater_temp.")
        except Exception as e:
            print(f"Failed to apply pending update: {str(e)}")

    gui = ControlGUI()
    gui.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    run_gui()
