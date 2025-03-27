import tkinter as tk
from tkinter import messagebox
import os
import psutil
import subprocess
from datetime import datetime

# Конфигурация
BROWSERS = {
    "Google Chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "Microsoft Edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "Mozilla Firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe"
}
LOG_FILE = "C:\\sandbox_log.txt"

class SandboxApp:
    def __init__(self, root):
        self.root = root
        root.title("Browser Sandbox Tool")
        root.geometry("400x300")
        
        # Элементы GUI
        self.label = tk.Label(root, text="Выберите браузеры для изоляции:", font=('Arial', 12))
        self.label.pack(pady=10)
        
        self.checkboxes = {}
        for browser in BROWSERS:
            var = tk.IntVar()
            cb = tk.Checkbutton(root, text=browser, variable=var, font=('Arial', 10))
            cb.pack(anchor='w', padx=20)
            self.checkboxes[browser] = var
        
        self.start_btn = tk.Button(root, text="Запустить защиту", command=self.start_protection, height=2, width=20)
        self.start_btn.pack(pady=20)
        
        self.status = tk.Label(root, text="Статус: Ожидание", fg="gray")
        self.status.pack()

    def log(self, message):
        with open(LOG_FILE, "a") as f:
            f.write(f"[{datetime.now()}] {message}\n")

    def run_sandboxed(self, browser_path):
        try:
            subprocess.Popen([
                "powershell",
                "Start-Process",
                "-FilePath", f'"{browser_path}"',
                "-ArgumentList", "'--no-sandbox'",
                "-AppContainer",
                "-Verb", "RunAs"
            ], shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
            self.log(f"Успех: {browser_path} в песочнице")
            return True
        except Exception as e:
            self.log(f"Ошибка: {str(e)}")
            return False

    def monitor_browsers(self):
        for browser_name, var in self.checkboxes.items():
            if var.get() == 1:  # Если браузер выбран
                path = BROWSERS[browser_name]
                for proc in psutil.process_iter(['name', 'exe']):
                    try:
                        if proc.info['exe'] and os.path.normpath(proc.info['exe']) == os.path.normpath(path):
                            proc.kill()
                            self.run_sandboxed(path)
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
        self.root.after(1000, self.monitor_browsers)  # Проверка каждую секунду

    def start_protection(self):
        enabled_browsers = [b for b, var in self.checkboxes.items() if var.get() == 1]
        if not enabled_browsers:
            messagebox.showwarning("Ошибка", "Выберите хотя бы один браузер!")
            return
        
        self.status.config(text="Статус: Активен", fg="green")
        self.log("=== Запуск защиты ===")
        self.monitor_browsers()

if __name__ == "__main__":
    root = tk.Tk()
    app = SandboxApp(root)
    root.mainloop()