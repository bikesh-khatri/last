import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import re
from datetime import datetime

def register_page(root):
    root.withdraw()
    register_win = tk.Toplevel(root)
    register_win.title("Registration Page")
    register_win.geometry("850x500")
    register_win.configure(bg="white")
    register_win.iconbitmap("abc.ico")

    def register():
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        email = entry_email.get()
        password = entry_password.get()
        confirm_password = entry_confirm_password.get()
        number_of_rooms = entry_number_of_rooms.get()

        if not all([first_name, last_name, email, password, confirm_password, number_of_rooms]):
            messagebox.showerror("Error", "All fields are required!")
            return
        elif password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return
        # Email format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            messagebox.showerror("Error", "Invalid email format! Use: example@domain.com")
            return
        try:
            number_of_rooms = int(number_of_rooms)
            if number_of_rooms <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Number of rooms must be a positive integer!")
            return

        conn = sqlite3.connect("new.db")
        cursor = conn.cursor()

        try:
            # Insert user
            cursor.execute("INSERT INTO users (first_name, last_name, email, password, number_of_rooms) VALUES (?, ?, ?, ?, ?)",
                        (first_name, last_name, email, password, number_of_rooms))
            user_id = cursor.lastrowid  # Get the new user’s ID

            # Insert rooms
            for i in range(number_of_rooms):
                cursor.execute("INSERT INTO room (user_id, room_no, capacity) VALUES (?, ?, ?)",( user_id, i+1, 4))

            # Prepopulate default meal plan (e.g., for 7 days)
            default_meals = [
                (user_id, "Monday", "Toast", "Fruit", "Sandwich", "Pasta"),
                (user_id, "Tuesday", "Omelette", "Yogurt", "Burger", "Rice"),
                (user_id, "Wednesday", "Pancakes", "Juice", "Salad", "Chicken"),
                (user_id, "Thursday", "Cereal", "Smoothie", "Pizza", "Fish"),
                (user_id, "Friday", "Bagel", "Milk", "Tacos", "Steak"),
                (user_id, "Saturday", "Waffles", "Tea", "Wrap", "Soup"),
                (user_id, "Sunday", "Eggs", "Coffee", "Pasta", "Roast")
            ]
            cursor.executemany("INSERT INTO meal (user_id, day, breakfast, meal, lunch, dinner) VALUES (?, ?, ?, ?, ?, ?)", default_meals)

            conn.commit()
            messagebox.showinfo("Success", "Registration successful!")
            register_win.destroy()
            login_page(root)
        except sqlite3.IntegrityError:
            messagebox.showerror("Signup failed", "Email already exists!")
        finally:
            conn.close()

    # UI setup (logo_frame remains unchanged)
    logo_frame = tk.Frame(register_win, width=300, height=500, bg="gray")
    logo_frame.pack(side="left", fill="both")
    try:
        logo = Image.open("abc.png")
        logo = logo.resize((250, 250), Image.Resampling.LANCZOS)
        logo_img = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(logo_frame, image=logo_img, bg="gray")
        logo_label.image = logo_img
        logo_label.pack(pady=50)
    except Exception as e:
        print(f"Error loading logo: {e}")

    form_frame = tk.Frame(register_win, bg="white")
    form_frame.pack(side="right", expand=True, fill="both", padx=40, pady=20)

    tk.Label(form_frame, text="Register", font=("Arial", 18, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

    entry_first_name = tk.Entry(form_frame, font=("Arial", 12))
    entry_last_name = tk.Entry(form_frame, font=("Arial", 12))
    entry_email = tk.Entry(form_frame, font=("Arial", 12))
    entry_password = tk.Entry(form_frame, font=("Arial", 12), show="*")
    entry_confirm_password = tk.Entry(form_frame, font=("Arial", 12), show="*")
    entry_number_of_rooms = tk.Entry(form_frame, font=("Arial", 12))

    labels = ["First Name:", "Last Name:", "Email:", "Password:", "Confirm Password:", "Number of Rooms:"]
    entries = [entry_first_name, entry_last_name, entry_email, entry_password, entry_confirm_password, entry_number_of_rooms]

    for i, (label, entry) in enumerate(zip(labels, entries)):
        tk.Label(form_frame, text=label, font=("Arial", 12), bg="white").grid(row=i+1, column=0, sticky="w", pady=5)
        entry.grid(row=i+1, column=1, pady=5, padx=10)

    tk.Button(form_frame, text="Register", command=register, bg="#4CAF50", fg="white", font=("Arial", 12)).grid(row=8, column=0, columnspan=2, pady=20)

    tk.Label(form_frame, text="Already a member?", font=("Arial", 10), bg="white").grid(row=9, column=0, pady=5, sticky="e")
    gotoLogin = tk.Button(form_frame, text="Login Here", font=("Arial", 10, "underline"), fg="blue", bg="white", bd=0, cursor="hand2",
                          command=lambda: [register_win.destroy(), login_page(root)])
    gotoLogin.grid(row=9, column=1, sticky="w")

def login_page(root):
    root.withdraw()
    login_win = tk.Toplevel(root)
    login_win.title("Login Page")
    login_win.geometry("900x500")
    login_win.configure(bg="#f4f4f4")
    login_win.iconbitmap("abc.ico")

    # UI setup (logo_frame remains unchanged)
    logo_frame = tk.Frame(login_win, width=300, height=500, bg="gray")
    logo_frame.pack(side="left", fill="both")
    try:
        logo = Image.open("abc.png")
        logo = logo.resize((250, 250), Image.Resampling.LANCZOS)
        logo_img = ImageTk.PhotoImage(logo)
        logo_label = tk.Label(logo_frame, image=logo_img, bg="gray")
        logo_label.image = logo_img
        logo_label.pack(pady=50)
    except Exception as e:
        print(f"Error loading logo: {e}")

    form_frame = tk.Frame(login_win, bg="white")
    form_frame.pack(side="right", expand=True, fill="both", padx=40, pady=20)

    def check_login():
        email = entry_email.get()
        password = entry_password.get()

        if not email or not password:
            messagebox.showerror("Invalid Input", "Fields must not be empty!")
            return

        conn = sqlite3.connect("new.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE email = ? AND password = ?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Success", "Logged in successfully!")  # Added login messagebox
            login_win.destroy()
            admin_dashboard(user[0])  # Pass user_id to dashboard
        else:
            messagebox.showerror("Login failed", "Invalid email or password")

    # UI setup continues (form_frame remains largely unchanged)
    frame = tk.Frame(login_win, bg="white", padx=40, pady=40)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(frame, text="Email:", font=("Arial", 12), bg="white").grid(row=1, column=0, pady=10, sticky="e")
    entry_email = tk.Entry(frame, font=("Arial", 12))
    entry_email.grid(row=1, column=1, pady=10)

    tk.Label(frame, text="Password:", font=("Arial", 12, "bold"), bg="white").grid(row=2, column=0, pady=10, sticky="e")
    entry_password = tk.Entry(frame, font=("Arial", 12), show="*")
    entry_password.grid(row=2, column=1, pady=10)

    tk.Button(frame, text="Login", command=check_login, bg="#4CAF50", fg="white", font=("Arial", 12), padx=20, pady=5).grid(row=5, column=0, columnspan=2, pady=20)

    tk.Label(frame, text="Create new account?", font=("Arial", 10), bg="white").grid(row=9, column=0, pady=5, sticky="e")
    gotoRegister = tk.Button(frame, text="Register Here", font=("Arial", 10, "underline"), fg="blue", bg="white", bd=0, cursor="hand2",
                          command=lambda: [login_win.destroy(), register_page(root)])
    gotoRegister.grid(row=9, column=1, sticky="w")

def admin_dashboard(user_id):
    dashboard = tk.Toplevel()
    dashboard.title("Warden Sab")
    dashboard.geometry("800x600")
    dashboard.configure(bg="#f0f0f0")
    dashboard.iconbitmap("abc.ico")

    welcome_label = tk.Label(dashboard, text="Welcome!", font=("Arial", 24, "bold"), bg="#F0F0F0", fg="black")
    welcome_label.pack(pady=20)

    button_frame = tk.Frame(dashboard, bg="#f0f0f0")
    button_frame.pack(expand=True, fill="both", padx=20, pady=20)

    button_frame.columnconfigure(0, weight=1)
    button_frame.columnconfigure(1, weight=1)

    button_width = 15
    button_height = 5

    meal_button = tk.Button(button_frame, text="Meal", command=lambda: [dashboard.destroy(), meal_management(user_id)], bg="#4CAF50", fg="white", font=("Arial", 14), width=button_width, height=button_height)
    meal_button.grid(row=1, column=0, padx=50, pady=20, sticky="nw")

    student_button = tk.Button(button_frame, text="Students", command=lambda: [dashboard.destroy(), students(user_id)], bg="#4CAF50", fg="white", font=("Arial", 14), width=button_width, height=button_height)
    student_button.grid(row=2, column=0, padx=50, pady=20, sticky="nw")

    fee_button = tk.Button(button_frame, text="Add Student", command=lambda: [dashboard.destroy(), add_students(user_id)], bg="#4CAF50", fg="white", font=("Arial", 14), width=button_width, height=button_height)
    fee_button.grid(row=1, column=1, padx=50, pady=20, sticky="ne")

    room_button = tk.Button(button_frame, text="Room Details", command=lambda: [dashboard.destroy(), room(user_id)], bg="#4CAF50", fg="white", font=("Arial", 14), width=button_width, height=button_height)
    room_button.grid(row=2, column=1, padx=50, pady=20, sticky="ne")

    # New Edit Profile Button
    edit_profile_button = tk.Button(button_frame, text="Edit Profile", command=lambda: [dashboard.destroy(), 
                                                                                        edit_user_profile
                                                                                        (user_id)], 
                                                                                        bg="#4CAF50", 
                                                                                        fg="white", 
                                                                                        font=("Arial", 14), 
                                                                                        width=button_width, 
                                                                                        height=button_height)
    edit_profile_button.grid(row=3, column=0, padx=50, pady=20, sticky="sw")

    # Logout button with messagebox
    logout_button = tk.Button(button_frame, text="Logout", command=lambda: [messagebox.showinfo("Logout", 
    "Logged out successfully!"), dashboard.destroy(), login_page(root)], bg="#FF0000", fg="white", 
    font=("Arial", 14), width=button_width, height=button_height)
    logout_button.grid(row=3, column=1, padx=50, pady=20, sticky="se")

def edit_user_profile(user_id):
    profile_win = tk.Toplevel()
    profile_win.title("Edit Profile")
    profile_win.geometry("400x500")
    profile_win.configure(bg="#f0f0f0")
    profile_win.iconbitmap("abc.ico")

    back_button = tk.Label(profile_win, text="←", font=("Arial", 10), bg="#f0f0f0", fg="black", cursor="hand2")
    back_button.place(x=10, y=10)
    back_button.bind("<Button-1>", lambda e: [profile_win.destroy(), admin_dashboard(user_id)])

    tk.Label(profile_win, text="Edit Profile", font=("Arial", 24, "bold"), bg="#F0F0F0").pack(pady=20)

    # Fetch current user details
    conn = sqlite3.connect("new.db")
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, last_name, email, password, number_of_rooms FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()
    conn.close()

    labels = ["First Name", "Last Name", "Email", "Password", "Number of Rooms"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(profile_win, text=label, font=("Arial", 12), bg="#F0F0F0").pack(pady=5)
        entry = tk.Entry(profile_win, font=("Arial", 12))
        entry.pack(pady=2)
        entry.insert(0, user_data[i])
        entries[label] = entry

    def save_profile():
        first_name = entries["First Name"].get()
        last_name = entries["Last Name"].get()
        email = entries["Email"].get()
        password = entries["Password"].get()
        number_of_rooms = entries["Number of Rooms"].get()

        if not all([first_name, last_name, email, password, number_of_rooms]):
            messagebox.showerror("Error", "All fields are required!")
            return

        # Email format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            messagebox.showerror("Error", "Invalid email format! Use: example@domain.com")
            return

        # Number of rooms validation
        try:
            number_of_rooms = int(number_of_rooms)
            if number_of_rooms <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Number of rooms must be a positive integer!")
            return

        conn = sqlite3.connect("new.db")
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE users 
                SET first_name = ?, last_name = ?, email = ?, password = ?, number_of_rooms = ?
                WHERE id = ?
            """, (first_name, last_name, email, password, number_of_rooms, user_id))
            conn.commit()
            messagebox.showinfo("Success", "Profile updated successfully!")
            profile_win.destroy()
            admin_dashboard(user_id)
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Email already exists!")
        finally:
            conn.close()

    tk.Button(profile_win, text="Save Changes", font=("Arial", 14), bg="#4CAF50", fg="white", command=save_profile).pack(pady=20)

def meal_management(user_id):
    mealBoard = tk.Toplevel()
    mealBoard.title("Warden Sab")
    mealBoard.geometry("800x600")
    mealBoard.configure(bg="#f0f0f0")
    mealBoard.iconbitmap("abc.ico")
    mealBoard.attributes('-fullscreen', True)

    back_button = tk.Label(mealBoard, text="←", font=("Arial", 10), bg="#f0f0f0", fg="black", cursor="hand2")
    back_button.place(x=10, y=10)  
    back_button.bind("<Button-1>", lambda e: [mealBoard.destroy(), admin_dashboard(user_id)]) 

    welcome_label = tk.Label(mealBoard, text="Weekly Meal Plan", font=("Arial", 24, "bold"), bg="#F0F0F0", fg="black")
    welcome_label.pack(pady=20)

    conn = sqlite3.connect("new.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, day, breakfast, meal, lunch, dinner FROM meal WHERE user_id = ?", (user_id,))
    meals = cursor.fetchall()
    conn.close()

    table_frame = tk.Frame(mealBoard, bg="#f0f0f0")
    table_frame.pack()

    headers = ["Day", "Breakfast", "Meal", "Lunch", "Dinner"]
    for col, title in enumerate(headers):
        label = tk.Label(table_frame, text=title, font=("Arial", 14, "bold"), bg="lightgray", padx=10, pady=5, borderwidth=1, relief="solid")
        label.grid(row=0, column=col, sticky="nsew")

    entry_widgets = {}
    for row, meal in enumerate(meals, start=1):
        meal_id = meal[0]
        entry_widgets[meal_id] = []
        for col, value in enumerate(meal[1:]):
            entry = tk.Entry(table_frame, font=("Arial", 12), bg="white", width=15)
            entry.insert(0, value)
            entry.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
            entry_widgets[meal_id].append(entry)

    def save_changes():
        conn = sqlite3.connect("new.db")
        cursor = conn.cursor()
        for meal_id, entries in entry_widgets.items():
            updated_values = [entry.get() for entry in entries]
            cursor.execute("UPDATE meal SET day = ?, breakfast = ?, meal = ?, lunch = ?, dinner = ? WHERE id = ? AND user_id = ?",
                           (*updated_values, meal_id, user_id))
        conn.commit()
        conn.close()
        tk.messagebox.showinfo("Success", "Meal plan updated successfully!")

    save_button = tk.Button(mealBoard, text="Save Changes", font=("Arial", 14, "bold"), bg="green", fg="white", padx=10, pady=5, command=save_changes)
    save_button.pack(pady=20)

def students(user_id):
    students_win = tk.Toplevel()
    students_win.title("Students Details")
    students_win.geometry("1000x600")
    students_win.configure(bg="#f0f0f0")
    students_win.iconbitmap("abc.ico")
    students_win.attributes('-fullscreen', True)

    back_button = tk.Label(students_win, text="←", font=("Arial", 10), bg="#f0f0f0", 
    fg="black", cursor="hand2")
    back_button.place(x=10, y=10)
    back_button.bind("<Button-1>", lambda e: [students_win.destroy(), admin_dashboard(user_id)])

    welcome_label = tk.Label(students_win, text="Students Details", font=("Arial", 24, "bold"), 
    bg="#F0F0F0", fg="black")
    welcome_label.pack(pady=20)
        
    search_frame = tk.Frame(students_win, bg="#f0f0f0")
    search_frame.pack(fill="x", padx=20, pady=10)

    tk.Label(search_frame, text="Search:", font=("Arial", 12), bg="#f0f0f0").pack(side="left", padx=5)
    search_entry = tk.Entry(search_frame, font=("Arial", 12), width=30)
    search_entry.pack(side="left", padx=5)
    search_button = tk.Button(search_frame, text="Search", font=("Arial", 12), bg="#4CAF50",
    fg="white", command=lambda: search_students())
    search_button.pack(side="left", padx=5)

    table_frame = tk.Frame(students_win, bg="#f0f0f0")
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    columns = ("ID", "Name", "DOB", "Address", "Email", "Phone", "Parent Name", "Parent Phone", "Entry Date", "Paid Till", "Room Number")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
    tree.pack(fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)
    tree.column("ID", width=50)
    tree.column("Name", width=150)
    tree.column("DOB", width=100)
    tree.column("Address", width=200)
    tree.column("Email", width=150)
    tree.column("Phone", width=100)
    tree.column("Parent Name", width=150)
    tree.column("Parent Phone", width=100)
    tree.column("Entry Date", width=100)
    tree.column("Paid Till", width=100)
    tree.column("Room Number", width=100)

    def load_students():
        conn = sqlite3.connect("new.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id,name, dob, address, email, number, parent_name, parent_number, entry_date, paid_till, room_number FROM student WHERE user_id = ?", (user_id,))
        students = cursor.fetchall()
        conn.close()
        for row in tree.get_children():
            tree.delete(row)
        for student in students:
            tree.insert("", "end", values=student)
    
    def search_students():
        search_term = search_entry.get().strip().lower()
        if not search_term:
            load_students()  
            return

        for row in tree.get_children():
            tree.delete(row)

        conn = sqlite3.connect("new.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id,name, dob, address, email, number, parent_name, parent_number,entry_date, paid_till, room_number FROM student WHERE name LIKE ? AND user_id=?",(search_term,user_id))
        students = cursor.fetchall()
        conn.close()

        for student in students:
            tree.insert("", "end", values=student, tags=("highlight",)) 
            tree.tag_configure("highlight", background="yellow")

    load_students()

    def edit_student():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student to edit!")
            return

        student_data = tree.item(selected_item, "values")
        edit_win = tk.Toplevel(students_win)
        edit_win.title("Edit Student")
        edit_win.geometry("400x500")
        edit_win.configure(bg="#f0f0f0")

        entries = {}
        labels = ["ID", "Name", "DOB", "Address", "Email", "Phone", "Parent Name", "Parent Phone", "Entry Date", "Paid Till", "Room Number"]
        for i, label in enumerate(labels):
            tk.Label(edit_win, text=label, 
            font=("Arial", 12), bg="#F0F0F0").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(edit_win, font=("Arial", 12))
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            entry.insert(0, student_data[i])
            entries[label] = entry

        def save_edit():
            updated_data = [entries[label].get() for label in labels]
            conn = sqlite3.connect("new.db")
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE student 
                SET name=?, dob=?, address=?, email=?, number=?, parent_name=?, parent_number=?, 
                entry_date=?, paid_till=?, room_number=? WHERE id=? AND user_id=?""", 
                (*updated_data[1:], updated_data[0], user_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student record updated successfully!")
            edit_win.destroy()
            load_students()

        tk.Button(edit_win, text="Save", font=("Arial", 14), bg="#4CAF50", 
        fg="white", command=save_edit).grid(row=len(labels), column=0, columnspan=2, pady=10)

    def remove_student():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student to remove!")
            return
        student_id = tree.item(selected_item, "values")[0]
        room_number = tree.item(selected_item, "values")[10]
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this student?")
        if not confirm:
            return
        conn = sqlite3.connect("new.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM student WHERE id = ? AND user_id = ?", (student_id, user_id))
        if room_number:
            cursor.execute("UPDATE room SET occupied = occupied - 1 WHERE room_no = ? AND user_id = ?", (room_number, user_id))
        conn.commit()
        conn.close()
        tree.delete(selected_item)
        messagebox.showinfo("Success", "Student removed successfully!")
    
    load_students()
    button_frame = tk.Frame(students_win, bg="#f0f0f0")
    button_frame.pack(pady=10)
    tk.Button(button_frame, text="Edit Selected Student", font=("Arial", 14), bg="#4CAF50",
     fg="white", command=edit_student).pack(side="left", padx=10)
    tk.Button(button_frame, text="Remove Selected Student", font=("Arial", 14), bg="#FF0000",
     fg="white", command=remove_student).pack(side="left", padx=10)

def add_students(user_id):
    addStudent = tk.Toplevel()
    addStudent.title("Add Student")
    addStudent.geometry("800x600")
    addStudent.configure(bg="#f0f0f0")
    addStudent.iconbitmap("abc.ico")
    addStudent.attributes('-fullscreen', True)

    back_button = tk.Label(addStudent, text="←", font=("Arial", 10), bg="#f0f0f0", 
    fg="black", cursor="hand2")
    back_button.place(x=10, y=10)
    back_button.bind("<Button-1>", lambda e: [addStudent.destroy(), admin_dashboard(user_id)])

    def fetch_rooms():
        conn = sqlite3.connect("new.db")
        cursor = conn.cursor()
        cursor.execute('''SELECT id, room_no, capacity, occupied FROM room WHERE 
                        user_id = ? AND occupied < capacity''', (user_id,))
        rooms_list = cursor.fetchall()
        conn.close()
        return rooms_list

    def submit():
        name = entries["Name"].get()
        dob = entries["Date of Birth (YYYY-MM-DD)"].get()
        address = entries["Address"].get()
        email = entries["Email"].get()
        number = entries["Phone Number"].get()
        parent_name = entries["Parent Name"].get()
        parent_number = entries["Parent Number"].get()
        entry_date = entries["Entry Date (YYYY-MM-DD)"].get()
        paid_till = entries["Paid Till (YYYY-MM-DD)"].get()
        selected_room = room_var.get()

        if not all([name, dob, address, email, number, parent_name, parent_number, selected_room]):
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        # Validation for DOB, Entry Date, Paid Till (YYYY-MM-DD format)
        date_pattern = r'^\d{4}-\d{2}-\d{2}$'
        try:
            for date_field, field_name in [(dob, "Date of Birth"), (entry_date, "Entry Date"), (paid_till, "Paid Till")]:
                if not re.match(date_pattern, date_field) or not datetime.strptime(date_field, "%Y-%m-%d"):
                    messagebox.showerror("Error", f"Invalid {field_name} format! Use YYYY-MM-DD (e.g., 2000-01-01)")
                    return
        except ValueError:
            messagebox.showerror("Error", "Invalid date! Ensure dates are valid and in YYYY-MM-DD format.")
            return

        # Email format validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            messagebox.showerror("Error", "Invalid email format! Use: example@domain.com")
            return

        # Phone number and parent phone number validation (10 digits)
        phone_pattern = r'^\d{10}$'
        if not re.match(phone_pattern, number):
            messagebox.showerror("Error", "Invalid phone number! Must be 10 digits (e.g., 1234567890)")
            return
        if not re.match(phone_pattern, parent_number):
            messagebox.showerror("Error", "Invalid parent phone number! Must be 10 digits (e.g., 1234567890)")
            return

        room_number = int(selected_room.split()[1])

        conn = sqlite3.connect("new.db")
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO student (user_id, name, dob, address, email, number, parent_name, parent_number,
                 entry_date, paid_till, room_number)VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                 (user_id, name, dob, address, email, number, parent_name,
                  parent_number, entry_date, paid_till, room_number))
            cursor.execute("UPDATE room SET occupied = occupied + 1 WHERE room_no = ? AND user_id = ?", 
            (room_number, user_id))
            conn.commit()
            messagebox.showinfo("Success", "Student added successfully!")
            addStudent.destroy()
            admin_dashboard(user_id)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")
            conn.rollback()
        finally:
            conn.close()

    tk.Label(addStudent, text="Add Student", font=("Arial", 24, "bold"), bg="#F0F0F0").pack(pady=20)
    labels = ["Name", "Date of Birth (YYYY-MM-DD)", "Address", "Email", "Phone Number","Parent Name", "Parent Number", "Entry Date (YYYY-MM-DD)", "Paid Till (YYYY-MM-DD)"]
    entries = {}
    for label in labels:
        tk.Label(addStudent, text=label, font=("Arial", 12), bg="#F0F0F0").pack()
        entry = tk.Entry(addStudent, font=("Arial", 12))
        entry.pack(pady=2)
        entries[label] = entry
    tk.Label(addStudent, text="Select Room", font=("Arial", 12), bg="#F0F0F0").pack()
    rooms = fetch_rooms()
    room_var = tk.StringVar()
    room_dropdown = ttk.Combobox(addStudent, textvariable=room_var, values=[f"Room {r[1]}" for r in rooms], 
    state="readonly")
    room_dropdown.pack(pady=5)
    tk.Button(addStudent, text="Submit", font=("Arial", 14), bg="#4CAF50", 
    fg="white", command=submit).pack(pady=10)

def room(user_id):
    room_win = tk.Toplevel()
    room_win.title("Room Details")
    room_win.geometry("1000x600")
    room_win.configure(bg="#f0f0f0")
    room_win.iconbitmap("abc.ico")
    room_win.attributes('-fullscreen', True)

    back_button = tk.Label(room_win, text="←", font=("Arial", 10), 
    bg="#f0f0f0", fg="black", cursor="hand2")
    back_button.place(x=10, y=10)  
    back_button.bind("<Button-1>", lambda e: [room_win.destroy(), admin_dashboard(user_id)]) 

    welcome_label = tk.Label(room_win, text="Room Details", font=("Arial", 24, "bold"),
     bg="#F0F0F0", fg="black")
    welcome_label.pack(pady=20)

    table_frame = tk.Frame(room_win, bg="#f0f0f0")
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    columns = ("Room no", "Capacity", "Occupied", "Beds Left", "Students")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
    tree.pack(fill="both", expand=True)

    for col in columns:
        tree.heading(col, text=col)

    tree.column("Room no", width=100)
    tree.column("Capacity", width=100)
    tree.column("Occupied", width=100)
    tree.column("Beds Left", width=100)
    tree.column("Students", width=300)

    def load_rooms():
        conn = sqlite3.connect("new.db")  
        cursor = conn.cursor()

        # Fetch room data
        cursor.execute("SELECT room_no, capacity, occupied FROM room WHERE user_id = ?", (user_id,))
        rooms = cursor.fetchall()

        for room_data in rooms:
            room_no, capacity, occupied = room_data
            beds_left = capacity - occupied

            cursor.execute("SELECT name FROM student WHERE room_number = ?", (room_no,))
            students = cursor.fetchall()
            student_names = ", ".join([student[0] for student in students])
            tree.insert("", "end", values=(room_no, capacity, occupied, beds_left, student_names))
        conn.close()
    
    load_rooms()

    def edit_room():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a room to edit!")
            return

        room_data = tree.item(selected_item, "values")

        edit_win = tk.Toplevel(room_win)
        edit_win.title("Edit Room Details")
        edit_win.geometry("400x300")
        edit_win.configure(bg="#f0f0f0")
        edit_win.iconbitmap("abc.ico") 

        labels = ["Capacity", "Occupied"]
        entries = {}

        for i, label in enumerate(labels):
            tk.Label(edit_win, text=label, font=("Arial", 12), 
            bg="#F0F0F0").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(edit_win, font=("Arial", 12))
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
            entry.insert(0, room_data[i + 1])  
            entries[label] = entry

        def save_edit():
            updated_data = [entries[label].get() for label in labels]
            room_no = room_data[0] 
            try:
                capacity = int(updated_data[0])  
                occupied = int(updated_data[1])  
                if capacity < occupied:
                    messagebox.showerror("Error", "Capacity cannot be less than occupied beds!")
                    return
            except ValueError:
                messagebox.showerror("Error", "Capacity and Occupied must be integers!")
                return

            conn = sqlite3.connect("new.db") 
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE room 
                SET capacity = ?, occupied = ?
                WHERE room_no = ? AND user_id = ?
            """, (capacity, occupied, room_no, user_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Room details updated successfully!")
            edit_win.destroy()
            tree.delete(*tree.get_children())  
            load_rooms()  

        save_button = tk.Button(edit_win, text="Save", font=("Arial", 14), bg="#4CAF50", 
        fg="white", command=save_edit)
        save_button.grid(row=len(labels) + 1, column=0, columnspan=2, pady=10)  

    edit_button = tk.Button(room_win, text="Edit Room", font=("Arial", 14), bg="#4CAF50", 
    fg="white", command=edit_room)
    edit_button.pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap("abc.ico")
    login_page(root)
    root.mainloop()