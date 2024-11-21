import tkinter as tk
from tkinter import ttk
from datetime import datetime

# Function to determine greeting based on time
def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning"
    elif hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

# Main window setup
def main_window():
    root = tk.Tk()
    root.title("Zigla's LMS")
    root.geometry("800x400")
    
    # Styling
    button_style = {"font": ("Arial", 12), "bg": "#f0f0f0", "relief": "groove", "width": 12}
    greeting_style = {"font": ("Arial", 16, "bold"), "fg": "#333"}
    
    # Navigation bar frame
    nav_frame = tk.Frame(root, bg="#cccccc", height=50)
    nav_frame.pack(side="top", fill="x")
    
    # Buttons in the navigation bar
    buttons = ["Add", "Search", "Borrow", "Return", "View"]
    for btn_text in buttons:
        btn = tk.Button(nav_frame, text=btn_text, **button_style, command=lambda b=btn_text: navigate_to(b))
        btn.pack(side="left", padx=5, pady=5)
    
    settings_btn = tk.Button(nav_frame, text="Settings", **button_style, command=lambda: navigate_to("Settings"))
    settings_btn.pack(side="right", padx=5, pady=5)
    
    # Greeting message in the center
    greeting = f"{get_greeting()}, welcome to Zigla's LMS"
    greeting_label = tk.Label(root, text=greeting, **greeting_style)
    greeting_label.pack(expand=True)
    
    root.mainloop()

# Function to handle navigation (Later add logic for different phases here)
def navigate_to(phase):
    print(f"Navigating to: {phase}")

# Run the main window
if __name__ == "__main__":
    main_window()
