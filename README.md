# PRODIGY_CS_03
Description: This project is a tool built to assess the strength of a password. It evaluates the password based on verity of criteria, The tool provides feedback to the user regarding the password strength and suggests improvements if necessary. Additionally, it generates strong password suggestions and allows users to toggle password visibility.
Password Strength Checker Tool
This is a Python-based tool built using Kivy, which is primarily designed for mobile app development, but it has been adapted here for use on Windows. The tool evaluates the strength of a password by checking its length, presence of uppercase and lowercase letters, numbers, and special characters. It also provides feedback on the password's strength and suggests strong passwords.

Steps to Build the Password Strength Checker Tool
1. Set Up the Development Environment
Before you start building the application, make sure you have the required software:

Python 3.6+: Ensure that you have Python installed on your system. You can download it from python.org.

Kivy: Kivy is a Python framework used to build the graphical user interface (GUI). Kivy is typically used for mobile applications, but it works perfectly on Windows as well. You can install Kivy by running:

bash
Copy
Edit
pip install kivy
2. Create the Main Python File
Create a Python file named password_checker.py. This file will contain all the logic for checking password strength and generating feedback.

In this file, you will:

Define the password strength checker function: This function will evaluate the password by checking:

Length

Presence of uppercase and lowercase letters

Presence of numbers

Presence of special characters

Define the suggest password function: This will suggest a random strong password to the user.

Set up a Kivy graphical interface with:

A text input field for the user to enter their password.

A button to suggest a strong password.

A display area for feedback about the password’s strength.

3. Define the Password Strength Function
The check_password_strength function checks the password's strength based on predefined criteria. If the password is weak, it provides suggestions to make it stronger.

python
Copy
Edit
import re

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
        return "Strong password ✅", [0, 1, 0], feedback
    elif strength_score >= 3:
        return "Medium password ⚠️\n" + "\n".join(feedback), [1, 0.5, 0], feedback
    else:
        return "Weak password ❌\n" + "\n".join(feedback), [1, 0, 0], feedback
4. Build the Graphical User Interface (GUI)
Next, you'll use Kivy to build the interface. Kivy makes it easy to design interactive applications.

The application should have the following components:

A title

An image (optional)

A password input field

A label to display the password strength result

A button to suggest a strong password

A button to toggle password visibility

A clear button to reset the input

python
Copy
Edit
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from functools import partial

class PasswordStrengthLine(Widget):
    def __init__(self, **kwargs):
        super(PasswordStrengthLine, self).__init__(**kwargs)
        self.color = [0.5, 0.5, 0.5]

    def on_size(self, *args):
        if self.canvas:
            self.canvas.clear()
            with self.canvas:
                Color(1, 0, 0, 1)
                self.rect = Rectangle(size=self.size, pos=self.pos)

class PasswordCheckerApp(App):
    def build(self):
        root = BoxLayout(orientation="vertical", padding=10, spacing=10)

        title_label = Label(text="Password Strength Checker", font_size=24, size_hint_y=None, height=40, bold=True)
        root.add_widget(title_label)

        password_entry = TextInput(password=True, multiline=False, size_hint_y=None, height=40)
        root.add_widget(password_entry)

        result_label = Label(text="", font_size=16, size_hint_y=None, height=40)
        root.add_widget(result_label)

        password_strength_line = PasswordStrengthLine(size_hint_y=None, height=10)
        root.add_widget(password_strength_line)

        # Add a button for suggesting strong passwords
        suggest_button = Button(text="Suggest a Strong Password", size_hint_y=None, height=50)
        suggest_button.bind(on_press=partial(self.suggest_password, password_entry, result_label, password_strength_line))
        root.add_widget(suggest_button)

        toggle_button = Button(text="Show Password", size_hint_y=None, height=50)
        toggle_button.bind(on_press=lambda x: self.toggle_password_visibility(password_entry, toggle_button))
        root.add_widget(toggle_button)

        clear_button = Button(text="Clear", size_hint_y=None, height=50)
        clear_button.bind(on_press=lambda x: self.clear_input(password_entry, result_label, password_strength_line))
        root.add_widget(clear_button)

        password_entry.bind(text=partial(self.evaluate_password, password_entry, result_label, password_strength_line))

        return root

    def suggest_password(self, password_entry, result_label, password_strength_line, *args):
        length = 12
        suggested_password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length))
        password_entry.text = suggested_password
        self.evaluate_password(password_entry, result_label, password_strength_line)

    def evaluate_password(self, password_entry, result_label, password_strength_line, *args):
        password = password_entry.text
        result, color, _ = check_password_strength(password)
        result_label.text = result

        password_strength_line.canvas.clear()
        with password_strength_line.canvas:
            Color(*color)
            Rectangle(size=(password_strength_line.width, password_strength_line.height), pos=password_strength_line.pos)

    def toggle_password_visibility(self, password_entry, toggle_button):
        if password_entry.password:
            password_entry.password = False
            toggle_button.text = "Hide Password"
        else:
            password_entry.password = True
            toggle_button.text = "Show Password"

    def clear_input(self, password_entry, result_label, password_strength_line):
        password_entry.text = ""
        result_label.text = ""
        password_strength_line.canvas.clear()

if __name__ == "__main__":
    PasswordCheckerApp().run()
5. Running the Application
Once the code is ready, you can run it from the terminal:

bash
Copy
Edit
python password_checker.py
This will open up the graphical user interface where you can test password strength, view feedback, and suggest strong passwords.

6. How to Use the Tool
Input a Password: Type a password into the password input field.

Check Strength: The tool will automatically evaluate your password's strength.

Suggest a Strong Password: Press the "Suggest a Strong Password" button to generate a random strong password.

Toggle Password Visibility: Use the "Show Password" or "Hide Password" button to reveal or hide the password.

Clear Input: Press the "Clear" button to reset the input and feedback.
