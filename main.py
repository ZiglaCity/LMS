import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import sqlite3


# Function to determine greeting based on time
def get_greeting():
    # check if the admin has a name to be greeted with
    cursor.execute('''
            SELECT * FROM admin
            ''') 
    admin = cursor.fetchall()

    if admin:
        name = admin[0][1]
    else:
        name = ""

    hour = datetime.now().hour
    if hour < 12:
        return f"Good morning {name.capitalize()}"
    elif hour < 18:
        return f"Good afternoon {name.capitalize()}"
    else:
        return f"Good evening {name.capitalize()}"

def on_closing():
    response = messagebox.askyesno("Quit", "Do you want to quit?")
    if response:
        if conn:
            cursor.close()
            conn.close()
        root.destroy()


database = "ZigsLMS.db"
conn = sqlite3.connect(database)
cursor = conn.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    genre TEXT,
                    author TEXT,
                    isbn TEXT,
                    is_borrowed BOOLEAN DEFAULT 0,
                    borrower_id INTEGER  )
            ''') 

cursor.execute('''CREATE TABLE IF NOT EXISTS borrower(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               borrower_id INTEGER,
               name TEXT,
               email TEXT,
               is_returned BOOLEAN,
               book_id INTEGER,
               FOREIGN KEY (book_id) REFERENCES books (id),
               FOREIGN KEY (borrower_id) REFERENCES books (borrower_id)
               )''')


cursor.execute('''
               CREATE TABLE IF NOT EXISTS admin(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT,
               passcode TEXT )
            ''')

conn.commit()


def global_style():
    style = ttk.Style()

    style.configure(
        "Modern.TLabelframe",
        font=("Helvetica", 14, "bold"), 
        background="#f9f9f9",
        foreground="#333000", 
        relief="ridge",
        padding=10 
    )
    style.configure(
        "Modern.TLabelframe.Label",
        background="#f9f9f9",
        foreground="#598347",
        font=("Helvetica", 16, "bold")
    )

    style.configure(
        "TEntry",
        font=("Helvetica", 12),  
        padding=5
    )

    style.configure(
        "TButton",
        font=("Helvetica", 12, "bold"),
        background="#4CAF50",
        foreground="#598347",
        padding=10
    )
    style.map(
        "TButton",
        background=[("active", "#45a049")],
        relief=[("pressed", "sunken"), ("!pressed", "raised")]
    )



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
        

# define a nav bar to be used in all phases to reduce redundancy
def create_nav_bar(root, navigate_to, theme):
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

    return nav_frame


def save_book(title_entry, genre_entry, author_entry, isbn_entry):
    # Retrieve values and capitalize each word for easy search
    title = title_entry.get().strip().title()
    genre = genre_entry.get().strip().title()
    author = author_entry.get().strip().title()
    isbn = isbn_entry.get().strip().title()
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

    else:
        messagebox.askokcancel("Prompt", "Please input book details to be saved.")
    


def search_book(title_entry, genre_entry, author_entry, isbn_entry):
    title = title_entry.get().strip().title()
    genre = genre_entry.get().strip().title()
    author = author_entry.get().strip().title()
    isbn = isbn_entry.get().strip().title()

    if title or genre or author or isbn:
        # print(f"Book Details:\nTitle: {title}\nGenre: {genre}\nAuthor: {author}\nISBN: {isbn}")
        if title and not genre and not author:
            cursor.execute('''SELECT * FROM books WHERE title LIKE ? ''', (f"%{title}%",))
        elif genre and not title and not author:
            cursor.execute('''SELECT * FROM books WHERE genre LIKE ?''', (f"%{genre}%",))
        elif author and not genre and not title:
            cursor.execute('''SELECT * FROM books WHERE author LIKE ?''', (f"%{author}%",))
        elif title and author and not genre:
            cursor.execute('''SELECT * FROM books WHERE title LIKE ? AND author LIKE ?''', (f"%{title}%", f"%{author}%"))
        elif title and genre and not author:
            cursor.execute('''SELECT * FROM books WHERE title LIKE ? AND genre LIKE ?''', (f"%{title}%", f"%{genre}%"))
        elif genre and author and not title:
            cursor.execute('''SELECT * FROM books WHERE genre LIKE ? AND author LIKE ?''', (f"%{genre}%", f"%{author}%"))
        else:
            cursor.execute('''SELECT * FROM books WHERE title LIKE ? AND genre LIKE ? AND author LIKE ?''', (f"%{title}%", f"%{genre}%", f"%{author}%"))

        search = cursor.fetchall()

        if not search:
            messagebox.showinfo("Search", "No such book found")

        else:
            open_search_result(search)

    else:
        messagebox.showinfo("Search", "Input at least one field to search!")


def borrow_action(entries):
    data = {field: entry.get().strip().title() for field, entry in entries.items()}
    
    # borrower = ["Name", "ID", "Email"]
    # details =  ["Title", "Genre", "Author", "ISBN"]
    # entries = {}

    if not data["name"] or not data["id"] or not data["email"]:
        messagebox.showinfo("Incorrect Details!", "Please input all borrower details to proceed")
        return

    if not data["title"] or not data["genre"] or not data["author"]:
        messagebox.showinfo("Incorrect Details!", "Please input all book details to borrow")

    else:

        #get the id of one of the books the user is trying to borrow if that book is not already borrwed
        cursor.execute('''
                        SELECT id FROM books WHERE "title" = ? AND  "genre" = ? AND "author" = ? AND "is_borrowed" = ?
                       ''', (data["title"], data["genre"], data["author"], False))
        book_id = cursor.fetchone()
        

        if book_id:
            messagebox.showinfo("Borrowed!", "Book has successfully been borrowed!")

            # if all details are provided and book has successfully been borrowed, add user to borrower table
            cursor.execute('''
                            INSERT INTO borrower("borrower_id", "name", "email",is_returned, book_id) VALUES(?,?,?,?,?)
            ''',  (data["id"], data["name"], data["email"], False, book_id[0]))

            conn.commit()

            cursor.execute('''SELECT * FROM borrower''')

            results = cursor.fetchall()

            # change the is_borrowed status to true and set the borrower id in the books where the book has been borrowed
            cursor.execute('''
                            UPDATE books SET is_borrowed = ?, borrower_id = ? WHERE id = ?
                           ''', (True, data["id"], book_id[0]))
            conn.commit()

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
    conn.commit()
  

def return_action(entries):
    data = {field: entry.get().strip().title() for field, entry in entries.items()}

    # borrower = ["Name", "ID", "Email"]
    # details =  ["Title", "Genre", "Author", "ISBN"]
    # entries = {}

    if not data["name"] or not data["id"] or not data["email"]:
        messagebox.showinfo("Incorrect Details!", "Please input all returnee details to proceed")
        return

    if not data["title"] or not data["genre"] or not data["author"]:
        messagebox.showinfo("Incorrect Details!", "Please input all book details to be returned")

    else:
        #get the id of the book the user is trying to return by using returnees details from book borrowed if that book is not returned
        cursor.execute('''
                        SELECT id FROM books WHERE "title" = ? AND  "genre" = ? AND "author" = ? AND "is_borrowed" = ? AND borrower_id = ?
                       ''', (data["title"], data["genre"], data["author"], True, data["id"]))
        book_id = cursor.fetchone()
        print(book_id)

        if book_id:
            # check if the details of the returnee is not in the borrower table
            cursor.execute('''
                            SELECT * FROM borrower WHERE "borrower_id" = ? AND  "name" = ? AND "email" = ?
            ''',  ( data["id"], data["name"], data["email"]))

            x = cursor.fetchone()
            print(x)
            if not x:
                messagebox.showinfo("Incorrect Details!", "User never borrowed!")
                return
            
            # exit if the book has already been returned 
            cursor.execute('''
                            SELECT * FROM borrower WHERE "borrower_id" = ? AND  "name" = ? AND "email" = ? AND "is_returned" = ?
                            ''',  ( data["id"], data["name"], data["email"], False))
            
            x = cursor.fetchone()
            print(x)

            if not x:
                messagebox.showinfo("Returned!", "User already returned book!")
                return
            
            # if all details are provided and book has successfully been returned, remove user from borrower table or set is_returned to true, to still keep track of all borrowers
            cursor.execute('''
                            UPDATE borrower SET is_returned = ? WHERE "borrower_id" = ? AND  "name" = ? AND "email" = ? AND book_id = ?
            ''',  (True, data["id"], data["name"], data["email"], book_id[0]))
            conn.commit()

            cursor.execute('''SELECT * FROM borrower''')

            results = cursor.fetchall()
 
            # change the is_borrowed status to true and set the borrower id in the books where the book has been borrowed
            cursor.execute('''
                            UPDATE books SET is_borrowed = ?, borrower_id = ? WHERE id = ?
                           ''', (False, None, book_id[0]))
            conn.commit()

            messagebox.showinfo("Returned!", "Book has successfully been returned!")

            
        else:
            # check if the details of the returnee is not in the borrower table
            cursor.execute('''
                            SELECT * FROM borrower WHERE "borrower_id" = ? AND  "name" = ? AND "email" = ?
            ''',  ( data["id"], data["name"], data["email"]))

            x = cursor.fetchall()
            if not x:
                messagebox.showinfo("Incorrect Details!", "User never borrowed!")
                return

            # check if the book wasnt found because it has already been returned or it isnt available
            cursor.execute('''
                        SELECT id FROM books WHERE "title" = ? AND  "genre" = ? AND "author" = ?
                       ''', (data["title"], data["genre"], data["author"]))
            book = cursor.fetchall()
            if book:
                messagebox.showinfo("Error!", "Book already returned!")
                return
            else:
                messagebox.showinfo("Error!", "No such book found")
                return


# Main window setup
def main_window():
    global root
    apply_light_theme()
    root = tk.Tk()
    root.title("Zigla's LMS")
    root.geometry("800x400")
    root.state("zoomed")
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
    # print(f"Navigating to: {phase}")
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
    
    create_nav_bar(root, navigate_to, theme)

    title_label = tk.Label(
        root, 
        text="Adding books to library...", 
        font=("Helvetica", 16, "bold"), 
        bg=theme["background"], 
        anchor="center"
    )
    title_label.pack(pady=20)

    # Center frame with a modern style
    form_frame = ttk.LabelFrame(
        root, 
        text="📚 Fill form to add books", 
        padding=20, 
        style="Modern.TLabelframe"
    )
    form_frame.pack(pady=20, padx=20, expand=True)

    title_entry = ttk.Entry(form_frame, width=theme["entry_width"])
    genre_entry = ttk.Entry(form_frame, width=theme["entry_width"])
    author_entry = ttk.Entry(form_frame, width=theme["entry_width"])
    isbn_entry = ttk.Entry(form_frame, width=theme["entry_width"])

    ttk.Label(form_frame, text="Title📖", anchor="w", font=theme["label_font"], width=10).grid(row=0, column=0, pady=10, sticky="w")
    title_entry.grid(row=0, column=1, pady=5)

    ttk.Label(form_frame, text="Genre🗂️", anchor="w", font=theme["label_font"], width=10).grid(row=1, column=0, pady=10, sticky="w")
    genre_entry.grid(row=1, column=1, pady=5)

    ttk.Label(form_frame, text="Author✍️", anchor="w", font=theme["label_font"], width=10).grid(row=2, column=0, pady=10, sticky="w")
    author_entry.grid(row=2, column=1, pady=5)

    ttk.Label(form_frame, text="ISBN📇", anchor="w", font=theme["label_font"], width=10).grid(row=3, column=0, pady=10, sticky="w")
    isbn_entry.grid(row=3, column=1, pady=5)

    save_button = ttk.Button(
        form_frame, 
        text="💾 Save Book", 
        style="Form.TButton",
        command=lambda: save_book(title_entry, genre_entry, author_entry, isbn_entry)
    )
    save_button.grid(row=4, column=0, columnspan=2, pady=20)

    global_style()
    
def search_phase():
    root.title("Zigla's LMS - Search Books")
    
    create_nav_bar(root, navigate_to, theme)

    title_label = tk.Label(
        root, 
        text="Searching books from library...", 
        font=("Helvetica", 16, "bold"), 
        bg=theme["background"], 
        anchor="center"
    )
    title_label.pack(pady=20)

    form_frame = ttk.LabelFrame(
        root, 
        text="🔍Input any detail to search", 
        padding=20, 
        style="Modern.TLabelframe"
    )
    form_frame.pack(pady=20, padx=20, expand=True)


    title_entry = ttk.Entry(form_frame, width=theme["entry_width"])
    genre_entry = ttk.Entry(form_frame, width=theme["entry_width"])
    author_entry = ttk.Entry(form_frame, width=theme["entry_width"])
    isbn_entry = ttk.Entry(form_frame, width=theme["entry_width"])

    ttk.Label(form_frame, text="Title📖", anchor="w", font=theme["label_font"], width=10).grid(row=0, column=0, pady=5, sticky="w")
    title_entry.grid(row=0, column=1, pady=5)

    ttk.Label(form_frame, text="Genre🗂️", anchor="w", font=theme["label_font"], width=10).grid(row=1, column=0, pady=5, sticky="w")
    genre_entry.grid(row=1, column=1, pady=5)

    ttk.Label(form_frame, text="Author✍️", anchor="w", font=theme["label_font"], width=10).grid(row=2, column=0, pady=5, sticky="w")
    author_entry.grid(row=2, column=1, pady=5)

    ttk.Label(form_frame, text="ISBN📇", anchor="w", font=theme["label_font"], width=10).grid(row=3, column=0, pady=5, sticky="w")
    isbn_entry.grid(row=3, column=1, pady=5)

    search_button = ttk.Button(
        form_frame,
        text="🔍Search",
        command=lambda: search_book(title_entry, genre_entry, author_entry, isbn_entry)
    )
    search_button.grid(row=4, column=0, columnspan=2, pady=10)

    view_all_button = ttk.Button(
        form_frame,
        text="📚View All",
        command=lambda: view_all(cursor, open_search_result)
    )
    view_all_button.grid(row=5, column=0, columnspan=2, pady=5)

    def view_all(cursor, open_search_result):
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        open_search_result(books)
    
    global_style()


def borrow_phase():
    root.title("Zigla's LMS - Borrow Books")

    create_nav_bar(root, navigate_to, theme)

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

    borrower_with_emojis = {
        "Name": "Name 🧑",
        "ID": "ID 🆔",
        "Email": "Email 📧",
    }

    details_with_emojis = {
        "Title": "Title 📖",
        "Genre": "Genre 🎭",
        "Author": "Author ✍️",
        "ISBN": "ISBN 🔢",
    }

    borrower_frame = ttk.Labelframe(root, text="Input borrower details", padding=20, style="Modern.TLabelframe")
    borrower_frame.pack(pady=0, padx=20, expand=True)

    for i, label in enumerate(borrower):
        tk.Label(borrower_frame, text=borrower_with_emojis[label],  anchor="w", font=theme["label_font"], width=10).grid(
            row=i, column=0,pady=5, sticky="e"
        )
        entry = ttk.Entry(borrower_frame, width=theme["entry_width"])
        entry.grid(row=i, column=1, pady=5)
        entries[label.lower()] = entry


    content_frame = ttk.Labelframe(root, text="Input book details", padding=20, style="Modern.TLabelframe")
    content_frame.pack(pady=0, padx=20, expand=True)


    for i, label in enumerate(details): 
        tk.Label(content_frame, text=details_with_emojis[label], anchor="w", font=theme["label_font"], width=10).grid(
            row=i, column=0,pady=5, sticky="e"
        )
        entry = ttk.Entry(content_frame, width=theme["entry_width"])
        entry.grid(row=i, column=1, pady=5)
        entries[label.lower()] = entry

    borrow_button = ttk.Button(
        content_frame, text="📜 Borrow", command=lambda: borrow_action(entries)
    )
    borrow_button.grid(row=7, column=0, columnspan=2, pady=5, sticky="n")

    viewAllBorrowers_button = ttk.Button(
        content_frame, text="📚 View Borrowers", command=lambda: viewAllBorrowers()
    )
    viewAllBorrowers_button.grid(row=8, column=0, columnspan=2, pady=5, sticky="n")


    def viewAllBorrowers():
        cursor.execute('''
                       SELECT * FROM borrower
                        ''')
        borrowers = cursor.fetchall()

        open_borrower_result(borrowers)

    global_style()


def return_phase():
    root.title("Zigla's LMS - Return Books")

    create_nav_bar(root, navigate_to, theme)

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

    returner_with_emojis = {
        "Name": "Name 🧑",
        "ID": "ID 🆔",
        "Email": "Email 📧",
    }

    details_with_emojis = {
        "Title": "Title 📖",
        "Genre": "Genre 🎭",
        "Author": "Author ✍️",
        "ISBN": "ISBN 🔢",
    }

    
    returner_frame = ttk.Labelframe(root, text="Input returnee details",  padding=20, style="Modern.TLabelframe")
    returner_frame.pack(pady=20, padx=20, expand=True)

    for i, label in enumerate(returner):
        tk.Label(returner_frame, text=returner_with_emojis[label], anchor="w", font=theme["label_font"], width=10).grid(
            row=i, column=0,pady=5, sticky="e"
        )
        entry = ttk.Entry(returner_frame,  width=theme["entry_width"])
        entry.grid(row=i, column=1, pady=5)
        entries[label.lower()] = entry


    content_frame = ttk.Labelframe(root, text="Input book details",  padding=20, style="Modern.TLabelframe")
    content_frame.pack(pady=20, padx=20, expand=True)

    for i, label in enumerate(details):
        tk.Label(content_frame, text=details_with_emojis[label],anchor="w", font=theme["label_font"], width=10).grid(
            row=i, column=0,pady=5, sticky="e"
        )
        entry = ttk.Entry(content_frame, width=theme["entry_width"])
        entry.grid(row=i, column=1, pady=5)
        entries[label.lower()] = entry

    return_button = ttk.Button(
        content_frame, text="📜 Return", command=lambda: return_action(entries)
    )
    return_button.grid(row=7, column=0, columnspan=2, pady=20, sticky="n")

    global_style()


def home_phase():
    root.title("Zigla's LMS")
    
    create_nav_bar(root, navigate_to, theme)

    greeting = f"{get_greeting()}, Welcome to Zigla's LMS"
    greeting_label = tk.Label(root, text=greeting, font=theme["greeting_font"], bg=theme["background"], fg="#333")
    greeting_label.pack(expand=True)


def settings_phase():
    root.title("Zigla's LMS - Settings")
    
    create_nav_bar(root, navigate_to, theme)

    cursor.execute('''
            SELECT * FROM admin
            ''') 
    admin = cursor.fetchall()

    if admin:
        name = admin[0][1]
    else:
        name = ""

    passcode = tk.StringVar()
    admin_name = tk.StringVar()
    admin_name.set(name)

    
    settings_frame = ttk.Labelframe(root, text="Change Account Settings...", padding=20, style="Modern.TLabelframe")
    settings_frame.pack(pady=20, padx=20, expand=True)

    name_label = ttk.Label(settings_frame, text="AdminName🧑", anchor="w", font=theme["label_font"], width=12)
    name_label.grid(row=1, column=1, sticky="e")

    name_entry = ttk.Entry(settings_frame, textvariable=admin_name, width=theme["entry_width"])
    name_entry.grid(row=1, column=2, pady=10)

    passcode_label = ttk.Label(settings_frame, text="Passcode🕵️‍♂️" , anchor="w", font=theme["label_font"], width=12)
    passcode_label.grid(row=2, column=1, pady=10, sticky="e")

    code_entry = ttk.Entry(settings_frame, textvariable=passcode, width=theme["entry_width"])
    code_entry.grid(row=2, column=2)

    save_admin = ttk.Button(settings_frame, text="💾 Save", style="Form.TButton", command=lambda: saveAdmin())
    save_admin.grid(row=3, column=2)

    global_style()


    def saveAdmin():
        cursor.execute('''
                SELECT * FROM admin
                ''') 
        admin = cursor.fetchall()

        if admin:
            cursor.execute('''
                            UPDATE admin SET "name" = ?,  "passcode" = ? WHERE id = ?
                            ''', ( name_entry.get(), code_entry.get(), 1))
        
        else:
            cursor.execute('''
                            INSERT INTO admin (id, name, passcode) VALUES(?,?,?)
                            ''', (1, name_entry.get(), code_entry.get()))
            
        conn.commit()

        cursor.execute('''
                       SELECT * FROM admin
                        ''') 
           
        admin = cursor.fetchall()


def open_search_result(search):
    for widgets in root.winfo_children():
        widgets.destroy()
    root.title("Zigla's LMS- Search Result")
    
    create_nav_bar(root, navigate_to, theme)

    tree = ttk.Treeview(
        root, 
        columns=("ID", "Title", "Genre", "Author", "ISBN", "Is_borrowed", "Borrower_id"), 
        show="headings", 
        style="Modern.Treeview"
    )
    
    headings = ["ID", "Title", "Genre", "Author", "ISBN", "Is_borrowed", "Borrower_id"]
    for col in headings:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120) 

    scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=scrollbar.set)

    def capitalized_row(text):
        return text.title()
    
    for row in search:
        capitalized_words = [capitalized_row(str(item)) for item in row]
        tree.insert("", tk.END, values=capitalized_words)

    style = ttk.Style()

    style.configure(
        "Modern.Treeview",
        font=("Helvetica", 12), 
        rowheight=30,
        background="#f9f9f9",
        foreground="#333",
        fieldbackground="#f4f4f4"
    )
    style.configure(
        "Modern.Treeview.Heading",
        font=("Helvetica", 14, "bold"),
        background="#4CAF50",
        foreground="black",
        padding=5
    )
    style.map(
        "Modern.Treeview.Heading",
        background=[("active", "#45a049")],
        relief=[("pressed", "sunken"), ("!pressed", "flat")]
    )
    
    style.configure("Vertical.TScrollbar", gripcount=0, background="#ccc", troughcolor="#e6e6e6")


def open_borrower_result(borrowers):
    for widgets in root.winfo_children():
        widgets.destroy()
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


    tree = ttk.Treeview(
        root, 
        columns=("ID", "Borrower ID", "Name", "Email", "is_returned", "book_id"), 
        show="headings", 
        style="Modern.Treeview"
    )

    headings = ["ID", "Borrower ID", "Name", "Email", "is_returned", "book_id"]
    for col in headings:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=150) 

    scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=tree.yview)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tree.configure(yscrollcommand=scrollbar.set)



    def capitalized_row(text):
        return text.title()
    
    for row in borrowers:
        capitalized_words = [capitalized_row(str(item)) for item in row]
        tree.insert("", tk.END, values=capitalized_words)


    style = ttk.Style()

    style.configure(
        "Modern.Treeview",
        font=("Helvetica", 12), 
        rowheight=30,
        background="#f9f9f9",
        foreground="#333",
        fieldbackground="#f4f4f4"
    )
    style.configure(
        "Modern.Treeview.Heading",
        font=("Helvetica", 14, "bold"),
        background="#4CAF50",
        foreground="black",
        padding=5
    )
    style.map(
        "Modern.Treeview.Heading",
        background=[("active", "#45a049")],
        relief=[("pressed", "sunken"), ("!pressed", "flat")]
    )

    style.configure("Vertical.TScrollbar", gripcount=0, background="#ccc", troughcolor="#e6e6e6")



# Run the main window
if __name__ == "__main__":
    main_window()
