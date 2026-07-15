import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class AI:
    def __init__(self, window):
        self.window = window
        self.chat_window = None

    def open_chat(self, _):
        BG = '#B34A44'
        self.chat_window = tk.Toplevel(self.window)
        self.chat_window.configure(bg=BG)
        self.chat_window.title('Talk With Me!')
        self.chat_window.geometry('220x180')