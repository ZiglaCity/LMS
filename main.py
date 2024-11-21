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
    global root
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
    for widgets in root.winfo_children():
        widgets.destroy()
    print(f"Navigating to: {phase}")
    if phase == "Add":
        add_phase()
    elif phase == "Search":
        search_phase()
    elif phase == "Borrow":
        borrow_phase()
    elif phase == "Return":
        return_phase()
    elif phase == "View":
        view_phase()


def add_phase():
    root.title("Zigla's LMS - Add Books")
    
    # Styling
    button_style = {"font": ("Arial", 12), "bg": "#f0f0f0", "relief": "groove", "width": 12}
    
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

     # Title
    title_label = tk.Label(
        root,
        text="Adding books to library...",
        font=("Helvetica", 16, "bold"),
        anchor="center"
    )
    title_label.pack(pady=20)

    # Form Frame
    form_frame = ttk.Labelframe(root, text="Fill form to add books", padding=10)
    form_frame.pack(pady=20, padx=20, fill=tk.X)
        
    # Individual entries
    title_entry = ttk.Entry(form_frame, width=40)
    genre_entry = ttk.Entry(form_frame, width=40)
    author_entry = ttk.Entry(form_frame, width=40)
    isbn_entry = ttk.Entry(form_frame, width=40)

    # Placement
    ttk.Label(form_frame, text="Title:", anchor="w", width=10).grid(row=0, column=0, pady=5, sticky="w")
    title_entry.grid(row=0, column=1, pady=5)

    ttk.Label(form_frame, text="Genre:", anchor="w", width=10).grid(row=1, column=0, pady=5, sticky="w")
    genre_entry.grid(row=1, column=1, pady=5)

    ttk.Label(form_frame, text="Author:", anchor="w", width=10).grid(row=2, column=0, pady=5, sticky="w")
    author_entry.grid(row=2, column=1, pady=5)

    ttk.Label(form_frame, text="ISBN:", anchor="w", width=10).grid(row=3, column=0, pady=5, sticky="w")
    isbn_entry.grid(row=3, column=1, pady=5)

    # Save Button
    save_button = ttk.Button(form_frame, text="Save")
    save_button.grid(row=4, column=0, columnspan=2, pady=10)

    
def search_phase():
    print("Search phase activated")
    
def borrow_phase():
    print("Borrow phase activated")

def return_phase():
    print("Return phase activated")


def view_phase():
    print("View phase activated")

# Run the main window
if __name__ == "__main__":
    main_window()
