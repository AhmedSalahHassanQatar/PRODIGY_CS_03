# PRODIGY_CS_03
### Password Strength Checker Tool
This tool is a simple Python application built with the Kivy framework. Although Kivy is typically used for mobile development, it has been tailored here for Windows users. The tool evaluates a password’s strength based on its length, the use of uppercase and lowercase letters, the presence of numbers, and special characters. Additionally, it provides feedback on how strong the password is and offers suggestions for stronger alternatives.

How the Password Strength Checker Tool Was Built
1. Setting Up the Development Environment
Before starting to build the tool, the following software is needed:

Python 3.6+: Python is the core language for this project. If you don't have it installed, you can download it from python.org.

Kivy: Kivy is a Python framework used to create graphical user interfaces (GUIs). Although it is primarily used for mobile apps, Kivy also works on Windows. You can install Kivy using the command:

pip install kivy

### 2. Creating the Python Script
The core logic of the password checker is implemented in a Python file, password_checker.py. This script includes:

Password Strength Checker: This function checks the password for length, uppercase/lowercase letters, numbers, and special characters.

Suggestions: If a password fails to meet the strength requirements, the tool suggests ways to improve it.

Graphical Interface (GUI): A simple interface is built using Kivy that includes:

A text input field for the user to enter their password.

A button to suggest a stronger password.

A display area showing the feedback on the password’s strength.

### 3. Password Strength Function
The password strength function checks whether the password meets several criteria. Based on the evaluation, it provides feedback:

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
### 4. Building the GUI with Kivy
Next, we set up the graphical interface using Kivy. This allows users to input their password and see the results immediately. The interface includes:

A title for the tool.

A password input field for users to enter their password.

A label to display the password strength result.

A progress bar to visually indicate the password strength.

Buttons for suggesting a strong password, toggling password visibility, and clearing the input.

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
### 5. Running the Tool
To run the application, simply execute the following command in your terminal or command prompt:

python password_checker.py
The GUI will open, allowing you to input a password and see the results immediately.

### 6. Using the Tool
1.Input a Password: Type the password you want to check.

2.Password Strength Feedback: The tool will automatically evaluate your password’s strength and display feedback.

3.Generate a Strong Password: Click on the "Suggest a Strong Password" button to generate a random, secure password.

4.Toggle Password Visibility: Use the "Show Password" or "Hide Password" button to reveal or hide the password.

5.Clear the Input: Press the "Clear" button to reset the input and feedback.

### 7. Possible Future Improvements
Integrate a password history feature to compare against common weak passwords.

Allow the user to save or copy the suggested strong passwords.



