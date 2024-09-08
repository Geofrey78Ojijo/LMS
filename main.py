# Importing required modules
import sqlite3
from tkinter import *
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog

# Database connection setup
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create the Library table if it doesn't exist
conn.execute(
    '''CREATE TABLE IF NOT EXISTS Books (
        Title TEXT, 
        Book_ID TEXT PRIMARY KEY NOT NULL, 
        Author TEXT, 
        Status TEXT, 
        Issuer_ID TEXT
    )'''
)

# Function to get Issuer's Card ID
def get_issuer_id():
    issuer_id = simpledialog.askstring('Issuer Card', 'Please enter the Issuer\'s Card ID:')
    
    if not issuer_id:
        messagebox.showerror('Invalid Entry', 'Issuer Card ID cannot be empty!')
        return None
    return issuer_id

# Display records in the treeview
def refresh_display():
    tree.delete(*tree.get_children())
    cursor.execute('SELECT * FROM Books')
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)

# Clear input fields
def clear_inputs():
    book_title.set('')
    book_id.set('')
    author.set('')
    status.set('Available')
    issuer_id.set('')
    book_id_entry.config(state='normal')

# Add new book record to the database
def add_book():
    if status.get() == 'Issued':
        issuer_id.set(get_issuer_id())
    
    if not messagebox.askyesno('Confirm Entry', 'Are you sure you want to add this record?'):
        return
    
    try:
        conn.execute(
            'INSERT INTO Books (Title, Book_ID, Author, Status, Issuer_ID) VALUES (?, ?, ?, ?, ?)',
            (book_title.get(), book_id.get(), author.get(), status.get(), issuer_id.get() or 'N/A')
        )
        conn.commit()
        refresh_display()
        messagebox.showinfo('Success', 'Book record added successfully!')
        clear_inputs()
    except sqlite3.IntegrityError:
        messagebox.showerror('Duplicate Entry', 'Book ID already exists in the database.')

# View selected record
def view_record():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror('Selection Error', 'Please select a record to view.')
        return

    record = tree.item(selected_item)['values']
    book_title.set(record[0])
    book_id.set(record[1])
    author.set(record[2])
    status.set(record[3])
    issuer_id.set(record[4])
    book_id_entry.config(state='disabled')

# Update existing book record
def update_book():
    if status.get() == 'Issued':
        issuer_id.set(get_issuer_id())

    cursor.execute(
        'UPDATE Books SET Title=?, Author=?, Status=?, Issuer_ID=? WHERE Book_ID=?',
        (book_title.get(), author.get(), status.get(), issuer_id.get(), book_id.get())
    )
    conn.commit()
    refresh_display()
    clear_inputs()

# Remove selected record
def remove_book():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror('Selection Error', 'Please select a record to delete.')
        return

    book_id_to_delete = tree.item(selected_item)['values'][1]
    cursor.execute('DELETE FROM Books WHERE Book_ID=?', (book_id_to_delete,))
    conn.commit()
    refresh_display()

# Delete all records
def clear_inventory():
    if messagebox.askyesno('Confirm Deletion', 'Are you sure you want to delete the entire inventory?'):
        cursor.execute('DELETE FROM Books')
        conn.commit()
        refresh_display()

# Change book availability
def toggle_availability():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror('Selection Error', 'Please select a book to update.')
        return

    record = tree.item(selected_item)['values']
    book_id_to_update = record[1]
    current_status = record[3]

    if current_status == 'Issued':
        if messagebox.askyesno('Return Confirmation', 'Has the book been returned?'):
            cursor.execute('UPDATE Books SET Status=?, Issuer_ID=? WHERE Book_ID=?', ('Available', 'N/A', book_id_to_update))
            conn.commit()
        else:
            messagebox.showerror('Action Denied', 'Cannot mark the book as available until it is returned.')
    else:
        issuer_card = get_issuer_id()
        if issuer_card:
            cursor.execute('UPDATE Books SET Status=?, Issuer_ID=? WHERE Book_ID=?', ('Issued', issuer_card, book_id_to_update))
            conn.commit()

    refresh_display()

# Setting up the GUI
root = Tk()
root.title('Library Management System')
root.geometry('1000x600')

# Color scheme
bg_color = "#1a1a2e"
header_color = "#16213e"
btn_color = "#0f3460"
label_color = "#e94560"
entry_bg = "#f0f0f0"
entry_fg = "#1a1a2e"
text_color = "#ffffff"

# Footer Label
footer_font = ('Helvetica', 10, 'italic')

# Variables
book_title = StringVar()
book_id = StringVar()
author = StringVar()
status = StringVar(value='Available')
issuer_id = StringVar()

# Styling the window
root.configure(bg=bg_color)

# Input Form
Label(root, text='Book Title', bg=bg_color, fg=text_color).grid(row=0, column=0, padx=10, pady=10)
Entry(root, textvariable=book_title, bg=entry_bg, fg=entry_fg).grid(row=0, column=1, padx=10, pady=10)

Label(root, text='Book ID', bg=bg_color, fg=text_color).grid(row=1, column=0, padx=10, pady=10)
book_id_entry = Entry(root, textvariable=book_id, bg=entry_bg, fg=entry_fg)
book_id_entry.grid(row=1, column=1, padx=10, pady=10)

Label(root, text='Author', bg=bg_color, fg=text_color).grid(row=2, column=0, padx=10, pady=10)
Entry(root, textvariable=author, bg=entry_bg, fg=entry_fg).grid(row=2, column=1, padx=10, pady=10)

Label(root, text='Status', bg=bg_color, fg=text_color).grid(row=3, column=0, padx=10, pady=10)
OptionMenu(root, status, 'Available', 'Issued').grid(row=3, column=1, padx=10, pady=10)

Button(root, text='Add Book', command=add_book, bg=btn_color, fg=text_color).grid(row=4, column=0, padx=10, pady=10)
Button(root, text='Clear', command=clear_inputs, bg=btn_color, fg=text_color).grid(row=4, column=1, padx=10, pady=10)

# Treeview for displaying records
columns = ('Title', 'Book_ID', 'Author', 'Status', 'Issuer_ID')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Control Buttons
Button(root, text='Update', command=update_book, bg=btn_color, fg=text_color).grid(row=6, column=0, padx=10, pady=10)
Button(root, text='Delete', command=remove_book, bg=btn_color, fg=text_color).grid(row=6, column=1, padx=10, pady=10)
Button(root, text='Clear Inventory', command=clear_inventory, bg=btn_color, fg=text_color).grid(row=7, column=0, padx=10, pady=10)
Button(root, text='Toggle Availability', command=toggle_availability, bg=btn_color, fg=text_color).grid(row=7, column=1, padx=10, pady=10)

# Footer
footer_label = Label(root, text="Developed by Geofrey Ojijo", bg=bg_color, fg=label_color, font=footer_font)
footer_label.grid(row=8, column=0, columnspan=2, pady=20)

# Populate records initially
refresh_display()

# Run the application
root.mainloop()
