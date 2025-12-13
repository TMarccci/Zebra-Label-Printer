import tkinter as tk
from tkinter import ttk, messagebox
import os
import shutil
import subprocess
from pathlib import Path

try:
    import win32com.client as win32
except Exception:
    win32 = None
try:
    import pythoncom
except Exception:
    pythoncom = None

from zlp_lib.zlp import APP_FOLDER, USER, resource_path

DESKTOP_SHORTCUT = Path.home() / "Desktop" / "Zebra Label Printer.lnk"
STARTUP_SHORTCUT = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup" / "Zebra Label Printer.lnk"

class ZebraLabelPrinterUninstaller:
    def __init__(self, root):
        self.root = root
        self.root.title("Zebra Label Printer Uninstaller")
        self.root.geometry("600x600")
        self.app_path = APP_FOLDER
        self.remove_files = tk.BooleanVar(value=True)
        self.remove_desktop = tk.BooleanVar(value=True)
        self.remove_startup = tk.BooleanVar(value=True)
        self.progress = None
        self.log_text = None
        self._running = False
        self._dot_ticks = 0
        self.progress_label = None
        self.build_ui()

    def build_ui(self):
        self.clear_window()
        ttk.Label(self.root, text="Uninstall Zebra Label Printer", font=("Arial", 16, "bold")).pack(pady=12)

        body = ttk.Frame(self.root)
        body.pack(fill="both", expand=True, padx=24, pady=8)
        ttk.Label(body, text=f"App folder: {self.app_path}").pack(anchor="w", pady=(0,10))
        ttk.Checkbutton(body, text="Remove application files", variable=self.remove_files).pack(anchor="w", pady=6)
        ttk.Checkbutton(body, text="Remove Desktop shortcut", variable=self.remove_desktop).pack(anchor="w", pady=6)
        ttk.Checkbutton(body, text="Remove Startup shortcut", variable=self.remove_startup).pack(anchor="w", pady=6)

        ttk.Separator(self.root, orient="horizontal").pack(fill="x", pady=8)
        self.log_text = tk.Text(self.root, height=10, wrap="word")
        self.log_text.pack(fill="both", expand=True, padx=12)

        self.progress_label = ttk.Label(self.root, text="Ready.")
        self.progress_label.pack(pady=(8,4))
        self.progress = ttk.Progressbar(self.root, length=520, mode="determinate", maximum=100)
        self.progress.pack(pady=(0,8))

        self.footer = ttk.Frame(self.root)
        self.footer.pack(side="bottom", fill="x", padx=12, pady=12)
        self.cancel_btn = ttk.Button(self.footer, text="Cancel", command=self.root.quit)
        self.cancel_btn.pack(side="left")
        self.uninstall_btn = ttk.Button(self.footer, text="Uninstall", command=self.confirm_and_uninstall)
        self.uninstall_btn.pack(side="right")

    def confirm_and_uninstall(self):
        if not messagebox.askyesno("Confirm", "This will remove app files and shortcuts. Continue?"):
            return
        self._running = True
        self.progress_label.config(text="Uninstalling")
        self.root.after(300, self._animate_dots)
        self.root.after(50, self._do_uninstall)

    def _animate_dots(self):
        if not self._running or self.progress_label is None:
            return
        self._dot_ticks = (self._dot_ticks + 1) % 4
        dots = "." * self._dot_ticks
        base = self.progress_label.cget("text").split(".")[0]
        self.progress_label.config(text=f"{base}{dots}")
        self.root.after(600, self._animate_dots)

    def _do_uninstall(self):
        steps = []
        if self.remove_desktop.get():
            steps.append(self._remove_desktop_shortcut)
        if self.remove_startup.get():
            steps.append(self._remove_startup_shortcut)
        if self.remove_files.get():
            steps.append(self._remove_app_files)

        total = len(steps)
        done = 0
        for step in steps:
            try:
                step()
            except Exception as e:
                self._log(f"Error: {e}")
            done += 1
            pct = int(done * 100 / max(1, total))
            self.progress.config(value=pct)
            self.root.update_idletasks()

        self._log("Uninstall complete.")
        self._running = False
        self.progress_label.config(text="Uninstaller completed")
        self.progress.config(value=100)
        # Switch footer buttons: disable Uninstall, show Close
        try:
            self.uninstall_btn.config(state="disabled")
        except Exception:
            pass
        # Replace Cancel with Close
        for child in list(self.footer.winfo_children()):
            child.destroy()
        ttk.Button(self.footer, text="Close", command=self.root.quit).pack(side="right")

    def _remove_desktop_shortcut(self):
        if DESKTOP_SHORTCUT.exists():
            try:
                DESKTOP_SHORTCUT.unlink()
                self._log("Removed Desktop shortcut.")
            except Exception:
                self._log("Failed to remove Desktop shortcut directly, trying COM...")
                self._delete_shortcut_com(str(DESKTOP_SHORTCUT))
        else:
            self._log("Desktop shortcut not found.")

    def _remove_startup_shortcut(self):
        if STARTUP_SHORTCUT.exists():
            try:
                STARTUP_SHORTCUT.unlink()
                self._log("Removed Startup shortcut.")
            except Exception:
                self._log("Failed to remove Startup shortcut directly, trying COM...")
                self._delete_shortcut_com(str(STARTUP_SHORTCUT))
        else:
            self._log("Startup shortcut not found.")

    def _delete_shortcut_com(self, path: str):
        # COM deletion fallback (rarely needed)
        if win32 is None:
            self._log("pywin32 not available; unable to delete via COM.")
            return
        if pythoncom is not None:
            pythoncom.CoInitialize()
        try:
            # No direct delete API; fall back to os.remove after resolving
            if os.path.exists(path):
                os.remove(path)
                self._log(f"Removed shortcut: {path}")
        finally:
            if pythoncom is not None:
                pythoncom.CoUninitialize()

    def _remove_app_files(self):
        # Attempt to stop running app before removal
        exe_path = Path(self.app_path) / "Zebra-Label-Printer.exe"
        updater_path = Path(self.app_path) / "zlp-updater.exe"
        server_path = Path(self.app_path) / "zlp-server.exe"
        # best-effort kill via taskkill (do NOT kill the running uninstaller)
        names_to_kill = ("Zebra-Label-Printer.exe", "zlp-updater.exe", "zlp-server.exe")
        try:
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            # CREATE_NO_WINDOW keeps Command Prompt windows from flashing
            creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
        except Exception:
            si = None
            creationflags = 0
        for name in names_to_kill:
            try:
                subprocess.run(["taskkill", "/IM", name, "/F"], capture_output=True, startupinfo=si, creationflags=creationflags)
            except Exception:
                pass

        if os.path.isdir(self.app_path):
            try:
                shutil.rmtree(self.app_path)
                self._log(f"Removed app folder: {self.app_path}")
            except Exception as e:
                self._log(f"Failed to remove app folder: {e}")
        else:
            self._log("App folder not found.")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def _log(self, message: str):
        if self.log_text is not None:
            self.log_text.insert("end", message + "\n")
            self.log_text.see("end")
            self.root.update_idletasks()


if __name__ == "__main__":
    root = tk.Tk()
    try:
        root.iconbitmap(resource_path("static/icon.ico"))
    except Exception:
        pass
    app = ZebraLabelPrinterUninstaller(root)
    root.mainloop()