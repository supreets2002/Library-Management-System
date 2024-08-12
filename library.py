import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Database setup
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Creating tables
cursor.execute("""
    CREATE TABLE IF NOT EXISTS authors (
        author_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author_id INTEGER,
        FOREIGN KEY (author_id) REFERENCES authors (author_id)
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS members (
        member_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS borrow_records (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER,
        member_id INTEGER,
        borrow_date TEXT,
        return_date TEXT,
        FOREIGN KEY (book_id) REFERENCES books (book_id),
        FOREIGN KEY (member_id) REFERENCES members (member_id)
    )
""")
conn.commit()

# Functions for database operations
def insert_author(name):
    cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
    conn.commit()

def insert_book(title, author_id):
    cursor.execute("INSERT INTO books (title, author_id) VALUES (?, ?)", (title, author_id))
    conn.commit()

def insert_member(name):
    cursor.execute("INSERT INTO members (name) VALUES (?)", (name,))
    conn.commit()

def insert_borrow_record(book_id, member_id, borrow_date, return_date):
    cursor.execute("INSERT INTO borrow_records (book_id, member_id, borrow_date, return_date) VALUES (?, ?, ?, ?)", (book_id, member_id, borrow_date, return_date))
    conn.commit()

def get_authors():
    cursor.execute("SELECT * FROM authors")
    return cursor.fetchall()

def get_books():
    cursor.execute("SELECT books.book_id, books.title, authors.name FROM books JOIN authors ON books.author_id = authors.author_id")
    return cursor.fetchall()

def get_members():
    cursor.execute("SELECT * FROM members")
    return cursor.fetchall()

def get_borrow_records():
    cursor.execute("""
        SELECT borrow_records.record_id, books.title, members.name, borrow_records.borrow_date, borrow_records.return_date 
        FROM borrow_records 
        JOIN books ON borrow_records.book_id = books.book_id 
        JOIN members ON borrow_records.member_id = members.member_id
    """)
    return cursor.fetchall()

def update_author(author_id, name):
    cursor.execute("UPDATE authors SET name=? WHERE author_id=?", (name, author_id))
    conn.commit()

def update_book(book_id, title, author_id):
    cursor.execute("UPDATE books SET title=?, author_id=? WHERE book_id=?", (title, author_id, book_id))
    conn.commit()


def update_member(member_id, name):
    cursor.execute("UPDATE members SET name=? WHERE member_id=?", (name, member_id))
    conn.commit()

def update_borrow_record(record_id, book_id, member_id, borrow_date, return_date):
    cursor.execute("UPDATE borrow_records SET book_id=?, member_id=?, borrow_date=?, return_date=? WHERE record_id=?", (book_id, member_id, borrow_date, return_date, record_id))
    conn.commit()

def delete_author(author_id):
    cursor.execute("DELETE FROM authors WHERE author_id=?", (author_id,))
    conn.commit()

def delete_book(book_id):
    cursor.execute("DELETE FROM books WHERE book_id=?", (book_id,))
    conn.commit()

def delete_member(member_id):
    cursor.execute("DELETE FROM members WHERE member_id=?", (member_id,))
    conn.commit()

def delete_borrow_record(record_id):
    cursor.execute("DELETE FROM borrow_records WHERE record_id=?", (record_id,))
    conn.commit()

