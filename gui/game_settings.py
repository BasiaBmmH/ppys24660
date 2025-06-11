import customtkinter as ctk
from gui.game_screen import GameScreen
from models.database import SessionLocal
from models.category import Category

class GameSettingsScreen(ctk.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master)
        self.master = master
        self.username = username
        self.pack(expand=True, fill="both")

        self.mode_var = ctk.StringVar(value="classic")
        self.time_var = ctk.StringVar(value="30")
        self.category_var = ctk.StringVar()

        self.create_widgets()
        self.load_categories()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Ustawienia Gry", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)
        ctk.CTkLabel(self, text="Tryb gry:").pack()
        ctk.CTkOptionMenu(self, variable=self.mode_var, values=["classic", "timer"]).pack(pady=5)

        ctk.CTkLabel(self, text="Czas (sekundy):").pack()
        ctk.CTkEntry(self, textvariable=self.time_var).pack(pady=5)

        ctk.CTkLabel(self, text="Kategoria:").pack()
        self.category_menu = ctk.CTkOptionMenu(self, variable=self.category_var, values=[])
        self.category_menu.pack(pady=5)

        ctk.CTkButton(self, text="Rozpocznij grę", command=self.start_game).pack(pady=20)
        ctk.CTkButton(self, text="Powrót", command=self.go_back).pack()

    def load_categories(self):
        session = SessionLocal()
        categories = session.query(Category).all()
        session.close()
        if categories:
            category_names = [cat.name for cat in categories]
            self.category_menu.configure(values=category_names)
            self.category_var.set(category_names[0])
        else:
            self.category_menu.configure(values=["Brak kategorii"])
            self.category_var.set("Brak kategorii")

    def start_game(self):
        mode = self.mode_var.get()
        time = int(self.time_var.get()) if mode == "timer" else None
        category = self.category_var.get()
        self.destroy()
        GameScreen(self.master, self.username, mode=mode, time_limit=time, category_name=category)

    def go_back(self):
        self.destroy()
        from gui.main_menu import MainMenu
        MainMenu(self.master, self.username)
