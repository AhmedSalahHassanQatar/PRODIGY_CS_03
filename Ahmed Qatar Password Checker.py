import re
import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import random
import string
import os
import sys

# Function to check password strength
def check_password_strength(password):
    strength_score = 0
    feedback = []
    
    # Check length
    if len(password) >= 8:
        strength_score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")
    
    # Check uppercase letters
    if re.search(r"[A-Z]", password):
        strength_score += 1
    else:
        feedback.append("Password should contain at least one uppercase letter.")
    
    # Check lowercase letters
    if re.search(r"[a-z]", password):
        strength_score += 1
    else:
        feedback.append("Password should contain at least one lowercase letter.")
    
    # Check numbers
    if re.search(r"\d", password):
        strength_score += 1
    else:
        feedback.append("Password should contain at least one number.")
    
    # Check special characters
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        strength_score += 1
    else:
        feedback.append("Password should contain at least one special character.")
    
    # Determine strength level
    if strength_score == 5:
        return "Strong password ✅", "green", feedback
    elif strength_score >= 3:
        return "Medium password ⚠️" + "\n" + "\n".join(feedback), "orange", feedback
    else:
        return "Weak password ❌" + "\n" + "\n".join(feedback), "red", feedback

# Function to suggest a strong random password
def suggest_password():
    length = 12  # Default length for a strong password
    all_characters = string.ascii_letters + string.digits + string.punctuation
    suggested_password = ''.join(random.choice(all_characters) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, suggested_password)
    evaluate_password()  # Re-evaluate password strength after suggestion

# Evaluate the password as the user types
def evaluate_password(event=None):
    password = password_entry.get()
    result, color, feedback = check_password_strength(password)
    result_label.config(text=result, fg=color)  # Change text color based on strength
    strength_line.config(bg=color)  # Change the line color to indicate strength

# Toggle password visibility
def toggle_password_visibility():
    if password_entry.cget("show") == "*":
        password_entry.config(show="")
        toggle_button.config(text="Hide Password")
    else:
        password_entry.config(show="*")
        toggle_button.config(text="Show Password")

# Clear the input and result label
def clear_input():
    password_entry.delete(0, tk.END)
    result_label.config(text="", fg="black")
    strength_line.config(bg="gray")  # Reset line to neutral color

# Get the correct path for the image, depending on whether we're running as a script or executable
def resource_path(relative_path):
    try:
        # PyInstaller creates a temporary folder to store files, and this gets the path to the correct directory
        base_path = sys._MEIPASS
    except Exception:
        # If running normally (not as an executable), return the relative path
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Create GUI Window
root = tk.Tk()
root.title("Ahmed Qatar Password Checker")
root.geometry("400x600")  # Adjust the size of the window if needed

# Title Label
title_label = tk.Label(root, text="Ahmed Qatar Password Checker", font=("Arial", 14, "bold"))
title_label.pack(pady=10)  # Add some padding to give space

# Load Image with Pillow
try:
    img = Image.open(resource_path("Password Checker.png"))  # Use the correct path for the image
    img = img.resize((100, 100))  # Resize if necessary
    img = ImageTk.PhotoImage(img)
    img_label = tk.Label(root, image=img)
    img_label.pack(pady=10)  # Add padding below the image for space
except Exception as e:
    print(f"Error loading image: {e}")

# Create Input Field and Bind to Key Release Event
password_label = tk.Label(root, text="Enter Password:")
password_label.pack()

password_entry = tk.Entry(root, show="*", width=30)
password_entry.pack(pady=10)

# Bind the key release event to evaluate the password strength as the user types
password_entry.bind("<KeyRelease>", evaluate_password)

# Create a Label to Display Result
result_label = tk.Label(root, text="", font=("Arial", 12))
result_label.pack(pady=10)  # Add some padding for spacing

# Create a Line (Frame) to Indicate Password Strength
strength_line = tk.Frame(root, height=10, bg="gray", width=350)
strength_line.pack(pady=5)

# Add a Button to Toggle Password Visibility
toggle_button = tk.Button(root, text="Show Password", command=toggle_password_visibility)
toggle_button.pack(pady=5)

# Add a Clear Button to Reset the Input and Result
clear_button = tk.Button(root, text="Clear", command=clear_input)
clear_button.pack(pady=5)

# Add a Suggest Password Button
suggest_button = tk.Button(root, text="Suggest a Strong Password", command=suggest_password)
suggest_button.pack(pady=5)

# Run GUI
root.mainloop()
