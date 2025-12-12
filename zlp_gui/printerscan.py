# ---------------------------------------
# MARK: IMPORTS
# ---------------------------------------
import ipaddress
import socket
import sys
import psutil
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QSize, QThread
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QMovie

from zlp_lib.zlp import resource_path, test_print


# ---------------------------------------
# MARK: WORKER
# ---------------------------------------
class ScannerWorker(QObject):
    """Background worker that discovers Zebra printers on local subnets.

    Emits:
    - progress(str): human-readable status updates for the UI
    - finished(list[str]): list of discovered printer IPs
    """
    finished = pyqtSignal(list)
    progress = pyqtSignal(str)

    @pyqtSlot()
    def run(self):
        """Entry point for the worker thread.
        - Enumerates local IPv4 subnets
        - Scans each subnet for hosts listening on port 9100
        - Optionally identifies Zebra-compatible devices
        """
        printers = []
        subnets = []

        for iface, addrs in psutil.net_if_addrs().items():
            if getattr(self, "cancelled", False):
                break
            for addr in addrs:
                if getattr(self, "cancelled", False):
                    break
                if addr.family == socket.AF_INET:
                    ip = ipaddress.ip_address(addr.address)
                    netmask = ipaddress.ip_address(addr.netmask)
                    network = ipaddress.ip_network(f"{ip}/{netmask}", strict=False)
                    # Only scan reasonably small subnets
                    if network.prefixlen >= 23:
                        subnets.append(str(network))

        if "--dev" in sys.argv:
            # In dev mode scan a small range to keep things fast
            subnets = ["192.168.1.210/28"]

        for subnet in subnets:
            if getattr(self, "cancelled", False):
                break
            self.progress.emit(f"Scanning {subnet}...")
            printers.extend(self.scan_subnet(subnet))

        self.finished.emit(printers)

    def cancel(self):
        """Signal the worker to stop as soon as feasible."""
        self.cancelled = True

    def is_zebra_printer(self, ip, ZEBRA_PORT=9100, TIMEOUT=0.3):
        """Probe a host for a Zebra-compatible response on port 9100.

        Returns True when the returned banner suggests a Zebra/ZPL device.
        Note: This currently returns True on exceptions as a permissive fallback.
        """
        try:
            sock = socket.create_connection((str(ip), ZEBRA_PORT), timeout=TIMEOUT)
            sock.sendall(b"~HI\n")
            response = sock.recv(1024).decode(errors="ignore")
            sock.close()
            return "Zebra" in response or "ZPL" in response or "HONEYWELL" in response
        except:
            return True

    def scan_subnet(self, subnet, ZEBRA_PORT=9100, TIMEOUT=0.3):
        """Iterate hosts in a CIDR and collect reachable printer endpoints."""
        network = ipaddress.ip_network(subnet, strict=False)
        found = []

        for ip in network.hosts():
            self.progress.emit(f"Scanning {subnet}...\n  Checking {ip}...")
            if getattr(self, "cancelled", False):
                break
            try:
                sock = socket.create_connection((str(ip), ZEBRA_PORT), timeout=TIMEOUT)
                sock.close()

                if self.is_zebra_printer(ip):
                    found.append(str(ip))
            except:
                pass

        return found


# ---------------------------------------
# MARK: UI FLOW
# ---------------------------------------
class PrinterScanFlow(QObject):
    """UI controller that manages the scanning flow.

    Responsibilities:
    - Opens a small spinner window while scanning in a background thread
    - Streams status updates from the worker into the spinner window
    - Displays a separate results window on completion with Select/Test actions
    - Supports cancel via closing the spinner window
    """
    def __init__(self):
        super().__init__()
        self._spinner_window = None
        self._movie = None
        self._thread = None
        self._worker = None
        self._result_window = None

    def start_scan(self, parent):
        """Kick off scanning and present a spinner/status window."""
        parent.find_printers_btn.setEnabled(False)

        # Spinner window
        self._spinner_window = QWidget(None)
        self._spinner_window.setWindowTitle("Printer Scanner")
        self._spinner_window.resize(360, 160)
        self._spinner_window.setFixedSize(self._spinner_window.size())
        layout = QVBoxLayout()
        self._status_label = QLabel("Scanning network...")
        layout.addWidget(self._status_label)

        # Animated spinner GIF
        spinner_label = QLabel()
        spinner_label.setFixedSize(50, 50)
        self._movie = QMovie(resource_path("static/spinner.gif"))
        self._movie.setScaledSize(QSize(50, 50))
        spinner_label.setMovie(self._movie)
        layout.addWidget(spinner_label)
        self._spinner_window.setLayout(layout)
        self._spinner_window.show()
        self._movie.start()

        # Thread and worker (do the network work off the UI thread)
        self._thread = QThread()
        self._worker = ScannerWorker()
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.progress.connect(self._status_label.setText)
        self._worker.finished.connect(lambda printers: self._on_done(parent, printers))
        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)

        # Closing the spinner cancels the scan and cleans up the thread
        def _on_close(ev):
            try:
                self.cancel_scan(parent)
            finally:
                ev.accept()
        self._spinner_window.closeEvent = _on_close

        self._thread.start()

    def _on_done(self, parent, printers):
        """Handle completion: replace spinner with a results window."""
        # Close spinner and show results in a new window
        self._cleanup_spinner()
        parent.find_printers_btn.setEnabled(True)

        self._result_window = QWidget(None)
        self._result_window.setWindowTitle("Printer Scanner Results")
        self._result_window.resize(350, 150)
        self._result_window.setFixedSize(self._result_window.size())
        layout = QVBoxLayout()

        status = QLabel()
        layout.addWidget(status)

        if not printers:
            status.setText("No Zebra printers found.")
            close_btn = QPushButton("Close")
            close_btn.clicked.connect(self._result_window.close)
            layout.addWidget(close_btn)
        else:
            status.setText("Found printers:")
            for ip in printers:
                hl = QHBoxLayout()
                hl.addWidget(QLabel(str(ip)))

                test_btn = QPushButton("Test Print")
                # If test_print trues, show success message; else show failure message
                test_btn.clicked.connect(lambda _, ip=ip: 
                    QMessageBox.information(None, "Test Print", f"Test print sent to {ip} successfully.") 
                    if test_print(ip) 
                    else QMessageBox.warning(None, "Test Print", f"Failed to send test print to {ip}.")
                )
                select_btn = QPushButton("Select")
                select_btn.clicked.connect(lambda _, ip=ip: (parent.printer_ip_input.setText(ip), self._result_window.close()))

                hl.addWidget(test_btn)
                hl.addWidget(select_btn)
                layout.addLayout(hl)

            close_btn = QPushButton("Close")
            close_btn.clicked.connect(self._result_window.close)
            layout.addWidget(close_btn)

        self._result_window.setLayout(layout)
        self._result_window.show()

    def cancel_scan(self, parent):
        """User-initiated cancel: stop animation, request worker cancel, quit thread."""
        try:
            if self._movie:
                self._movie.stop()
            if self._spinner_window:
                self._spinner_window.close()
            parent.find_printers_btn.setEnabled(True)
        except Exception:
            pass

        if self._worker is not None:
            try:
                self._worker.cancel()
                self._status_label.setText("Scan cancelled.")
            except Exception:
                pass

        if self._thread is not None:
            try:
                self._thread.quit()
            except Exception:
                pass

    def _cleanup_spinner(self):
        """Internal helper to stop and close the spinner window safely."""
        try:
            if self._movie:
                self._movie.stop()
            if self._spinner_window:
                self._spinner_window.close()
        finally:
            self._movie = None
            self._spinner_window = None