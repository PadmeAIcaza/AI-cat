import tkinter as tk
from tkinter import *
from pathlib import Path
from cat import Cat
from AIchat import AI

born_path = Path('../assets')/'sprites'/'Born.png'
idle_path = Path('../assets')/'sprites'/'Idle2.png'
talk_path = Path('../assets')/'sprites'/'Walk.png'
sleep_path = Path('../assets')/'sprites'/'Sleep.png'
jump_path = Path('../assets')/'sprites'/'Jump.png'

window = tk.Tk()
cat = Cat(window, born_path, idle_path, talk_path, sleep_path, jump_path)
AI_bot = AI(window, cat)
screen_width = window.winfo_screenwidth()  # 1536
screen_height = window.winfo_screenheight() # 864

window.title("VoidCat")
window.overrideredirect(True)
window.attributes("-topmost", True)
transparent_color = 'magenta'
window.configure(bg=transparent_color)
window.attributes('-transparentcolor', transparent_color)

window.geometry(f"{cat.window_width}x{cat.window_height}+{cat.x}+{cat.y}")

cat.label.bind('<Enter>', cat.wake_up)
cat.label.bind("<Button-1>", AI_bot.open_chat)
cat.check_idle()

window.bind("<Escape>", lambda event: window.destroy())
window.mainloop()