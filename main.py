import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import sqlite3

# Function to determine greeting based on time
def get_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning"
    elif hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

def on_closing():
    response = messagebox.askyesno("Quit", "Do you want to quit?")
    if response:
        if conn:
            cursor.close()
            conn.close()
            print("Connection closed")
        root.destroy()


database = "ZigsLMS.db"
conn = sqlite3.connect(database)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                genre TEXT,
                author TEXT,
                isbn TEXT,
                is_borrowed BOOLEAN DEFAULT 0,
                borrower_id INTEGER
    
)''') 

cursor.execute('''CREATE TABLE IF NOT EXISTS borrower(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               borrower_id INTEGER,
               name TEXT,
               email TEXT,
               is_returned BOOLEAN,
               FOREIGN KEY (borrower_id) REFERENCES books (borrower_id)
               )''')



cursor.execute('''SELECT * FROM books''')

rows = cursor.fetchall()


for row in rows:
    print(row)



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
    if not isbn:
        isbn = None
    is_borrowed = False

    if title and genre and author: 
        # saving book into database
        cursor.execute('''INSERT INTO books(title, genre, author,   isbn, is_borrowed, borrower_id)
                        VALUES(?,?,?,?, ?, ?)''',
                    (title, genre, author, isbn, is_borrowed, None)
                    ) 
        conn.commit()

        messagebox.showinfo("Saved!", "Book successfully saved!")
        cursor.execute('''SELECT * FROM books''')
        rows = cursor.fetchall()
        for row in rows:
            print(row)

        print(f"Book Details:\nTitle: {title}\nGenre: {genre}\nAuthor: {author}\nISBN: {isbn}")
    else:
        print("All fields are required!")
        messagebox.askokcancel("Prompt", "Please input book details to be saved.")
    


def search_book(title_entry, genre_entry, author_entry, isbn_entry):
    title = title_entry.get().strip()
    genre = genre_entry.get().strip()
    author = author_entry.get().strip()
    isbn = isbn_entry.get().strip()

    if title or genre or author or isbn:
        print(f"Book Details:\nTitle: {title}\nGenre: {genre}\nAuthor: {author}\nISBN: {isbn}")
        if title and not genre and not author:
            cursor.execute('''SELECT * FROM books WHERE title = ?''', (title,))
        elif genre and not title and not author:
            cursor.execute('''SELECT * FROM books WHERE genre = ?''', (genre,))
        elif author and not genre and not title:
            cursor.execute('''SELECT * FROM books WHERE author = ?''', (author,))
        elif title and author and not genre:
            cursor.execute('''SELECT * FROM books WHERE title = ? AND author = ?''', (title, author))
        elif title and genre and not author:
            cursor.execute('''SELECT * FROM books WHERE title = ? AND genre = ?''', (title, genre))
        elif genre and author and not title:
            cursor.execute('''SELECT * FROM books WHERE genre = ? AND author = ?''', (genre, author))
        else:
            cursor.execute('''SELECT * FROM books WHERE title = ? AND genre = ? AND author = ?''', (title, genre, author))

        search = cursor.fetchall()
        if not search:
            messagebox.showinfo("Search", "No such book found")
            print("No such book found")
        else:
            open_search_result(search)

        for row in search:
            print(row)

            
    else:
        messagebox.showinfo("Search", "Input at least one field to search!")
        print("Input at least one field to search!")

def borrow_action(entries):
    data = {field: entry.get() for field, entry in entries.items()}
    #how data looks: {'name': 'zigla ', 'id': '38895', 'email': 'asjfalk', 'title': '', 'genre': '', 'author': '', 'isbn': ''}
    print(data)
    print("Borrow Request Submitted:")
    for field, value in data.items():
        print(f"{field.capitalize()}: {value}")
    
    # borrower = ["Name", "ID", "Email"]
    # details =  ["Title", "Genre", "Author", "ISBN"]
    # entries = {}
    if not data["name"] or not data["id"] or not data["email"]:
        messagebox.showinfo("Incorrect Details!", "Please input all borrower details to proceed")
        return

    if not data["title"] or not data["genre"] or not data["author"]:
        messagebox.showinfo("Incorrect Details!", "Please input all book details to borrow")

    else:

        print(f'title: {data["title"]} genre: {data["genre"]} author: {data["author"]}')
        #get the id of one of the books the user is trying to borrow if that book is not already borrwed
        cursor.execute('''
                        SELECT id FROM books WHERE "title" = ? AND  "genre" = ? AND "author" = ? AND "is_borrowed" = ?
                       ''', (data["title"], data["genre"], data["author"], False))
        result = cursor.fetchone()

        if result:
            print(result)
            messagebox.showinfo("Borrowed!", "Book has successfully been borrowed!")

            # if all details are provided and book has successfully been borrowed, add user to borrower table
            cursor.execute('''
                            INSERT INTO borrower("borrower_id", "name", "email") VALUES(?,?,?)
            ''',  (data["id"], data["name"], data["email"]))

            cursor.execute('''SELECT * FROM borrower''')

            results = cursor.fetchall()

            for rows in results:
                print(rows)
                
            # change the is_borrowed status to true and set the borrower id in the books where the book has been borrowed
            cursor.execute('''
                            UPDATE books SET is_borrowed = ?, borrower_id = ? WHERE id = ?
                           ''', (True, data["id"], result[0]))
            conn.commit()
            # DEBUG: CHECK IF THE IS_BORROWED ATTRIBUTE OF THE BOOK BORROWED HAS BEEN CHANGED TO TRUE
            cursor.execute('''
                            SELECT * FROM books WHERE "is_borrowed" = ?
                           ''', (True,))
            x = cursor.fetchall()
            for rows in x:
                print(rows)
            
            
        else:
            # check if the book wasnt found because it has already been borrowed or it isnt available
            cursor.execute('''
                        SELECT id FROM books WHERE "title" = ? AND  "genre" = ? AND "author" = ?
                       ''', (data["title"], data["genre"], data["author"]))
            book = cursor.fetchall()
            if book:
                messagebox.showinfo("Error!", "Book already borrowed!")
            else:
                messagebox.showinfo("Error!", "No such book found")

        

def return_action(entries):
    data = {field: entry.get() for field, entry in entries.items()}
    print("Return Request Submitted:")
    for field, value in data.items():
        print(f"{field.capitalize()}: {value}")

    # borrower = ["Name", "ID", "Email"]
    # details =  ["Title", "Genre", "Author", "ISBN"]
    # entries = {}
    if not data["name"] or not data["id"] or not data["email"]:
        messagebox.showinfo("Incorrect Details!", "Please input all returnee details to proceed")
        return
    else:

        cursor.execute('''
                        INSERT INTO borrower("borrower_id", "name", "email") VALUES(?,?,?)
        ''',  (data["id"], data["name"], data["email"]))

        cursor.execute('''SELECT * FROM borrower''')

        results = cursor.fetchall()

        for rows in results:
            print(rows)

    if not data["title"] or not data["genre"] or not data["author"]:
        messagebox.showinfo("Incorrect Details!", "Please input all book details to borrow")
    else:
        print(f'title: {data["title"]} genre: {data["genre"]} author: {data["author"]}')
        #get the id of one of the books the user is trying to borrow if that book is not already borrwed
        cursor.execute('''
                        SELECT id FROM books WHERE "title" = ? AND  "genre" = ? AND "author" = ? AND "is_borrowed" = ?
                       ''', (data["title"], data["genre"], data["author"], False))
        result = cursor.fetchone()
        if result:
            print(result)
            messagebox.showinfo("Borrowed!", "Book has successfully been borrowed!")
            # change the is_borrowed status to true and set the borrower id in the books where the book has been borrowed
            cursor.execute('''
                            UPDATE books SET is_borrowed = ?, borrower_id = ? WHERE id = ?
                           ''', (True, data["id"], result[0]))
            conn.commit()
            # DEBUG: CHECK IF THE IS_BORROWED ATTRIBUTE OF THE BOOK BORROWED HAS BEEN CHANGED TO TRUE
            cursor.execute('''
                            SELECT * FROM books WHERE "is_borrowed" = ?
                           ''', (True,))
            x = cursor.fetchall()
            for rows in x:
                print(rows)
            
            
        else:
            # check if the book wasnt found because it has already been borrowed or it isnt available
            cursor.execute('''
                        SELECT id FROM books WHERE "title" = ? AND  "genre" = ? AND "author" = ?
                       ''', (data["title"], data["genre"], data["author"]))
            book = cursor.fetchall()
            if book:
                messagebox.showinfo("Error!", "Book already borrowed!")
            else:
                messagebox.showinfo("Error!", "No such book found")

    


# Main window setup
def main_window():
    global root
    apply_light_theme()
    root = tk.Tk()
    root.title("Zigla's LMS")
    root.geometry("800x400")
    root.configure(bg=theme["background"])

    root.protocol("WM_DELETE_WINDOW", on_closing)

    
    # Navigation bar frame
    nav_frame = tk.Frame(root, bg=theme["navbar"], height=50)
    nav_frame.pack(side="top", fill="x")
    
    # Buttons in the navigation bar
    buttons = ["Add", "Search", "Borrow", "Return", "Home"]
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

# Function to handle navigation
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
    elif phase == "Home":
        home_phase()
    elif phase == "Settings":
        settings_phase()


def add_phase():
    root.title("Zigla's LMS - Add Books")
    
    # Navigation bar frame
    nav_frame = tk.Frame(root, bg="#cccccc", height=50)
    nav_frame.pack(side="top", fill="x")
    
    # Buttons in the navigation bar
    buttons = ["Add", "Search", "Borrow", "Return", "Home"]
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

    form_frame = ttk.Labelframe(root, text="Fill form to add books", padding=20)
    form_frame.pack(pady=20, padx=20, expand=True)
        
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
    
    buttons = ["Add", "Search", "Borrow", "Return", "Home"]
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
    form_frame.pack(pady=20, padx=20, expand=True)
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
    root.title("Zigla's LMS - Borrow Books")

    nav_frame = tk.Frame(root, bg="#cccccc", height=50)
    nav_frame.pack(side="top", fill="x")

    buttons = ["Add", "Search", "Borrow", "Return", "Home"]
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
        text="Borrowing book from library...", 
        font=("Helvetica", 16, "bold"), 
        bg=theme["background"], 
        anchor="center"
    )
    title_label.pack(pady=20)
    
    borrower = ["Name", "ID", "Email"]
    details =  ["Title", "Genre", "Author", "ISBN"]
    entries = {}

    
    borrower_frame = ttk.Labelframe(root, text="Input borrower details", padding=20)
    borrower_frame.pack(pady=20, padx=20, expand=True)

    for i, label in enumerate(borrower):
        tk.Label(borrower_frame, text=label, font=("Arial", 14), bg="white").grid(
            row=i, column=0,pady=5, sticky="e"
        )
        entry = ttk.Entry(borrower_frame, font=("Arial", 14))
        entry.grid(row=i, column=1, pady=5, sticky="ew")
        entries[label.lower()] = entry


    content_frame = ttk.Labelframe(root, text="Input book details", padding=20)
    content_frame.pack(pady=20, padx=20, expand=True)


    for i, label in enumerate(details):
        tk.Label(content_frame, text=label, font=("Arial", 14), bg="white").grid(
            row=i, column=0,pady=5, sticky="e"
        )
        entry = ttk.Entry(content_frame, font=("Arial", 14))
        entry.grid(row=i, column=1, pady=5, sticky="ew")
        entries[label.lower()] = entry

    borrow_button = ttk.Button(
        content_frame, text="Borrow", command=lambda: borrow_action(entries)
    )
    borrow_button.grid(row=7, column=0, columnspan=2, pady=20, sticky="n")



def return_phase():
    print("Return phase activated")
    root.title("Zigla's LMS - Return Books")

    nav_frame = tk.Frame(root, bg="#cccccc", height=50)
    nav_frame.pack(side="top", fill="x")

    buttons = ["Add", "Search", "Borrow", "Return", "Home"]
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
        text="Returning book to library...", 
        font=("Helvetica", 16, "bold"), 
        bg=theme["background"], 
        anchor="center"
    )
    title_label.pack(pady=20)
    
    returner = ["Name", "ID", "Email"]
    details =  ["Title", "Genre", "Author", "ISBN"]
    entries = {}

    
    returner_frame = ttk.Labelframe(root, text="Input returnee details", padding=20)
    returner_frame.pack(pady=20, padx=20, expand=True)

    for i, label in enumerate(returner):
        tk.Label(returner_frame, text=label, font=("Arial", 14), bg="white").grid(
            row=i, column=0,pady=5, sticky="e"
        )
        entry = ttk.Entry(returner_frame, font=("Arial", 14))
        entry.grid(row=i, column=1, pady=5, sticky="ew")
        entries[label.lower()] = entry


    content_frame = ttk.Labelframe(root, text="Input book details", padding=20)
    content_frame.pack(pady=20, padx=20, expand=True)

    for i, label in enumerate(details):
        tk.Label(content_frame, text=label, font=("Arial", 14), bg="white").grid(
            row=i, column=0,pady=5, sticky="e"
        )
        entry = ttk.Entry(content_frame, font=("Arial", 14))
        entry.grid(row=i, column=1, pady=5, sticky="ew")
        entries[label.lower()] = entry

    return_button = ttk.Button(
        content_frame, text="Borrow", command=lambda: return_action(entries)
    )
    return_button.grid(row=7, column=0, columnspan=2, pady=20, sticky="n")



def home_phase():
    print("Home phase activated")
    root.title("Zigla's LMS")
    
    nav_frame = tk.Frame(root, bg=theme["navbar"], height=50)
    nav_frame.pack(side="top", fill="x")
    
    buttons = ["Add", "Search", "Borrow", "Return", "Home"]
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
    
    greeting = f"{get_greeting()}, Welcome to Zigla's LMS"
    greeting_label = tk.Label(root, text=greeting, font=theme["greeting_font"], bg=theme["background"], fg="#333")
    greeting_label.pack(expand=True)


def settings_phase():
    print("Settings phase activated")
    root.title("Zigla's LMS - Settings")
    
    nav_frame = tk.Frame(root, bg="#cccccc", height=50)
    nav_frame.pack(side="top", fill="x")
    
    buttons = ["Add", "Search", "Borrow", "Return", "Home"]
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



def open_search_result(search):
    for widgets in root.winfo_children():
        widgets.destroy()
    print("Home phase activated")
    root.title("Zigla's LMS- Search Result")
    
    nav_frame = tk.Frame(root, bg=theme["navbar"], height=50)
    nav_frame.pack(side="top", fill="x")
    
    buttons = ["Add", "Search", "Borrow", "Return", "Home"]
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

    tree = ttk.Treeview(root, columns=("ID", "Title", "Genre", "Author", "ISBN", "Is_borrowed", "Borrower_id"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Title", text="Title")
    tree.heading("Genre", text="Genre")
    tree.heading("Author", text="Author")
    tree.heading("ISBN", text="ISBN")
    tree.heading("Is_borrowed", text="Is_borrowed")
    tree.heading("Borrower_id", text="Borrower_id")

    tree.pack(fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


    for rows in search:
        tree.insert("", tk.END, values=rows)



# Run the main window
if __name__ == "__main__":
    main_window()
