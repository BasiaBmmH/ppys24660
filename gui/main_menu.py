import customtkinter as ctk

class MainMenu(ctk.CTkFrame):
    def __init__(self, master, username):
        super().__init__(master)
        self.master = master
        self.username = username
        self.pack(expand=True, fill="both")
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text=f"Witaj, {self.username}", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=20)
        ctk.CTkButton(self, text="Nowa gra", command=self.show_settings).pack(pady=10)
        ctk.CTkButton(self, text="Statystyki", command=self.show_stats).pack(pady=10)
        ctk.CTkButton(self, text="Wyloguj", command=self.logout).pack(pady=10)
        ctk.CTkButton(self, text="Graj", command=self.go_to_game).pack(pady=5)
        ctk.CTkButton(self, text="Tryb klasyczny", command=self.start_classic).pack(pady=5)
        ctk.CTkButton(self, text="Tryb na czas", command=self.start_timer_mode).pack(pady=5)

    def go_to_game(self):
        self.destroy()
        from gui.game_screen import GameScreen
        GameScreen(self.master, self.username)

    def show_stats(self):
        self.destroy()
        from gui.stats_screen import StatsScreen
        StatsScreen(self.master, self.username)

    def logout(self):
        self.destroy()
        from gui.login_screen import LoginScreen
        LoginScreen(self.master)

    def start_classic(self):
        self.destroy()
        from gui.game_screen import GameScreen
        GameScreen(self.master, self.username, mode="classic")

    def start_timer_mode(self):
        self.destroy()
        from gui.game_screen import GameScreen
        GameScreen(self.master, self.username, mode="timer")

    def show_settings(self):
        self.destroy()
        from gui.game_settings import GameSettingsScreen
        GameSettingsScreen(self.master, self.username)
