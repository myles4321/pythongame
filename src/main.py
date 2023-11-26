"""
This is the main file that is used to start the game.
"""
import tkinter as tk
from game_logic.game_logic import main_menu

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

        # Initialize an empty dictionary to store user credentials
        self.user_credentials = {}

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Check if the username exists and the password is correct
        if username in self.user_credentials and self.user_credentials[username] == password:
            print("Login successful!")
            self.destroy()  # Close the login window
            main_menu()
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
            self.clear_entries()  # Clear the entry fields after registration

    def clear_entries(self):
        # Clear the entry fields
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

if __name__ == "__main__":
    login_page = LoginPage()
    login_page.mainloop()


# if __name__ == "__main__":
#     main_menu()
