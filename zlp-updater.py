import sys
import os
import shutil
import requests
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal
import tempfile

def resource_path(relative_path):
    try:
        base = sys._MEIPASS
    except:
        base = os.path.abspath(".")
    return os.path.join(base, relative_path)

class UpdateWorker(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

    def __init__(self, app_path):
        super().__init__()
        self.app_path = app_path

    def run(self):
        try:
            self.progress.emit("Fetching latest release...")

            # Get latest release from GitHub
            api_url = "https://api.github.com/repos/TMarccci/Zebra-Label-Printer/releases/latest"
            response = requests.get(api_url, timeout=10)
            response.raise_for_status()

            release_data = response.json()
            assets = release_data.get('assets', [])

            # Assets we care about
            wanted = {
                "Zebra-Label-Printer.exe": None,
                "zlp-server.exe": None,
            }
            for a in assets:
                name = a.get('name')
                if name in wanted:
                    wanted[name] = a.get('browser_download_url')
                    print(f"Asset URL set for {name}: {wanted[name]}")

            # Validate we found required assets
            missing = [k for k, v in wanted.items() if not v]
            if missing:
                raise RuntimeError(f"Missing assets in release: {', '.join(missing)}")

            temp_dir = tempfile.gettempdir()

            # Download each asset and replace
            for name, url in wanted.items():
                self.progress.emit(f"Downloading {name}...")
                
                r = requests.get(url, timeout=60)
                r.raise_for_status()
                
                temp_file = os.path.join(temp_dir, name)
                with open(temp_file, 'wb') as f:
                    f.write(r.content)

                target_file = os.path.join(self.app_path, name)
                print(f"Downloaded {name} to {target_file}")
                self.progress.emit(f"Backing up {name} if exists...")
                if os.path.exists(target_file):
                    shutil.copy2(target_file, target_file + ".bak")

                self.progress.emit(f"Replacing {name}...")
                shutil.copy2(temp_file, target_file)

                self.progress.emit(f"Cleaning up {name} temp file...")
                try:
                    os.remove(temp_file)
                except Exception:
                    pass

            # After successful replacement, remove all .bak files for the updated binaries
            for name in wanted.keys():
                bak_path = os.path.join(self.app_path, name + ".bak")
                if os.path.exists(bak_path):
                    try:
                        os.remove(bak_path)
                    except Exception:
                        pass

            self.finished.emit(True, "Update completed successfully!")
            
        except Exception as e:
            self.finished.emit(False, f"Error: {str(e)}")



class UpdateWindow(QWidget):
    def __init__(self, app_path):
        super().__init__()
        self.app_path = app_path
        self.init_ui()
        self.start_update()

    def init_ui(self):
        self.setWindowTitle("Zebra Label Printer - Update Tool")
        self.setGeometry(100, 100, 400, 150)
        
        layout = QVBoxLayout()
        
        self.label = QLabel("Starting update...")
        layout.addWidget(self.label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        layout.addWidget(self.progress_bar)
        
        self.setLayout(layout)

    def start_update(self):
        self.worker = UpdateWorker(self.app_path)
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def update_progress(self, message):
        self.label.setText(message)

    def on_finished(self, success, message):
        self.progress_bar.setRange(0, 1)
        self.progress_bar.setValue(1)
        self.label.setText(message)

        if success:
            # Clean original exe backups if created by previous versions
            target_dir = os.path.dirname(self.app_path)
            for name in ["Zebra-Label-Printer.exe", "zlp-server.exe"]:
                bak_path = os.path.join(target_dir, name + ".bak")
                if os.path.exists(bak_path):
                    try:
                        os.remove(bak_path)
                    except Exception:
                        pass
            
        QThread.sleep(2)
        self.close()
        if success:
            os.startfile(self.app_path + "\\Zebra-Label-Printer.exe")
        


def main():
    # Use fixed install folder
    USER = os.getenv("USERNAME")
    APP_FOLDER = f"C:\\Users\\{USER}\\Zebra Label Printer"

    if not os.path.exists(APP_FOLDER):
        print(f"Error: Folder not found: {APP_FOLDER}")
        sys.exit(1)

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("static/icon.ico")))
    window = UpdateWindow(APP_FOLDER)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()