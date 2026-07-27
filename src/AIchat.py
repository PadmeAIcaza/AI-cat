import time
import tkinter as tk
from pathlib import Path
from queue import Empty, Queue
from threading import Thread
from tkinter import messagebox

from PIL import Image, ImageTk

from ai import GeminiAI


WINDOW_WIDTH = 700
WINDOW_HEIGHT = 560
TRANSPARENT = "#ff00ff"
PANEL = "#df5256"
HEADER = "#d84b50"
OUTLINE = "#a92d32"
BUBBLE = "#b8373c"
BUTTON = "#bd3d42"
BUTTON_HOVER = "#a93237"
WHITE = "#fffaf7"
PLACEHOLDER = "Type your message..."


def rounded_rectangle(canvas, x1, y1, x2, y2, radius, **options):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, splinesteps=24, **options)


class AI:
    def __init__(self, window, cat):
        self.window = window
        self.cat = cat
        self.chat_window = None
        self.gemini = None
        self.result_queue = Queue()

    def open_chat(self, _):
        if self.chat_window is not None and self.chat_window.winfo_exists():
            self.chat_window.lift()
            return

        self.chat_window = tk.Toplevel(self.window)
        self.chat_window.title("Talk With Me!")
        self.chat_window.overrideredirect(True)
        self.chat_window.attributes("-topmost", True)
        self.chat_window.configure(bg=TRANSPARENT)
        self.chat_window.attributes("-transparentcolor", TRANSPARENT)

        x = self.chat_window.winfo_screenwidth() - WINDOW_WIDTH - 20
        self.chat_window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{max(0, x)}+40")

        canvas = tk.Canvas(self.chat_window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=TRANSPARENT, bd=0, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        ########################################################### chat design ###########################################################
        # Window shadow and main panel.
        rounded_rectangle(
            canvas, 10, 12, 694, 558, 28, fill="#772024", outline=""
        )
        rounded_rectangle(
            canvas,
            4,
            4,
            690,
            550,
            28,
            fill=PANEL,
            outline=OUTLINE,
            width=2,
        )

        # Header and divider.
        rounded_rectangle(
            canvas, 5, 5, 689, 75, 27, fill=HEADER, outline=""
        )
        canvas.create_rectangle(5, 48, 689, 75, fill=HEADER, outline="")
        canvas.create_line(5, 75, 689, 75, fill="#ae3439", width=2)
        canvas.create_text(
            350,
            40,
            text="Talk With Me!",
            fill=WHITE,
            font=("Georgia", 24, "bold"),
        )

        # Use VoidCat's first sprite frame as the header icon.
        icon_path = Path(__file__).resolve().parent.parent / "assets" / "sprites" / "Born.png"
        icon_sheet = Image.open(icon_path).convert("RGBA")
        icon = icon_sheet.crop((0, 0, 32, 32)).resize(
            (48, 48), Image.Resampling.NEAREST
        )
        self.header_icon = ImageTk.PhotoImage(icon)
        canvas.create_image(50, 40, image=self.header_icon)

        close_id = canvas.create_text(
            655,
            39,
            text="×",
            fill=WHITE,
            font=("Segoe UI", 30),
            tags=("close",),
        )
        canvas.tag_bind(
            close_id, "<Button-1>", lambda _event: self.chat_window.destroy()
        )
        canvas.tag_bind(close_id, "<Enter>", lambda _event: canvas.config(cursor="hand2"))
        canvas.tag_bind(close_id, "<Leave>", lambda _event: canvas.config(cursor=""))

        # Gemini response bubble and speech tail.
        rounded_rectangle(
            canvas, 42, 98, 658, 390, 26, fill=BUBBLE, outline=""
        )
        canvas.create_polygon(
            42, 338, 42, 398, 20, 398, 45, 375, fill=BUBBLE, outline=""
        )

        response_text = tk.Text(
            self.chat_window,
            wrap=tk.WORD,
            font=("Segoe UI", 13),
            fg=WHITE,
            bg=BUBBLE,
            insertbackground=WHITE,
            selectbackground="#8f292e",
            bd=0,
            highlightthickness=0,
            padx=4,
            pady=4,
        )
        response_text.place(x=66, y=120, width=568, height=242)
        response_text.insert(
            tk.END, "Hi! 🐱\n\nWhat would you like to talk about?"
        )
        response_text.configure(state=tk.DISABLED)

        # Rounded white input area.
        rounded_rectangle(
            canvas,
            44,
            420,
            656,
            480,
            17,
            fill="#fffefd",
            outline=OUTLINE,
            width=1,
        )
        chat_entry = tk.Entry(
            self.chat_window,
            font=("Segoe UI", 13),
            fg="#aaaaaa",
            bg="#fffefd",
            insertbackground="#3a2525",
            relief=tk.FLAT,
            bd=0,
        )
        chat_entry.place(x=66, y=437, width=565, height=27)
        chat_entry.insert(0, PLACEHOLDER)

        def clear_placeholder(_event=None):
            if chat_entry.get() == PLACEHOLDER:
                chat_entry.delete(0, tk.END)
                chat_entry.configure(fg="#3a2525")

        def restore_placeholder(_event=None):
            if not chat_entry.get():
                chat_entry.insert(0, PLACEHOLDER)
                chat_entry.configure(fg="#aaaaaa")

        chat_entry.bind("<FocusIn>", clear_placeholder)
        chat_entry.bind("<FocusOut>", restore_placeholder)

        # Rounded canvas button.
        button_shape = rounded_rectangle(
            canvas,
            298,
            494,
            402,
            536,
            15,
            fill=BUTTON,
            outline=OUTLINE,
            width=1,
            tags=("talk_button",),
        )
        button_text = canvas.create_text(
            350,
            515,
            text="Talk",
            fill=WHITE,
            font=("Segoe UI", 13, "bold"),
            tags=("talk_button",),
        )
        button_enabled = {"value": True}
########################################################### chat design ###########################################################
        def set_button_enabled(enabled):
            button_enabled["value"] = enabled
            canvas.itemconfigure(button_shape, fill=BUTTON if enabled else "#a95a5d")
            canvas.itemconfigure(button_text, fill=WHITE if enabled else "#e6bfc0")

        def show_response(text):
            response_text.configure(state=tk.NORMAL)
            response_text.delete("1.0", tk.END)
            response_text.insert(tk.END, text)
            response_text.see("1.0")
            response_text.configure(state=tk.DISABLED)

        def request_finished(answer=None, error=None):
            if not self.chat_window or not self.chat_window.winfo_exists():
                return
            set_button_enabled(True)
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
                self.result_queue.put((self.gemini.ask(prompt), None))
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

        def save_button_pressed(_event=None):
            if not button_enabled["value"]:
                return
            chat_text = chat_entry.get().strip()
            if not chat_text or chat_text == PLACEHOLDER:
                messagebox.showerror(title="Empty message", message="Please enter a message")
                return

            chat_entry.delete(0, tk.END)
            chat_entry.configure(state=tk.DISABLED)
            set_button_enabled(False)
            show_response("Thinking…")
            self.cat.state = "talk"
            self.cat.change_animation("talk")
            self.cat.last_interaction = time.time()
            Thread(target=ask_gemini, args=(chat_text,), daemon=True).start()
            self.chat_window.after(100, check_for_result)

        canvas.tag_bind("talk_button", "<Button-1>", save_button_pressed)
        canvas.tag_bind("talk_button", "<Enter>",
            lambda _event: (canvas.config(cursor="hand2"), canvas.itemconfigure(button_shape,fill=BUTTON_HOVER if button_enabled["value"] else "#a95a5d"))
                        )

        canvas.tag_bind("talk_button", "<Leave>",
                        lambda _event: (canvas.config(cursor=""), canvas.itemconfigure(button_shape,fill=BUTTON if button_enabled["value"] else "#a95a5d"))
                        )
        chat_entry.bind("<Return>", save_button_pressed)

        # the borderless window can be moved by dragging its header.
        drag = {"x": 0, "y": 0}

        def start_drag(event):
            drag["x"], drag["y"] = event.x_root, event.y_root

        def move_window(event):
            dx, dy = event.x_root - drag["x"], event.y_root - drag["y"]
            self.chat_window.geometry(
                f"+{self.chat_window.winfo_x() + dx}"
                f"+{self.chat_window.winfo_y() + dy}"
            )
            drag["x"], drag["y"] = event.x_root, event.y_root

        canvas.bind("<ButtonPress-1>", start_drag)
        canvas.bind("<B1-Motion>", move_window)
        chat_entry.focus_set()
