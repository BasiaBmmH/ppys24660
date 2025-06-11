import customtkinter as ctk
import random
import threading
import time
from playsound import playsound
from gui.main_menu import MainMenu
from models.database import SessionLocal
from models import player
from models.game_stats import GameStats
from models.category import Category
from models.word import Word

SOUNDS = {
    "correct": "assets/sounds/correct.wav",
    "wrong": "assets/sounds/wrong.wav",
    "win": "assets/sounds/win.wav"
}

def play_sound(path):
    threading.Thread(target=playsound, args=(path,), daemon=True).start()

class GameScreen(ctk.CTkFrame):
    def __init__(self, master, username, mode="classic", time_limit=None, category_name=None):
        super().__init__(master)
        self.master = master
        self.username = username
        self.mode = mode
        self.time_limit = time_limit
        self.category_name = category_name
        self.pack(expand=True, fill="both")

        self.word = self.get_random_word().upper()
        self.guessed = set()
        self.used_letters = set()
        self.score = 0
        self.max_attempts = 11
        self.remaining_attempts = self.max_attempts
        self.timer_thread = None
        self.remaining_time = self.time_limit

        self.create_widgets()

        if self.mode == "timer":
            self.start_timer()

    def get_random_word(self):
        session = SessionLocal()
        word = "PYTHON"  # fallback
        if self.category_name:
            category = session.query(Category).filter_by(name=self.category_name).first()
            if category and category.words:
                word = random.choice(category.words).word
        session.close()
        return word

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

        if self.mode == "timer":
            self.timer_label = ctk.CTkLabel(self, text=f"Pozostały czas: {self.remaining_time} s")
            self.timer_label.pack(pady=5)

        self.entry = ctk.CTkEntry(self)
        self.entry.pack(pady=5)

        ctk.CTkButton(self, text="Zgadnij literę", command=self.guess_letter).pack(pady=5)

        self.status = ctk.CTkLabel(self, text="")
        self.status.pack(pady=10)

        ctk.CTkButton(self, text="Powrót", command=self.go_back).pack(pady=10)

    def start_timer(self):
        def countdown():
            while self.remaining_time > 0:
                time.sleep(1)
                self.remaining_time -= 1
                self.timer_label.configure(text=f"Pozostały czas: {self.remaining_time} s")
            if not self.is_game_over():
                self.status.configure(text="Czas minął! Koniec gry.")
                self.entry.configure(state="disabled")
                self.update_statistics(won=False)

        self.timer_thread = threading.Thread(target=countdown, daemon=True)
        self.timer_thread.start()

    def masked_word(self):
        return " ".join([l if l in self.guessed or l == " " else "_" for l in self.word])

    def guess_letter(self):
        if self.is_game_over():
            return

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
            self.score += 10
            self.status.configure(text=f"Dobrze! Litera '{letter}' występuje w haśle.")
            play_sound(SOUNDS["correct"])
        else:
            self.remaining_attempts -= 1
            self.score -= 1
            self.status.configure(text=f"Źle! Litery '{letter}' nie ma w haśle.")
            play_sound(SOUNDS["wrong"])

        self.word_label.configure(text=self.masked_word())
        self.attempts_label.configure(text=f"Pozostałe próby: {self.remaining_attempts}")
        self.used_letters_label.configure(text="Użyte litery: " + ", ".join(sorted(self.used_letters)))
        self.score_label.configure(text=f"Punkty: {self.score}")

        if all(l in self.guessed or l == " " for l in self.word):
            play_sound(SOUNDS["win"])
            self.score += 10
            self.status.configure(text=f"Gratulacje! Odgadłeś hasło: {self.word}")
            self.entry.configure(state="disabled")
            self.update_statistics(won=True)
        elif self.remaining_attempts <= 0:
            self.status.configure(text=f"Przegrałeś! Hasło to: {self.word}")
            self.entry.configure(state="disabled")
            self.update_statistics(won=False)

    def is_game_over(self):
        return self.entry.cget("state") == "disabled"

    def update_statistics(self, won):
        if self.is_game_over():
            return

        session = SessionLocal()

        correct_guesses = len([l for l in self.guessed if l.isalpha()])
        wrong_guesses = self.max_attempts - self.remaining_attempts
        score = correct_guesses * 10 - wrong_guesses
        if won:
            score += 10
            result = "win"
        else:
            result = "loss"

        player_instance = session.query(player.Player).filter_by(username=self.username).first()
        if player_instance:
            game_stat = GameStats(player_id=player_instance.id, score=score, result=result)
            session.add(game_stat)
            session.commit()

        session.close()

    def go_back(self):
        self.destroy()
        MainMenu(self.master, self.username)
