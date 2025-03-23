import re
import random
import string
import os
import sys
from functools import partial
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.switch import Switch
from PIL import Image as PILImage

# Function to check password strength
def check_password_strength(password):
    strength_score = 0
    feedback = []

    if len(password) >= 8:
        strength_score += 1
    else:
        feedback.append("Password should be at least 8 characters long.")

    if re.search(r"[A-Z]", password):
        strength_score += 1
    else:
        feedback.append("Password should contain at least one uppercase letter.")

    if re.search(r"[a-z]", password):
        strength_score += 1
    else:
        feedback.append("Password should contain at least one lowercase letter.")

    if re.search(r"\d", password):
        strength_score += 1
    else:
        feedback.append("Password should contain at least one number.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        strength_score += 1
    else:
        feedback.append("Password should contain at least one special character.")

    if strength_score == 5:
        return "Strong password ✅", [0, 1, 0], feedback  # Green color
    elif strength_score >= 3:
        return "Medium password ⚠️\n" + "\n".join(feedback), [1, 0.5, 0], feedback  # Orange color
    else:
        return "Weak password ❌\n" + "\n".join(feedback), [1, 0, 0], feedback  # Red color

# Suggest a strong random password
def suggest_password(password_entry, result_label, password_strength_line, *args):
    length = 12
    all_characters = string.ascii_letters + string.digits + string.punctuation
    suggested_password = ''.join(random.choice(all_characters) for _ in range(length))
    password_entry.text = suggested_password
    evaluate_password(password_entry, result_label, password_strength_line)

# Evaluate password strength
def evaluate_password(password_entry, result_label, password_strength_line, *args):
    password = password_entry.text
    result, color, _ = check_password_strength(password)
    result_label.text = result

    # Update strength line
    if password_strength_line:
        password_strength_line.canvas.clear()
        with password_strength_line.canvas:
            Color(*color)
            Rectangle(size=(password_strength_line.width, password_strength_line.height), pos=password_strength_line.pos)

# Toggle password visibility
def toggle_password_visibility(password_entry, toggle_button):
    if password_entry.password:
        password_entry.password = False
        toggle_button.text = "Hide Password"
    else:
        password_entry.password = True
        toggle_button.text = "Show Password"

# Clear input
def clear_input(password_entry, result_label, password_strength_line):
    password_entry.text = ""
    result_label.text = ""
    password_strength_line.canvas.clear()
    with password_strength_line.canvas:
        Color(0.5, 0.5, 0.5)  # Reset to gray
        Rectangle(size=(password_strength_line.width, password_strength_line.height), pos=password_strength_line.pos)

# Get the correct path for images
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Custom Widget for Password Strength Indicator
class PasswordStrengthLine(Widget):
    def __init__(self, **kwargs):
        super(PasswordStrengthLine, self).__init__(**kwargs)
        self.color = [0.5, 0.5, 0.5]

    def on_size(self, *args):
        if self.canvas:
            self.canvas.clear()
            with self.canvas:
                Color(1, 0, 0, 1)  # Example: Red color
                self.rect = Rectangle(size=self.size, pos=self.pos)

class PasswordCheckerApp(App):
    def build(self):
        root = BoxLayout(orientation="vertical", padding=10, spacing=10, size_hint_y=None)
        root.bind(minimum_height=root.setter('height'))  # Ensure proper layout height

        # Title Label (Higher Placement)
        title_label = Label(
            text="Ahmed Qatar Password Checker",
            font_size=28,  # Increased font size
            size_hint_y=0.2,  # Adjusted to push everything lower
            bold=True
        )
        root.add_widget(title_label)

        # Image (Higher Placement)
        try:
            img = PILImage.open(resource_path("Password Checker.png"))
            img = img.resize((150, 150))  # Adjusted image size
            img.save("temp_image.png")
            img_widget = Image(source="temp_image.png", size_hint=(None, None), size=(200, 200))
            root.add_widget(img_widget)
        except Exception as e:
            print(f"Error loading image: {e}")

        # Password Entry Field
        password_entry = TextInput(password=True, multiline=False, size_hint_y=None, height=50)
        root.add_widget(password_entry)

        # Result Label
        global result_label
        result_label = Label(text="", font_size=16, size_hint_y=None, height=40)
        root.add_widget(result_label)

        # Password Strength Line
        global password_strength_line
        password_strength_line = PasswordStrengthLine(size_hint_y=None, height=10)
        root.add_widget(password_strength_line)

        # Bind password entry field to evaluation function
        password_entry.bind(text=partial(evaluate_password, password_entry, result_label, password_strength_line))

        # Suggest Password Button
        suggest_button = Button(text="Suggest a Strong Password", size_hint_y=None, height=50)
        suggest_button.bind(on_press=partial(suggest_password, password_entry, result_label, password_strength_line))
        root.add_widget(suggest_button)

        # Toggle Password Visibility Button
        toggle_button = Button(text="Show Password", size_hint_y=None, height=50)
        toggle_button.bind(on_press=lambda x: toggle_password_visibility(password_entry, toggle_button))
        root.add_widget(toggle_button)

        # Clear Button
        clear_button = Button(text="Clear", size_hint_y=None, height=50)
        clear_button.bind(on_press=lambda x: clear_input(password_entry, result_label, password_strength_line))
        root.add_widget(clear_button)

        return root

if __name__ == "__main__":
    PasswordCheckerApp().run()
