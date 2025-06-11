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
        self.used_letters = set()
        self.score = 0  # Dodane: punkty
        self.max_attempts = 11
        self.remaining_attempts = self.max_attempts

        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Wisielec – zgadnij hasło!", font=ctk.CTkFont(size=20)).pack(pady=10)

        self.word_label = ctk.CTkLabel(self, text=self.masked_word(), font=ctk.CTkFont(size=24))
        self.word_label.pack(pady=10)

        self.attempts_label = ctk.CTkLabel(self, text=f"Pozostałe próby: {self.remaining_attempts}")
        self.attempts_label.pack(pady=5)

        self.used_letters_label = ctk.CTkLabel(self, text="Użyte litery: ")
        self.used_letters_label.pack(pady=5)

        self.score_label = ctk.CTkLabel(self, text=f"Punkty: {self.score}")
        self.score_label.pack(pady=5)

        self.entry = ctk.CTkEntry(self)
        self.entry.pack(pady=5)

        ctk.CTkButton(self, text="Zgadnij literę", command=self.guess_letter).pack(pady=5)

        self.status = ctk.CTkLabel(self, text="")
        self.status.pack(pady=10)

        ctk.CTkButton(self, text="Powrót", command=self.go_back).pack(pady=10)

    def masked_word(self):
        return " ".join([l if l in self.guessed or l == " " else "_" for l in self.word])

    def guess_letter(self):
        letter = self.entry.get().upper()
        self.entry.delete(0, "end")

        if not letter or len(letter) != 1 or not letter.isalpha():
            self.status.configure(text="Wprowadź jedną literę.")
            return

        if letter in self.used_letters:
            self.status.configure(text="Już użyłeś tej litery.")
            return

        self.used_letters.add(letter)

        if letter in self.word:
            self.guessed.add(letter)
            self.score += 10  # +10 pkt
            self.status.configure(text=f"Dobrze! Litera '{letter}' występuje w haśle.")
            play_sound(SOUNDS["correct"])
        else:
            self.remaining_attempts -= 1
            self.score -= 1  # -1 pkt
            self.status.configure(text=f"Źle! Litery '{letter}' nie ma w haśle.")
            play_sound(SOUNDS["wrong"])

        self.word_label.configure(text=self.masked_word())
        self.attempts_label.configure(text=f"Pozostałe próby: {self.remaining_attempts}")
        self.used_letters_label.configure(text="Użyte litery: " + ", ".join(sorted(self.used_letters)))
        self.score_label.configure(text=f"Punkty: {self.score}")

        if all(l in self.guessed or l == " " for l in self.word):
            play_sound(SOUNDS["win"])
            self.score += 10  # +10 pkt za całe hasło
            self.status.configure(text=f"Gratulacje! Odgadłeś hasło: {self.word}")
            self.entry.configure(state="disabled")
            self.update_statistics(won=True)
        elif self.remaining_attempts <= 0:
            self.status.configure(text=f"Przegrałeś! Hasło to: {self.word}")
            self.entry.configure(state="disabled")
            self.update_statistics(won=False)

    def update_statistics(self, won):
        session = SessionLocal()
        user = session.query(player.Player).filter_by(username=self.username).first()

        if user:
            if won:
                user.games_won += 1
            user.games_played += 1
            user.total_score += self.score
            session.commit()

        session.close()

    def go_back(self):
        self.destroy()
        MainMenu(self.master, self.username)
