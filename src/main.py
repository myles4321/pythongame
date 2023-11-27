"""
This is the main file that is used to start the game.
"""
import tkinter as tk
import json
from tkinter import messagebox
from game_logic.game_logic import play

class MainMenu(tk.Tk):
    def __init__(self, current_user):
        super().__init__()

        self.title("Game Main Menu")
        self.geometry("300x150")

        self.label_welcome = tk.Label(self, text=f"Welcome, {current_user}!")
        self.label_welcome.pack(pady=10)

        self.button_play = tk.Button(self, text="Play", command=lambda: self.play_game(current_user))
        self.button_play.pack(pady=5)

        self.button_logout = tk.Button(self, text="Logout", command=self.logout)
        self.button_logout.pack(pady=5)

    def play_game(self, current_user):
        # Call the play function from game_logic module
        play(current_user)

    def logout(self):
        self.destroy()

class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Game Login")
        self.geometry("300x150")

        self.label_username = tk.Label(self, text="Username:")
        self.label_password = tk.Label(self, text="Password:")

        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")

        self.button_login = tk.Button(self, text="Login", command=self.login)
        self.button_register = tk.Button(self, text="Register", command=self.register)

        self.label_username.pack(pady=5)
        self.entry_username.pack(pady=5)
        self.label_password.pack(pady=5)
        self.entry_password.pack(pady=5)
        self.button_login.pack(side=tk.LEFT, padx=5)
        self.button_register.pack(side=tk.LEFT, padx=5)

        # Load user credentials from a file or initialize an empty dictionary
        self.user_credentials = self.load_credentials()
        self.current_user = None  # Track the currently logged-in user

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Check if the username exists and the password is correct
        if username in self.user_credentials and self.user_credentials[username] == password:
            print("Login successful!")
            self.current_user = username  # Set the current user
            self.destroy()  # Close the login window
            self.show_main_menu()
        else:
            print("Invalid username or password. Please try again.")

    def register(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Check if the username already exists
        if username in self.user_credentials:
            print("Username already exists. Please choose another.")
        else:
            # Register the new user
            self.user_credentials[username] = password
            print("Registration successful!")
            self.save_credentials()  # Save the updated credentials to the file
            self.clear_entries()  # Clear the entry fields after registration

    def clear_entries(self):
        # Clear the entry fields
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

    def load_credentials(self):
        try:
            with open("user_credentials.json", "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_credentials(self):
        with open("user_credentials.json", "w") as file:
            json.dump(self.user_credentials, file)

    def show_main_menu(self):
        # Create and show the main menu window
        main_menu_window = MainMenu(self.current_user)
        main_menu_window.mainloop()

if __name__ == "__main__":
    login_page = LoginPage()
    login_page.mainloop()



# if __name__ == "__main__":
#     main_menu()
