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


defualt_theme = "light"
def apply_light_theme():
    global theme

    if defualt_theme == "light":
        theme = {
            "background": "#ffffff",
            "navbar": "#cccccc",
            "button_bg": "#f0f0f0",
            "button_font": ("Arial", 12),
            "greeting_font": ("Arial", 16, "bold"),
            "form_bg": "#f9f9f9",
            "form_font": ("Arial", 12),
            "label_font": ("Arial", 12),
            "entry_width": 50,
        }
    else:
        theme = {
            
        }
        


def save_book(title_entry, genre_entry, author_entry, isbn_entry):
    # Retrieve values
    title = title_entry.get().strip()
    genre = genre_entry.get().strip()
    author = author_entry.get().strip()
    isbn = isbn_entry.get().strip()

    if title and genre and author:
        if not isbn:
            isbn = None
        print(f"Book Details:\nTitle: {title}\nGenre: {genre}\nAuthor: {author}\nISBN: {isbn}")
    else:
        print("All fields are required!")


def search_book(title_entry, genre_entry, author_entry, isbn_entry):
    # Retrieve values
    title = title_entry.get().strip()
    genre = genre_entry.get().strip()
    author = author_entry.get().strip()
    isbn = isbn_entry.get().strip()

    if title or genre or author or isbn:
        print(f"Book Details:\nTitle: {title}\nGenre: {genre}\nAuthor: {author}\nISBN: {isbn}")
    else:
        print("Input at least one field to search!")

# Main window setup
def main_window():
    global root
    apply_light_theme()
    root = tk.Tk()
    root.title("Zigla's LMS")
    root.geometry("800x400")
    root.configure(bg=theme["background"])
    
    # Navigation bar frame
    nav_frame = tk.Frame(root, bg=theme["navbar"], height=50)
    nav_frame.pack(side="top", fill="x")
    
    # Buttons in the navigation bar
    buttons = ["Add", "Search", "Borrow", "Return", "View"]
    for btn_text in buttons:
        btn = tk.Button(
            nav_frame, 
            text=btn_text, 
            bg=theme["button_bg"], 
            font=theme["button_font"], 
            relief="groove", 
            width=12, 
            command=lambda b=btn_text: navigate_to(b)
        )
        btn.pack(side="left", padx=5, pady=5)
    
    settings_btn = tk.Button(
        nav_frame, 
        text="Settings", 
        bg=theme["button_bg"], 
        font=theme["button_font"], 
        relief="groove", 
        width=12, 
        command=lambda: navigate_to("Settings")
    )
    settings_btn.pack(side="right", padx=5, pady=5)
    
    # Greeting message in the center
    greeting = f"{get_greeting()}, Welcome to Zigla's LMS"
    greeting_label = tk.Label(root, text=greeting, font=theme["greeting_font"], bg=theme["background"], fg="#333")
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
    
    # Navigation bar frame
    nav_frame = tk.Frame(root, bg="#cccccc", height=50)
    nav_frame.pack(side="top", fill="x")
    
    # Buttons in the navigation bar
    buttons = ["Add", "Search", "Borrow", "Return", "View"]
    for btn_text in buttons:
        btn = tk.Button(
            nav_frame, 
            text=btn_text, 
            bg=theme["button_bg"], 
            font=theme["button_font"], 
            relief="groove", 
            width=12, 
            command=lambda b=btn_text: navigate_to(b)
        )
        btn.pack(side="left", padx=5, pady=5)
    
    settings_btn = tk.Button(
        nav_frame, 
        text="Settings", 
        bg=theme["button_bg"], 
        font=theme["button_font"], 
        relief="groove", 
        width=12, 
        command=lambda: navigate_to("Settings")
    )
    settings_btn.pack(side="right", padx=5, pady=5)

    title_label = tk.Label(
        root, 
        text="Adding books to library...", 
        font=("Helvetica", 16, "bold"), 
        bg=theme["background"], 
        anchor="center"
    )
    title_label.pack(pady=20)

    # Form Frame
    form_frame = ttk.Labelframe(root, text="Fill form to add books", padding=20)
    form_frame.pack(pady=20, padx=20, expand=True, fill=tk.BOTH)
    # fix frame style later
    form_frame.configure(style="TLabelframe")
        
    # Individual entries
    title_entry = ttk.Entry(form_frame, width=theme["entry_width"])
    genre_entry = ttk.Entry(form_frame, width=theme["entry_width"])
    author_entry = ttk.Entry(form_frame, width=theme["entry_width"])
    isbn_entry = ttk.Entry(form_frame, width=theme["entry_width"])

    # Placement
    ttk.Label(form_frame, text="Title:", anchor="w", font=theme["label_font"], width=10).grid(row=0, column=0, pady=5, sticky="w")
    title_entry.grid(row=0, column=1, pady=5)

    ttk.Label(form_frame, text="Genre:", anchor="w",font=theme["label_font"], width=10).grid(row=1, column=0, pady=5, sticky="w")
    genre_entry.grid(row=1, column=1, pady=5)

    ttk.Label(form_frame, text="Author:", anchor="w",font=theme["label_font"], width=10).grid(row=2, column=0, pady=5, sticky="w")
    author_entry.grid(row=2, column=1, pady=5)

    ttk.Label(form_frame, text="ISBN:", anchor="w",font=theme["label_font"], width=10).grid(row=3, column=0, pady=5, sticky="w")
    isbn_entry.grid(row=3, column=1, pady=5)

    save_button = ttk.Button(
        form_frame, 
        text="Save", 
        command=lambda: save_book(title_entry, genre_entry, author_entry, isbn_entry)
    )
    save_button.grid(row=4, column=0, columnspan=2, pady=10)

    

