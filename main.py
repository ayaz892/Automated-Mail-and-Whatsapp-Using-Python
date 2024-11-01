import tkinter as tk
from tkinter import simpledialog, messagebox
import subprocess
import os

# File to store user credentials
CREDENTIALS_FILE = "credentials.txt"

# Function to check if credentials are correct
def check_credentials(username, password):
    if not os.path.exists(CREDENTIALS_FILE):
        return False
    with open(CREDENTIALS_FILE, "r") as file:
        for line in file:
            stored_username, stored_password = line.strip().split(",")
            if stored_username == username and stored_password == password:
                return True
    return False

# Function to sign up a new user
def signup():
    username = simpledialog.askstring("Signup", "Enter username:")
    if username is None:
        return None, None
    password = simpledialog.askstring("Signup", "Enter password:", show="*")
    if password is None:
        return None, None
    
    with open(CREDENTIALS_FILE, "a") as file:
        file.write(f"{username},{password}\n")
    
    messagebox.showinfo("Signup", "Signup successful. Please login.")
    return username, password

# Function to login a user
def login():
    username = simpledialog.askstring("Login", "Enter username:")
    if username is None:
        return None, None
    password = simpledialog.askstring("Login", "Enter password:", show="*")
    if password is None:
        return None, None
    
    if check_credentials(username, password):
        return username, password
    else:
        messagebox.showerror("Login", "Invalid credentials. Please try again.")
        return None, None

# Function to authenticate user before performing an action
def authenticate_and_run(action_func):
    action_func_name = action_func.__name__.replace("run_", "").replace("_", " ").title()
    if not os.path.exists(CREDENTIALS_FILE) or os.path.getsize(CREDENTIALS_FILE) == 0:
        messagebox.showinfo("Info", "No users found. Please signup.")
        username, password = signup()
        if username is None:
            return
    else:
        choice = messagebox.askquestion("Authentication", "Do you want to login or signup?", icon='question', type='yesno', default='yes', detail='Yes: Login, No: Signup')
        if choice == "yes":
            username, password = login()
            if username is None:
                return
        else:
            username, password = signup()
            if username is None:
                return
    
    action_func()

def run_bulk_messages():
    result = subprocess.run(["python", "Bulk_msgs.py"])
    if result.returncode == 0:
        messagebox.showinfo("Success", "Bulk messages sent successfully.")
    else:
        messagebox.showerror("Error", "Failed to send bulk messages.")

def run_bulk_email():
    result = subprocess.run(["python", "Bulk_Email.py"])
    if result.returncode == 0:
        messagebox.showinfo("Success", "Bulk emails sent successfully.")
    else:
        messagebox.showerror("Error", "Failed to send bulk emails.")

def run_web_scrap():
    result = subprocess.run(["python", "fbscrapper.py"])
    if result.returncode == 0:
        messagebox.showinfo("Success", "Web scraping completed successfully.")
    else:
        messagebox.showerror("Error", "Failed to complete web scraping.")

# Function to create the main application window
def create_main_window():
    main_window = tk.Toplevel(root)
    main_window.title("Automation App")
    
    # Set background color
    main_window.configure(bg="#f0f0f0")
    
    # Create a frame for better layout
    frame = tk.Frame(main_window, padx=20, pady=20, bg="#f0f0f0")
    frame.pack(expand=True)
    
    # Create labels and buttons with custom colors
    label = tk.Label(frame, text="Select an operation to perform:", font=('Helvetica', 14), bg="#f0f0f0", fg="#333333")
    label.grid(row=0, column=0, columnspan=2, pady=10)
    
    button1 = tk.Button(frame, text="Send Whatsapp Messages", command=lambda: authenticate_and_run(run_bulk_messages), width=25, bg="#4CAF50", fg="white")
    button2 = tk.Button(frame, text="Send Email", command=lambda: authenticate_and_run(run_bulk_email), width=25, bg="#2196F3", fg="white")
    button3 = tk.Button(frame, text="Run Web Scraping", command=lambda: authenticate_and_run(run_web_scrap), width=25, bg="#FFC107", fg="black")
    exit_button = tk.Button(frame, text="Exit", command=root.quit, width=25, bg="#F44336", fg="white")
    
    # Place buttons in a grid
    button1.grid(row=1, column=0, pady=10)
    button2.grid(row=2, column=0, pady=10)
    button3.grid(row=3, column=0, pady=10)
    exit_button.grid(row=4, column=0, pady=10)

# Function to create the initial authentication window
def create_authentication_window():
    auth_window = tk.Toplevel(root)
    auth_window.title("Authentication")
    
    # Set background color
    auth_window.configure(bg="#f0f0f0")
    
    # Create a frame for better layout
    frame = tk.Frame(auth_window, padx=20, pady=20, bg="#f0f0f0")
    frame.pack(expand=True)
    
    # Create labels and buttons with custom colors
    label = tk.Label(frame, text="Welcome! Please Login or Signup:", font=('Helvetica', 14), bg="#f0f0f0", fg="#333333")
    label.grid(row=0, column=0, columnspan=2, pady=10)
    
    login_button = tk.Button(frame, text="Login", command=lambda: authenticate_and_open_main_window(auth_window, "login"), width=25, bg="#2196F3", fg="white")
    signup_button = tk.Button(frame, text="Signup", command=lambda: authenticate_and_open_main_window(auth_window, "signup"), width=25, bg="#4CAF50", fg="white")
    
    # Place buttons in a grid
    login_button.grid(row=1, column=0, pady=10)
    signup_button.grid(row=2, column=0, pady=10)

# Function to authenticate user and open main window
def authenticate_and_open_main_window(auth_window, mode):
    if mode == "login":
        username, password = login()
    else:
        username, password = signup()
    
    if username is not None and password is not None:
        auth_window.destroy()
        create_main_window()

# Create the main root window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Start with the authentication window
create_authentication_window()

# Start the Tkinter event loop
root.mainloop()
