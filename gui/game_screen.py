import customtkinter as ctk
import random
import threading
from playsound import playsound
from gui.main_menu import MainMenu
from models.database import SessionLocal
from models import player

HASLA = ["NORWAY", "PYTHON", "KOSMICZNA ESKAPADA"]
SOUNDS = {
    "correct": "assets/sounds/correct.wav",
    "wrong": "assets/sounds/wrong.wav",
    "win": "assets/sounds/win.wav"
}


def play_sound(path):
    threading.Thread(target=playsound, args=(path,), daemon=True).start()


class GameScreen(ctk.CTkFrame):
    def __init__(self, master, username, mode="classic"):
        super().__init__(master)
        self.master = master
        self.username = username
        self.mode = mode
        self.pack(expand=True, fill="both")

        self.word = random.choice(HASLA).upper()
        self.guessed = set()
        self.tries = 0
        self.score = 0

        self.create_widgets()

        if self.mode == "timer":
            self.remaining_time = 30  # 30 sekund
            self.timer_label = ctk.CTkLabel(self, text=f"Czas: {self.remaining_time} s")
            self.timer_label.pack(pady=5)
            self.update_timer()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Zgadnij hasło!", font=ctk.CTkFont(size=20)).pack(pady=10)
        self.word_label = ctk.CTkLabel(self, text=self.masked_word(), font=ctk.CTkFont(size=24))
        self.word_label.pack(pady=10)

        self.score_label = ctk.CTkLabel(self, text=f"Punkty: {self.score}")
        self.score_label.pack(pady=5)

        self.entry = ctk.CTkEntry(self)
        self.entry.pack(pady=5)
        ctk.CTkButton(self, text="Zakręć kołem i zgadnij literę", command=self.guess_letter).pack(pady=5)

        self.status = ctk.CTkLabel(self, text="")
        self.status.pack(pady=10)

        ctk.CTkButton(self, text="Powrót", command=self.go_back).pack(pady=10)

    def masked_word(self):
        return " ".join([l if l in self.guessed or l == " " else "_" for l in self.word])

    def spin_wheel_animation(self, callback):
        values = [0, 100, 200, 300, 400, 500, 'BANKRUCTWO']
        spins = [random.choice(values) for _ in range(20)] + [random.choice(values)]

        def animate(index=0):
            if index < len(spins):
                result = spins[index]
                self.status.configure(text=f"Koło się kręci... {result}")
                self.after(100 + index * 5, animate, index + 1)
            else:
                final_result = spins[-1]
                if final_result == 'BANKRUCTWO':
                    self.score = 0
                    self.score_label.configure(text=f"Punkty: {self.score}")
                    self.status.configure(text="BANKRUCTWO! Tracisz wszystkie punkty.")
                    callback(0)
                else:
                    self.status.configure(text=f"Koło wylosowało: {final_result} punktów")
                    callback(final_result)

        animate()

    def guess_letter(self):
        letter = self.entry.get().upper()
        self.entry.delete(0, "end")
        if not letter or len(letter) != 1:
            self.status.configure(text="Wpisz jedną literę.")
            return

        def after_spin(points):
            if points == 0:
                return

            self.guessed.add(letter)
            self.tries += 1

            if letter in self.word:
                self.score += points
                self.status.configure(text=f"Dobrze! Zdobywasz {points} punktów.")
                play_sound(SOUNDS["correct"])
            else:
                self.status.configure(text="Zła litera.")
                play_sound(SOUNDS["wrong"])

            self.score_label.configure(text=f"Punkty: {self.score}")
            self.word_label.configure(text=self.masked_word())

            if all(l in self.guessed or l == " " for l in self.word):
                play_sound(SOUNDS["win"])
                self.status.configure(text=f"Brawo! Odgadłeś hasło po {self.tries} próbach! Punkty: {self.score}")
                self.update_statistics(won=True)

        self.spin_wheel_animation(after_spin)

    def update_statistics(self, won=False):
        session = SessionLocal()
        user = session.query(player.Player).filter_by(username=self.username).first()
        if not user.statistics:
            from models.statistics import Statistics
            stat = Statistics(games_played=1, games_won=1 if won else 0, points=self.score, player=user)
            session.add(stat)
        else:
            user.statistics.games_played += 1
            user.statistics.points += self.score
            if won:
                user.statistics.games_won += 1
        session.commit()
        session.close()

    def go_back(self):
        self.destroy()
        MainMenu(self.master, self.username)

    def update_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.timer_label.configure(text=f"Czas: {self.remaining_time} s")
            self.after(1000, self.update_timer)
        else:
            self.end_game_due_to_time()

    def end_game_due_to_time(self):
        self.entry.configure(state="disabled")
        self.status.configure(text=f"Koniec czasu! Zdobyłeś {self.score} punktów.")
        play_sound(SOUNDS["wrong"])
        self.update_statistics(won=False)


