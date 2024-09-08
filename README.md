Library Management System
A Python-based desktop application for managing a library's book inventory, built using Tkinter for the graphical user interface (GUI) and SQLite for database management. This system allows users to add, view, update, and delete book records, as well as track the availability of books and manage issuer details.

Features
Add Book Records: Users can add new book records with details such as book title, author, status (available or issued), and issuer ID.
View Records: A tree-view structure displays all the books in the library with their respective details.
Update Book Information: Allows updating details such as book title, author, and status.
Delete Book: Users can remove specific books from the library or delete the entire inventory.
Toggle Availability: Easily change the status of a book between 'Available' and 'Issued' when returned or borrowed.
Clear Input Fields: Quickly reset the input fields for new data entry.
Footer: Displays the footer "Developed by Geofrey Ojijo."
Technologies Used
Python: Programming language.
Tkinter: GUI framework.
SQLite: Database for storing book records.
Prerequisites
Python 3.x: Ensure Python is installed on your system.
SQLite: No need to install separately, as Python comes with SQLite built-in.

Application Structure
Add Book: Input the book details (title, author, book ID, and status), and add them to the library's inventory.
View & Edit Books: Select books from the list to view or modify their details.
Change Book Status: Toggle between 'Available' and 'Issued' status based on the book's current availability.
Clear Fields: Reset all input fields.
Footer: Displays the footer with the text "Developed by Geofrey Ojijo."
GUI Components
Frames and Labels: Organize the UI with labels for book details such as title, author, book ID, and status.
Entry Fields: For entering the book details.
TreeView: Displays the list of books in a structured format with columns for title, ID, author, status, and issuer.
Buttons: Perform actions like add, delete, update, and change availability.
Color Scheme
The GUI features a visually appealing color scheme with a dark blue/purple background, bright button colors, and contrasting text for ease of use and readability.

Background: Dark blue and purple shades.
Labels and Buttons: Colorful and contrasting for better visual impact.
Footer: Displayed in a soft color with italic font.
License
This project is open-source and free to use. Feel free to modify and improve it.

Developed By
Geofrey Ojijo

Enjoy managing your library efficiently with this user-friendly management system!
