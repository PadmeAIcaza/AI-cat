import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from AIchat import AI
import time

class Cat:
    def __init__(self, window, born_path, idle_path, talk_path, sleep_path, jump_path):
        self.window = window
        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()
        self.window_width = 64
        self.window_height = 64
        self.x = self.screen_width - self.window_width
        self.y = 0
        self.state = 'born'
        self.animations = {}
        self.current_frame = 0
        self.animations = {
            'born': self.load_animation(
                born_path,
                frame_width=32,
                frame_height=32
            ),

            'idle': self.load_animation(
                idle_path,
                frame_width=32,
                frame_height=32
            ),

            'talk': self.load_animation(
                talk_path,
                frame_width=32,
                frame_height=32
            ),

            'sleep': self.load_animation(
                sleep_path,
                frame_width=64,
                frame_height=64
            ),
            'jump': self.load_animation(
                jump_path,
                frame_width=32,
                frame_height=32
            )
        }
        self.current_animation = 'born'
        self.last_interaction = time.time()

        self.label = tk.Label(self.window, image=self.animations['born'][0], width=64, height=64, bg="magenta", borderwidth=0)
        self.label.pack()
        self.animate()

    def load_animation(self, sprite_path, frame_width, frame_height):
        sprite_sheet = Image.open(sprite_path)

        frame_count = sprite_sheet.width // frame_width
        frames = []

        for frame_number in range(frame_count):
            left = frame_number * frame_width
            top = 0
            right = left + frame_width
            bottom = frame_height

            frame = sprite_sheet.crop(
                (left, top, right, bottom)
            )

            frames.append(ImageTk.PhotoImage(frame))

        return frames

    def change_animation(self, animation_name):
        if self.current_animation == animation_name:
            return # avoids restarting the animation if it is already active

        self.current_animation = animation_name
        self.current_frame = 0

    def animate(self):
        frames = self.animations[self.current_animation]

        self.label.config(image=frames[self.current_frame])

        self.current_frame += 1

        # Check whether the current animation reached its final frame.
        if self.current_frame >= len(frames):

            if self.current_animation == "born":
                # Born only plays once, then switches to idle.
                self.current_animation = "idle"
                self.current_frame = 0
            else:
                # Other animations loop normally.
                self.current_frame = 0

        self.window.after(100, self.animate)

    def check_idle(self):
        current_time = time.time()
        elapsed = current_time - self.last_interaction
        if elapsed > 5:
            self.state = 'sleep'
            self.change_animation(self.state)

        self.window.after(500, self.check_idle)

    def wake_up(self, _):
        if self.state == 'sleep':
            self.state = 'jump'
            self.change_animation(self.state)
            self.last_interaction = time.time()

            self.window.after(800, self.woken_up)

    def woken_up(self):
        if self.state == 'jump':
            self.state = 'idle'
            self.change_animation(self.state)


