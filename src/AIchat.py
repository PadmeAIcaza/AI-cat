import time
import tkinter as tk
from queue import Empty, Queue
from threading import Thread
from tkinter import messagebox
from PIL import Image, ImageTk
from ai import GeminiAI


class AI:
    def __init__(self, window, cat):
        self.window = window
        self.cat = cat
        self.chat_window = None
        self.gemini = None
        self.result_queue = Queue()

    def open_chat(self, _):
        bg = "#E05454"
        if self.chat_window is not None and self.chat_window.winfo_exists():
            self.chat_window.lift()
            return

        self.chat_window = tk.Toplevel(self.window)
        self.chat_window.title("Talk With Me!")
        self.chat_window.overrideredirect(True)
        self.chat_window.attributes("-topmost", True)
        transparent_color = "magenta"
        self.chat_window.configure(bg=transparent_color)
        self.chat_window.attributes("-transparentcolor", transparent_color)

        x = self.chat_window.winfo_screenwidth() - 500
        self.chat_window.geometry(f"500x500+{x}+64")

        chat_bg = Image.open("../assets/chat.png").resize(
            (500, 500), Image.Resampling.LANCZOS
        )
        self.chat_bg = ImageTk.PhotoImage(chat_bg)
        tk.Label(
            self.chat_window, image=self.chat_bg, bg=transparent_color
        ).place(x=0, y=0)

        response_text = tk.Text(
            self.chat_window,
            width=43,
            height=10,
            wrap=tk.WORD,
            font=("Times New Roman", 10),
            bd=0,
            bg="#F7D7C4",
        )
        response_text.place(x=100, y=75)
        response_text.insert(tk.END, "Hi! 🐱 What can I help you with?")
        response_text.configure(state=tk.DISABLED)

        chat_entry = tk.Entry(
            self.chat_window, width=50, font=("Times New Roman", 10)
        )
        chat_entry.place(x=115, y=270)

        def show_response(text):
            response_text.configure(state=tk.NORMAL)
            response_text.delete("1.0", tk.END)
            response_text.insert(tk.END, text)
            response_text.configure(state=tk.DISABLED)

        def request_finished(answer=None, error=None):
            if not self.chat_window or not self.chat_window.winfo_exists():
                return
            save_button.configure(state=tk.NORMAL)
            chat_entry.configure(state=tk.NORMAL)
            self.cat.state = "idle"
            self.cat.change_animation("idle")
            self.cat.last_interaction = time.time()
            if error:
                show_response(f"Sorry, I couldn't answer.\n\n{error}")
            else:
                show_response(answer)
            chat_entry.focus_set()

        def ask_gemini(prompt):
            try:
                if self.gemini is None:
                    self.gemini = GeminiAI()
                answer = self.gemini.ask(prompt)
                self.result_queue.put((answer, None))
            except Exception as exc:
                self.result_queue.put((None, str(exc)))

        def check_for_result():
            try:
                answer, error = self.result_queue.get_nowait()
            except Empty:
                if self.chat_window and self.chat_window.winfo_exists():
                    self.cat.last_interaction = time.time()
                    self.chat_window.after(100, check_for_result)
                return
            request_finished(answer, error)

        def save_button_pressed():
            chat_text = chat_entry.get().strip()
            if not chat_text:
                messagebox.showerror(
                    title="Empty Fields", message="Please enter a message"
                )
                return

            chat_entry.delete(0, tk.END)
            chat_entry.configure(state=tk.DISABLED)
            save_button.configure(state=tk.DISABLED)
            show_response("Thinking…")
            self.cat.state = "talk"
            self.cat.change_animation("talk")
            self.cat.last_interaction = time.time()
            Thread(
                target=ask_gemini, args=(chat_text,), daemon=True
            ).start()
            self.chat_window.after(100, check_for_result)

        button_image = Image.open("../assets/button.png").resize(
            (50, 20), Image.Resampling.LANCZOS
        )
        self.button = ImageTk.PhotoImage(button_image)
        save_button = tk.Button(
            self.chat_window,
            image=self.button,
            text="Talk",
            compound="center",
            fg="black",
            font=("Times New Roman", 10, "bold"),
            bd=0,
            highlightthickness=0,
            bg=bg,
            activebackground=bg,
            command=save_button_pressed,
        )
        save_button.place(x=240, y=300)
        chat_entry.bind("<Return>", lambda _event: save_button_pressed())
        chat_entry.focus_set()