def search_phase():
    print("Search phase activated")
    root.title("Zigla's LMS - Search Books")
    
    nav_frame = tk.Frame(root, bg="#cccccc", height=50)
    nav_frame.pack(side="top", fill="x")
    
    buttons = ["Add", "Search", "Borrow", "Return", "View"]
    for btn_text in buttons:
        btn = tk.Button(
            nav_frame, 
            text=btn_text, 
            bg=theme["button_bg"], 
            font=theme["button_font"], 
            relief="groove", 
            width=12, 
            command=lambda b=btn_text: navigate_to(b)
        )
        btn.pack(side="left", padx=5, pady=5)
    
    settings_btn = tk.Button(
        nav_frame, 
        text="Settings", 
        bg=theme["button_bg"], 
        font=theme["button_font"], 
        relief="groove", 
        width=12, 
        command=lambda: navigate_to("Settings")
    )
    settings_btn.pack(side="right", padx=5, pady=5)

    title_label = tk.Label(
        root, 
        text="Searching books from library...", 
        font=("Helvetica", 16, "bold"), 
        bg=theme["background"], 
        anchor="center"
    )
    title_label.pack(pady=20)

    form_frame = ttk.Labelframe(root, text="Input any detial to search", padding=20)
    form_frame.pack(pady=20, padx=20, expand=True, fill=tk.BOTH)
    # fix frame style later
    form_frame.configure(style="TLabelframe")
        
    title_entry = ttk.Entry(form_frame, width=theme["entry_width"])
    genre_entry = ttk.Entry(form_frame, width=theme["entry_width"])
    author_entry = ttk.Entry(form_frame, width=theme["entry_width"])
    isbn_entry = ttk.Entry(form_frame, width=theme["entry_width"])

    ttk.Label(form_frame, text="Title:", anchor="w", font=theme["label_font"], width=10).grid(row=0, column=0, pady=5, sticky="w")
    title_entry.grid(row=0, column=1, pady=5)

    ttk.Label(form_frame, text="Genre:", anchor="w",font=theme["label_font"], width=10).grid(row=1, column=0, pady=5, sticky="w")
    genre_entry.grid(row=1, column=1, pady=5)

    ttk.Label(form_frame, text="Author:", anchor="w",font=theme["label_font"], width=10).grid(row=2, column=0, pady=5, sticky="w")
    author_entry.grid(row=2, column=1, pady=5)

    ttk.Label(form_frame, text="ISBN:", anchor="w",font=theme["label_font"], width=10).grid(row=3, column=0, pady=5, sticky="w")
    isbn_entry.grid(row=3, column=1, pady=5)

    search_button = ttk.Button(
        form_frame, 
        text="Search", 
        command=lambda: search_book(title_entry, genre_entry, author_entry, isbn_entry)
    )
    search_button.grid(row=4, column=0, columnspan=2, pady=10)

    

def borrow_phase():
    print("Borrow phase activated")


def return_phase():
    print("Return phase activated")


def view_phase():
    print("View phase activated")



# Run the main window
if __name__ == "__main__":
    main_window()