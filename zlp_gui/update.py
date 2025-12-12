# ---------------------------------------
# MARK: IMPORTS
# ---------------------------------------
import requests
import subprocess
import sys

from PyQt5.QtWidgets import QMessageBox, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot, QSize
from PyQt5.QtGui import QMovie
from zlp_lib.zlp import CURRENT_PROGRAM_VERSION, APP_FOLDER, resource_path

# ---------------------------------------
# MARK: WORKER
# ---------------------------------------
class UpdateWorker(QObject):
    """Background worker that checks the latest release on GitHub.

    Emits a dict via `finished` with keys:
    - status: "ok" or "error"
    - latest: tag string when status is ok
    - error: message when status is error
    """
    finished = pyqtSignal(object)  # emits dict: {"status": "ok"|"error", "latest": str, "error": str}

    @pyqtSlot()
    def run(self):
        """Perform the HTTP request off the UI thread and emit the result."""
        try:
            response = requests.get("https://api.github.com/repos/TMarccci/Zebra-Label-Printer/releases/latest", timeout=30)
            if response.status_code == 200:
                latest = response.json().get("tag_name", "")
                self.finished.emit({"status": "ok", "latest": latest})
            else:
                self.finished.emit({"status": "error", "error": f"HTTP {response.status_code}"})
        except Exception as e:
            self.finished.emit({"status": "error", "error": str(e)})

# ---------------------------------------
# MARK: UI FLOW
# ---------------------------------------
class CheckforUpdate(QObject):
    """Controller for the update-check flow.

    Responsibilities:
    - Opens a small spinner window while checking in a background thread
    - On completion, shows a separate status window with actions
    - Cleans up thread/worker and handles user-initiated close
    """
    def __init__(self):
        super().__init__()
        self._spinner_window = None
        self._movie = None
        self._thread = None
        self._worker = None
        self._status_window = None

    # ---------------------------------------
    # MARK: START (THREADED) CHECK
    # ---------------------------------------
    def start_check(self, parent):
        """Kick off the update check and present a spinner/status window."""
        # Show spinner window as a new top-level window (not modal)
        self._spinner_window = QWidget(None)
        self._spinner_window.setWindowTitle("Checking for Updates")
        self._spinner_window.resize(280, 140)
        self._spinner_window.setFixedSize(self._spinner_window.size())
        layout = QVBoxLayout()
        self._status_label = QLabel("Checking latest version...")
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

        # Threaded worker (do network request off the UI thread)
        self._thread = QThread()
        self._worker = UpdateWorker()
        self._worker.moveToThread(self._thread)

        self._thread.started.connect(self._worker.run)
        self._worker.finished.connect(lambda result: self._on_done(parent, result))
        self._worker.finished.connect(self._thread.quit)
        self._worker.finished.connect(self._worker.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)

        # If user closes the spinner, stop animation and quit thread
        def _on_close(ev):
            try:
                self._cleanup_spinner()
                if self._thread is not None:
                    self._thread.quit()
            finally:
                ev.accept()
        self._spinner_window.closeEvent = _on_close

        self._thread.start()

    # ---------------------------------------
    # MARK: RESULT HANDLER
    # ---------------------------------------
    def _on_done(self, parent, result):
        """Handle completion: close spinner and open a status window with actions."""
        # Close spinner window and show results in a NEW window
        self._cleanup_spinner()

        # Keep a strong reference so the window doesn't get GC'd
        self._status_window = QWidget(None)
        self._status_window.setWindowTitle("Update Status")
        self._status_window.resize(360, 160)
        self._status_window.setFixedSize(self._status_window.size())
        layout = QVBoxLayout()

        status_label = QLabel()
        layout.addWidget(status_label)

        btn_row = QHBoxLayout()

        if result.get("status") != "ok":
            status_label.setText(f"Update check failed: {result.get('error')}")
            close_btn = QPushButton("Close")
            close_btn.clicked.connect(self._status_window.close)
            btn_row.addWidget(close_btn)
        else:
            latest = result.get("latest", "")
            if latest and latest != CURRENT_PROGRAM_VERSION:
                status_label.setText(
                    f"Update available: {latest}\nCurrent: {CURRENT_PROGRAM_VERSION}"
                )
                update_btn = QPushButton("Update Now")
                cancel_btn = QPushButton("Cancel")
                update_btn.clicked.connect(lambda: (self._status_window.close(), self.launch_updater(parent)))
                cancel_btn.clicked.connect(self._status_window.close)
                btn_row.addWidget(update_btn)
                btn_row.addWidget(cancel_btn)
            elif latest == CURRENT_PROGRAM_VERSION:
                status_label.setText(
                    f"You are up to date.\nCurrent: {CURRENT_PROGRAM_VERSION}"
                )
                close_btn = QPushButton("Close")
                close_btn.clicked.connect(self._status_window.close)
                btn_row.addWidget(close_btn)
            else:
                status_label.setText("You appear newer than latest release.")
                close_btn = QPushButton("Close")
                close_btn.clicked.connect(self._status_window.close)
                btn_row.addWidget(close_btn)

        layout.addLayout(btn_row)
        self._status_window.setLayout(layout)
        self._status_window.show()

    def _cleanup_spinner(self):
        """Stop the spinner animation and close its window safely."""
        try:
            if self._movie:
                self._movie.stop()
            if self._spinner_window:
                self._spinner_window.close()
        finally:
            self._movie = None
            self._spinner_window = None

    # ---------------------------------------
    # MARK: LAUNCH UPDATER
    # ---------------------------------------
    def launch_updater(self, parent):
        """Launch the external updater, then stop the server and quit the app.

        In dev mode, show an informational message and do nothing.
        """
        if "--dev" in sys.argv:
            QMessageBox.information(None, "Development Mode",
                "You are running in development mode. Update is disabled.",
            )
            return
        
        updater_path = APP_FOLDER + "\\zlp-updater.exe"
        print(f"Launching updater: {updater_path}")
        
        try:
            subprocess.Popen([updater_path])
            print("Updater launched.")
            
            # Stop server if running and exit GUI
            parent.kill_all_servers()
            # parent is a QWidget (likely main GUI); access QApplication via type
            from PyQt5.QtWidgets import QApplication
            QApplication.instance().quit()
        except Exception as e:
            QMessageBox.critical(None, "Updater Launch Failed", str(e))