# GUI setup
class LibraryManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.create_widgets()

    def create_widgets(self):
        # Notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=0, column=0, padx=10, pady=10)

        # Tabs
        self.tab_authors = tk.Frame(self.notebook)
        self.tab_books = tk.Frame(self.notebook)
        self.tab_members = tk.Frame(self.notebook)
        self.tab_borrow_records = tk.Frame(self.notebook)

        self.notebook.add(self.tab_authors, text="Authors")
        self.notebook.add(self.tab_books, text="Books")
        self.notebook.add(self.tab_members, text="Members")
        self.notebook.add(self.tab_borrow_records, text="Borrow Records")

        # Authors tab
        self.authors_listbox = tk.Listbox(self.tab_authors)
        self.authors_listbox.grid(row=0, column=0, columnspan=2)
        self.load_authors()

        self.author_name_label = tk.Label(self.tab_authors, text="Name")
        self.author_name_label.grid(row=1, column=0)
        self.author_name_entry = tk.Entry(self.tab_authors)
        self.author_name_entry.grid(row=1, column=1)

        self.add_author_button = tk.Button(self.tab_authors, text="Add Author", command=self.add_author)
        self.add_author_button.grid(row=2, column=0, columnspan=2)

        self.update_author_button = tk.Button(self.tab_authors, text="Update Author", command=self.update_author)
        self.update_author_button.grid(row=3, column=0, columnspan=2)

        self.delete_author_button = tk.Button(self.tab_authors, text="Delete Author", command=self.delete_author)
        self.delete_author_button.grid(row=4, column=0, columnspan=2)

        # Books tab
        self.books_listbox = tk.Listbox(self.tab_books)
        self.books_listbox.grid(row=0, column=0, columnspan=2)
        self.load_books()

        self.book_title_label = tk.Label(self.tab_books, text="Title")
        self.book_title_label.grid(row=1, column=0)
        self.book_title_entry = tk.Entry(self.tab_books)
        self.book_title_entry.grid(row=1, column=1)

        self.book_author_label = tk.Label(self.tab_books, text="Author")
        self.book_author_label.grid(row=2, column=0)
        self.book_author_combobox = ttk.Combobox(self.tab_books)
        self.book_author_combobox.grid(row=2, column=1)
        self.load_author_combobox()

        self.add_book_button = tk.Button(self.tab_books, text="Add Book", command=self.add_book)
        self.add_book_button.grid(row=3, column=0, columnspan=2)

        self.update_book_button = tk.Button(self.tab_books, text="Update Book", command=self.update_book)
        self.update_book_button.grid(row=4, column=0, columnspan=2)

        self.delete_book_button = tk.Button(self.tab_books, text="Delete Book", command=self.delete_book)
        self.delete_book_button.grid(row=5, column=0, columnspan=2)

        # Members tab
        self.members_listbox = tk.Listbox(self.tab_members)
        self.members_listbox.grid(row=0, column=0, columnspan=2)
        self.load_members()

        self.member_name_label = tk.Label(self.tab_members, text="Name")
        self.member_name_label.grid(row=1, column=0)
        self.member_name_entry = tk.Entry(self.tab_members)
        self.member_name_entry.grid(row=1, column=1)

        self.add_member_button = tk.Button(self.tab_members, text="Add Member", command=self.add_member)
        self.add_member_button.grid(row=2, column=0, columnspan=2)

        self.update_member_button = tk.Button(self.tab_members, text="Update Member", command=self.update_member)
        self.update_member_button.grid(row=3, column=0, columnspan=2)

        self.delete_member_button = tk.Button(self.tab_members, text="Delete Member", command=self.delete_member)
        self.delete_member_button.grid(row=4, column=0, columnspan=2)

        # Borrow Records tab
        self.borrow_records_listbox = tk.Listbox(self.tab_borrow_records)
        self.borrow_records_listbox.grid(row=0, column=0, columnspan=2)
        self.load_borrow_records()

        self.borrow_book_label = tk.Label(self.tab_borrow_records, text="Book")
        self.borrow_book_label.grid(row=1, column=0)
        self.borrow_book_combobox = ttk.Combobox(self.tab_borrow_records)
        self.borrow_book_combobox.grid(row=1, column=1)
        self.load_book_combobox()

        self.borrow_member_label = tk.Label(self.tab_borrow_records, text="Member")
        self.borrow_member_label.grid(row=2, column=0)
        self.borrow_member_combobox = ttk.Combobox(self.tab_borrow_records)
        self.borrow_member_combobox.grid(row=2, column=1)
        self.load_member_combobox()

        self.borrow_date_label = tk.Label(self.tab_borrow_records, text="Borrow Date")
        self.borrow_date_label.grid(row=3, column=0)
        self.borrow_date_entry = tk.Entry(self.tab_borrow_records)
        self.borrow_date_entry.grid(row=3, column=1)

        self.return_date_label = tk.Label(self.tab_borrow_records, text="Return Date")
        self.return_date_label.grid(row=4, column=0)
        self.return_date_entry = tk.Entry(self.tab_borrow_records)
        self.return_date_entry.grid(row=4, column=1)

        self.add_borrow_record_button = tk.Button(self.tab_borrow_records, text="Add Borrow Record", command=self.add_borrow_record)
        self.add_borrow_record_button.grid(row=5, column=0, columnspan=2)

        self.update_borrow_record_button = tk.Button(self.tab_borrow_records, text="Update Borrow Record", command=self.update_borrow_record)
        self.update_borrow_record_button.grid(row=6, column=0, columnspan=2)

        self.delete_borrow_record_button = tk.Button(self.tab_borrow_records, text="Delete Borrow Record", command=self.delete_borrow_record)
        self.delete_borrow_record_button.grid(row=7, column=0, columnspan=2)

    def load_authors(self):
        self.authors_listbox.delete(0, tk.END)
        for author in get_authors():
            self.authors_listbox.insert(tk.END, f"{author[0]} {author[1]}")

    def load_books(self):
        self.books_listbox.delete(0, tk.END)
        for book in get_books():
            self.books_listbox.insert(tk.END, f"{book[0]} {book[1]} {book[2]}")

    def load_members(self):
        self.members_listbox.delete(0, tk.END)
        for member in get_members():
            self.members_listbox.insert(tk.END, f"{member[0]} {member[1]}")

    def load_borrow_records(self):
        self.borrow_records_listbox.delete(0, tk.END)
        for record in get_borrow_records():
            self.borrow_records_listbox.insert(tk.END, f"{record[0]} {record[1]} {record[2]} {record[3]} {record[4]}")

    def load_author_combobox(self):
        self.book_author_combobox['values'] = [f"{author[0]} {author[1]}" for author in get_authors()]

    def load_book_combobox(self):
        self.borrow_book_combobox['values'] = [f"{book[0]} {book[1]}" for book in get_books()]

    def load_member_combobox(self):
        self.borrow_member_combobox['values'] = [f"{member[0]} {member[1]}" for member in get_members()]

    def add_author(self):
        name = self.author_name_entry.get()
        if name:
            insert_author(name)
            self.load_authors()
            self.load_author_combobox()
            messagebox.showinfo("Success", "Author added successfully!")
        else:
            messagebox.showerror("Error", "Please enter author name")

    def add_book(self):
        title = self.book_title_entry.get()
        author_id = self.book_author_combobox.get().split()[0]
        if title and author_id:
            insert_book(title, author_id)
            self.load_books()
            self.load_book_combobox()
            messagebox.showinfo("Success", "Book added successfully!")
        else:
            messagebox.showerror("Error", "Please fill all fields")

    def add_member(self):
        name = self.member_name_entry.get()
        if name:
            insert_member(name)
            self.load_members()
            self.load_member_combobox()
            messagebox.showinfo("Success", "Member added successfully!")
        else:
            messagebox.showerror("Error", "Please enter member name")

    def add_borrow_record(self):
        book_id = self.borrow_book_combobox.get().split()[0]
        member_id = self.borrow_member_combobox.get().split()[0]
        borrow_date = self.borrow_date_entry.get()
        return_date = self.return_date_entry.get()
        if book_id and member_id and borrow_date and return_date:
            insert_borrow_record(book_id, member_id, borrow_date, return_date)
            self.load_borrow_records()
            messagebox.showinfo("Success", "Borrow record added successfully!")
        else:
            messagebox.showerror("Error", "Please fill all fields")

    def update_author(self):
        try:
            selected_item = self.authors_listbox.curselection()[0]
            author_id = self.authors_listbox.get(selected_item).split()[0]
            name = self.author_name_entry.get()
            if name:
                update_author(author_id, name)
                self.load_authors()
                self.load_author_combobox()
                messagebox.showinfo("Success", "Author updated successfully!")
            else:
                messagebox.showerror("Error", "Please enter author name")
        except IndexError:
            messagebox.showerror("Error", "Please select an author to update")

    def update_book(self):
        try:
            selected_item = self.books_listbox.curselection()[0]
            book_id = self.books_listbox.get(selected_item).split()[0]
            title = self.book_title_entry.get()
            author_id = self.book_author_combobox.get().split()[0]
            if title and author_id:
                update_book(book_id, title, author_id)
                self.load_books()
                self.load_book_combobox()
                messagebox.showinfo("Success", "Book updated successfully!")
            else:
                messagebox.showerror("Error", "Please fill all fields")
        except IndexError:
            messagebox.showerror("Error", "Please select a book to update")


    def update_member(self):
        try:
            selected_item = self.members_listbox.curselection()[0]
            member_id = self.members_listbox.get(selected_item).split()[0]
            name = self.member_name_entry.get()
            if name:
                update_member(member_id, name)
                self.load_members()
                self.load_member_combobox()
                messagebox.showinfo("Success", "Member updated successfully!")
            else:
                messagebox.showerror("Error", "Please enter member name")
        except IndexError:
            messagebox.showerror("Error", "Please select a member to update")

    def update_borrow_record(self):
        try:
            selected_item = self.borrow_records_listbox.curselection()[0]
            record_id = self.borrow_records_listbox.get(selected_item).split()[0]
            book_id = self.borrow_book_combobox.get().split()[0]
            member_id = self.borrow_member_combobox.get().split()[0]
            borrow_date = self.borrow_date_entry.get()
            return_date = self.return_date_entry.get()
            if book_id and member_id and borrow_date and return_date:
                update_borrow_record(record_id, book_id, member_id, borrow_date, return_date)
                self.load_borrow_records()
                messagebox.showinfo("Success", "Borrow record updated successfully!")
            else:
                messagebox.showerror("Error", "Please fill all fields")
        except IndexError:
            messagebox.showerror("Error", "Please select a borrow record to update")

    def delete_author(self):
        try:
            selected_item = self.authors_listbox.curselection()[0]
            author_id = self.authors_listbox.get(selected_item).split()[0]
            delete_author(author_id)
            self.load_authors()
            self.load_author_combobox()
            messagebox.showinfo("Success", "Author deleted successfully!")
        except IndexError:
            messagebox.showerror("Error", "Please select an author to delete")

    def delete_book(self):
        try:
            selected_item = self.books_listbox.curselection()[0]
            book_id = self.books_listbox.get(selected_item).split()[0]
            delete_book(book_id)
            self.load_books()
            self.load_book_combobox()
            messagebox.showinfo("Success", "Book deleted successfully!")
        except IndexError:
            messagebox.showerror("Error", "Please select a book to delete")

    def delete_member(self):
        try:
            selected_item = self.members_listbox.curselection()[0]
            member_id = self.members_listbox.get(selected_item).split()[0]
            delete_member(member_id)
            self.load_members()
            self.load_member_combobox()
            messagebox.showinfo("Success", "Member deleted successfully!")
        except IndexError:
            messagebox.showerror("Error", "Please select a member to delete")

    def delete_borrow_record(self):
        try:
            selected_item = self.borrow_records_listbox.curselection()[0]
            record_id = self.borrow_records_listbox.get(selected_item).split()[0]
            delete_borrow_record(record_id)
            self.load_borrow_records()
            messagebox.showinfo("Success", "Borrow record deleted successfully!")
        except IndexError:
            messagebox.showerror("Error", "Please select a borrow record to delete")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementApp(root)
    root.mainloop()
