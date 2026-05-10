import os
import tkinter as tk
import webbrowser
from multiprocessing import Process
from app import pons_flask
from app import pons_tkinter

def launch_flask(root_window):
    """Start Flask in a separate process, hide launcher, and open browser."""
    flask_process = Process(target=pons_flask.run_flask, kwargs={"use_reloader": False})
    flask_process.start()
    root_window.withdraw()

    # Open the Flask search page in default web browser
    webbrowser.open("http://localhost:5000/search")

def launch_tkinter(root):
    """Destroy the launcher window and start the Tkinter app."""
    root.destroy()
    app = pons_tkinter.PonsTkApp(None)
    app.create_tkinter()

def center_window(window, width, height):
    """Centers a Tkinter window on the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def main():
    # --- Tkinter Launcher Window ---
    app = tk.Tk()
    app.title("PONS Dictionary Launcher")

    # Set desired size and center
    launcher_width = 400
    launcher_height = 200
    center_window(app, launcher_width, launcher_height)
    app.resizable(False, False)

    # Get icon
    icon_path = os.path.join(os.path.dirname(__file__), "app", "static", "icons", "dict.ico")
    icon_path = os.path.abspath(icon_path)
    icon_path = icon_path.replace("\\", "/")  # ensure forward slashes for Tcl
    try:
        app.iconbitmap(icon_path)
    except tk.TclError:
        print(f"Failed to load icon: {icon_path}")

    # Instruction label
    tk.Label(app, text="Select Application to Launch", font=("TkDefaultFont", 12)).pack(pady=20)

    # Buttons for Flask and Tkinter
    button_width = 30
    button_height = 2
    tk.Button(
        app,
        text="Launch Flask Web App",
        command=lambda: launch_flask(app),  # pass root to hide the launcher
        width=button_width,
        height=button_height
    ).pack(pady=10)

    tk.Button(
        app,
        text="Launch Tkinter App",
        command=lambda: launch_tkinter(app),
        width=button_width,
        height=button_height
    ).pack(pady=10)

    # Start the launcher
    app.mainloop()

if __name__ == "__main__":
    main()