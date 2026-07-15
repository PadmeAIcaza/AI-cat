import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class AI:
    def __init__(self, window, cat):
        self.window = window
        self.cat = cat
        self.chat_window = None

    def open_chat(self, _):
        BG = '#E05454'
        if self.chat_window is not None and self.chst_window.winfo_exists():
            self.chat_window.lift()
            return
        self.chat_window = tk.Toplevel(self.window)
        self.chat_window.title("Talk With Me!")
        self.chat_window.overrideredirect(True)
        self.chat_window.attributes("-topmost", True)
        transparent_color = 'magenta'
        self.chat_window.configure(bg=transparent_color)
        self.chat_window.attributes('-transparentcolor', transparent_color)
        self.chat_window.geometry('220x220')

        self.x = self.chat_window.winfo_screenwidth() - 220
        self.y = 64
        self.chat_window.geometry(f"220x220+{self.x}+{self.y}")

        chat_bg = Image.open("../assets/chat.png").resize((220, 220), Image.Resampling.LANCZOS)
        self.chat_bg = ImageTk.PhotoImage(chat_bg)
        tk.Label(self.chat_window, image= self.chat_bg, text='Hi!🐱 What can I help you with?', font=("Times New Roman", 10), compound="center", bg='magenta').place(x=0, y=0)
        chat_entry = tk.Entry(self.chat_window, width=20, font=("Times New Roman", 10))
        chat_entry.place(x=50, y=130)

        def save_button_pressed():
            chat_text = chat_entry.get().strip()
            if chat_text == '':
                messagebox.showerror(title='Empty Fields', message='Please fill every field')
                return
            elif chat_text:
                print(chat_text)
                chat_entry.delete(0, tk.END)

        button_image = Image.open('../assets/button.png').resize((50, 20), Image.Resampling.LANCZOS)
        self.button = ImageTk.PhotoImage(button_image)
        save_button = tk.Button(self.chat_window, image=self.button, text='Talk', compound='center', fg='black', font=("Times New Roman", 10, "bold"), bd=0, highlightthickness=0, bg=BG, activebackground=BG, command=save_button_pressed)
        save_button.place(x=85, y=160)



