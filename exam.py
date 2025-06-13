import psutil
import time
import win32gui
import win32con
import keyboard
from threading import Thread
import tkinter as tk

ALLOWED_APP = "Exam App"  
LOG_FILE = "exam_log.txt"

 
class FocusMonitor:
    def __init__(self):
        self.last_window = None

    def check_focus(self):
        while True:
            current_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if current_window != ALLOWED_APP and current_window:
                if current_window != self.last_window:
                    self.log_violation(f"SWITCHED_WINDOW: {current_window}")
                    self.last_window = current_window
                    
            time.sleep(1)

def kill_non_essential_apps():
    ESSENTIAL = ["explorer.exe", "System", "wininit.exe", "winlogon.exe", "csrss.exe", "services.exe", "lsass.exe", "smss.exe"]
    current_pid = psutil.Process().pid
    for proc in psutil.process_iter(['name', 'pid']):
        if proc.info['name'] not in ESSENTIAL and proc.info['pid'] != current_pid:
            try:
                proc.kill()
                log_violation(f"KILLED_PROCESS: {proc.info['name']}")
            except Exception as e:
                pass


import tkinter as tk

def show_notepad():
    root = tk.Tk()
    root.title("Exam Notepad")
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)
    root.overrideredirect(True)
    root.configure(bg='black')
    exit_btn = tk.Button(root, text="Exit", font=("Arial", 16), bg="red", fg="white", command=root.destroy)
    exit_btn.place(relx=0.98, rely=0.01, anchor='ne')
    text = tk.Text(root, font=("Consolas", 16), bg="white", fg="black", insertbackground="black", undo=True)
    text.pack(expand=True, fill='both', padx=20, pady=20)
    def block_close(event=None):
        return "break"
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    root.bind('<Alt-F4>', block_close)
    root.bind('<Escape>', block_close)
    root.mainloop()


class ProcessMonitor(Thread):
    def __init__(self):
        super().__init__()
        self.running = True
        self.whitelist = ["python.exe", "Exam App"]  

    def run(self):
        known_processes = set(p.info['name'] for p in psutil.process_iter(['name']))
        while self.running:
            current_processes = set(p.info['name'] for p in psutil.process_iter(['name']))
            new_processes = current_processes - known_processes
            for proc in new_processes:
                if proc not in self.whitelist:
                    log_violation(f"NEW_PROCESS: {proc}")
                   
            known_processes = current_processes
            time.sleep(2)


def block_shortcuts():
    keyboard.block_key('alt+tab')
    keyboard.block_key('ctrl+alt+delete')
    keyboard.block_key('win')
    keyboard.block_key('ctrl+shift+esc')
    keyboard.block_key('ctrl+v')
    keyboard.block_key('ctrl+c')


def log_violation(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time.ctime()}] {message}\n")


def show_fullscreen_message():
    root = tk.Tk()
    root.title("Exam Mode")
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)
    root.overrideredirect(True)  
    label = tk.Label(root, text="Hello user you are in", font=("Arial", 48), fg="white", bg="black")
    label.pack(expand=True, fill='both')
    root.configure(bg='black')
    
    def block_close(event=None):
        return "break"
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    root.bind('<Alt-F4>', block_close)
    root.bind('<Escape>', block_close)
    root.mainloop()

def show_code_ide():
    root = tk.Tk()
    root.title("Exam IDE")
    root.attributes('-fullscreen', True)
    root.attributes('-topmost', True)
    root.overrideredirect(True)
    root.configure(bg='black')
    label = tk.Label(root, text="Exam Coding Environment", font=("Arial", 32), fg="white", bg="black")
    label.pack(fill='x')
  
    code_editor = tk.Text(root, font=("Consolas", 16), bg="#1e1e1e", fg="#d4d4d4", insertbackground="white", undo=True)
    code_editor.pack(expand=True, fill='both', padx=20, pady=20)
    def block_close(event=None):
        return "break"
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    root.bind('<Alt-F4>', block_close)
    root.bind('<Escape>', block_close)
    root.mainloop()

if __name__ == "__main__":
    print("=== Exam Monitor Started ===")
    log_violation("=== SESSION STARTED ===")
    kill_non_essential_apps()
    show_notepad()
