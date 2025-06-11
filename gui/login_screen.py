import customtkinter as ctk
from tkinter import messagebox
from models.database import SessionLocal
from models.player import Player
from utils.crypto import verify_password

class LoginScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(expand=True, fill="both")
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Logowanie", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Login")
        self.username_entry.pack(pady=10)
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Hasło", show="*")
        self.password_entry.pack(pady=10)
        ctk.CTkButton(self, text="Zaloguj", command=self.login).pack(pady=10)
        ctk.CTkButton(self, text="Zarejestruj się", command=self.register).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Błąd", "Wprowadź login i hasło")
            return

        session = SessionLocal()
        user = session.query(Player).filter_by(username=username).first()
        session.close()

        if not user or not verify_password(password, user.password_hash):
            messagebox.showerror("Błąd", "Niepoprawny login lub hasło")
            return

        messagebox.showinfo("Sukces", f"Witaj, {username}!")
        self.destroy()
        from gui.main_menu import MainMenu
        MainMenu(self.master, username)

    def register(self):
        self.destroy()
        from gui.register_screen import RegisterScreen
        RegisterScreen(self.master)
