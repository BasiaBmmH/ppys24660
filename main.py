from customtkinter import CTk
from gui.login_screen import LoginScreen
from models.database import Base, engine
from models import player, statistics, category, word

Base.metadata.create_all(bind=engine)

app = CTk()
app.geometry("400x400")
LoginScreen(app)
app.mainloop()
