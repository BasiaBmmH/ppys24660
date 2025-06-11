import customtkinter as ctk
from models.database import SessionLocal
from models import player, statistics

class StatsScreen(ctk.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master)
        self.master = master
        self.username = username
        self.pack(expand=True, fill="both")
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text=f"Statystyki gracza: {self.username}", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)

        session = SessionLocal()
        user = session.query(player.Player).filter_by(username=self.username).first()
        stats = user.statistics

        if stats:
            ctk.CTkLabel(self, text=f"Liczba gier: {stats.games_played}").pack(pady=5)
            ctk.CTkLabel(self, text=f"Wygrane gry: {stats.games_won}").pack(pady=5)
            ctk.CTkLabel(self, text=f"Punkty: {stats.points}").pack(pady=5)
        else:
            ctk.CTkLabel(self, text="Brak danych statystycznych.").pack(pady=5)

        session.close()
        ctk.CTkButton(self, text="Powrót", command=self.go_back).pack(pady=10)

    def go_back(self):
        self.destroy()
        from gui.main_menu import MainMenu
        MainMenu(self.master, self.username)
