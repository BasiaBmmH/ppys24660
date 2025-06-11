import customtkinter as ctk
from tkinter import messagebox
from models.database import SessionLocal
from models.player import Player
from models.statistics import Statistics
from utils.crypto import hash_password

class RegisterScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(expand=True, fill="both")
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Rejestracja", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Login")
        self.username_entry.pack(pady=10)
        self.password_entry = ctk.CTkEntry(self, placeholder_text="Hasło", show="*")
        self.password_entry.pack(pady=10)
        ctk.CTkButton(self, text="Zarejestruj się", command=self.register).pack(pady=10)
        ctk.CTkButton(self, text="Powrót do logowania", command=self.go_back).pack(pady=10)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if not username or not password:
            messagebox.showerror("Błąd", "Wprowadź login i hasło")
            return

        session = SessionLocal()
        if session.query(Player).filter_by(username=username).first():
            messagebox.showerror("Błąd", "Użytkownik o takim loginie już istnieje")
            session.close()
            return

        new_player = Player(username=username, password_hash=hash_password(password))
        session.add(new_player)
        session.flush()

        new_stats = Statistics(player=new_player)
        session.add(new_stats)

        session.commit()
        session.close()

        messagebox.showinfo("Sukces", "Zarejestrowano pomyślnie!")
        self.destroy()
        from gui.login_screen import LoginScreen
        LoginScreen(self.master)

    def go_back(self):
        self.destroy()
        from gui.login_screen import LoginScreen
        LoginScreen(self.master)
