#!/usr/bin/python
from tkinter import *
from hdpitkinter import *
from pynput import keyboard, mouse
from pytesseract import image_to_string
import pyscreenshot as ImageGrab
from PIL import Image
from pathlib import Path
from win32api import GetSystemMetrics
import os


class PrimeWindow:
    def __init__(self):
        # Window setting
        self._win = HdpiTk()
        self._win.overrideredirect(True)
        self._win.lift()
        self._win.wm_attributes("-topmost", True)
        self._win.wm_attributes("-transparentcolor", "white")
        self._scr_width = GetSystemMetrics(0)
        self._scr_height = GetSystemMetrics(1)
       # print("w: %d h: %d" % (self._scr_width, self._scr_height))
        # Canvas setting
        self._canvas = Canvas(self._win, width=self._scr_width, height=self._scr_height, bg='white')
        self._canvas.pack()
        self._canvas.last_mouse_x = 0
        self._canvas.last_mouse_y = 0
        # Tracking rectangle
        self._track_rect_w=0
        self._track_rect_h=0
        self._track_rect_show=False
        self._track_rect_color_index=0
        self._track_rect_color = ['grey', 'blue', 'yellow']
        # Picture
        self._scrshot_save_name='src.png'
        # Coords
        self._x1 = 0
        self._x2 = 0
        self._y1 = 0
        self._y2 = 0
        self._lx = 0
        self._ly = 0

    def set_track_rectangle(self, width, height):
        self._track_rect_w, self._track_rect_h = width, height
        self._track_rect_x_step = width / 2
        self._track_rect_y_step = height / 2

    def take_shot_of_area(self):
        print('take shot')
        try:
            pic_file = Path(self._scrshot_save_name)
            if pic_file.is_file():
                os.remove(self._scrshot_save_name)
            im = ImageGrab.grab(backend="pil", bbox=(int(self._x1), int(self._y1), int(self._x2), int(self._y2)))
            im.save(self._scrshot_save_name)
            word=image_to_string(Image.open(self._scrshot_save_name))
            clean_word=""
            big_letter=True
            for ch in word:
                if ch.isalpha() or (ch == ' ' and len(clean_word)):
                    if big_letter:
                        clean_word += ch
                        big_letter=False
                    else:
                        clean_word += ch.lower()
                        if ch == ' ':
                            big_letter=True

           # print("Dirty: %s" % word)
            print("Clean: %s" % clean_word)
        except Exception as err:
            print(err)

    def show_track_rect(self):
        self._x1 = 0 if self._lx - self._track_rect_x_step < 0 else self._lx - self._track_rect_x_step
        self._y1 = 0 if self._ly - self._track_rect_y_step < 0 else self._ly - self._track_rect_y_step
        self._x2 = self._scr_width if self._lx + self._track_rect_x_step > self._scr_width else self._lx + self._track_rect_x_step
        self._y2 = self._scr_height if self._ly + self._track_rect_y_step > self._scr_height else self._ly + self._track_rect_y_step
        self._canvas.create_rectangle(self._x1, self._y1, self._x2, self._y2, tags="rect", outline=self._track_rect_color[self._track_rect_color_index], width=3)
        self._track_rect_show=True

    def hide_track_rect(self):
        self._canvas.delete("rect")
        self._track_rect_show=False

    def increase_rect_width(self):
        self._track_rect_w += 2
        self._track_rect_x_step = self._track_rect_w / 2

    def decrease_rect_width(self):
        self._track_rect_w -= 2
        self._track_rect_x_step = self._track_rect_w / 2

    def increase_rect_height(self):
        self._track_rect_h += 2
        self._track_rect_y_step = self._track_rect_h / 2

    def decrease_rect_height(self):
        self._track_rect_h -= 2
        self._track_rect_y_step = self._track_rect_h / 2

        
    def show(self):
        listener_kbd = keyboard.Listener(on_press=self._on_press, on_release=self._on_release, suppress=False)
        listener_kbd.start()
        listener_ms = mouse.Listener(on_move=self._ms_move)
        listener_ms.start()
        self._win.mainloop()

    def _on_press(self, key):
        if str(type(key)) == "<enum 'Key'>":
          #  print(key.name, key.value)
            if key.name == 'f6':           # Exit from Drawer
                self._win.destroy()
                exit()
            elif key.name == 'f2':          # On/Off Tracking Rectangle
                if self._track_rect_show:
                    self.hide_track_rect()
                else:
                    self.show_track_rect()
            elif key.name == 'f3':          # Change Rectange Color (Rarity)
                self._track_rect_color_index = 0 if self._track_rect_color_index >= 2 else self._track_rect_color_index + 1
                self.show_track_rect()
            elif key.name == 'f4':          # Manual increase width
                self.increase_rect_width()
                self._update_rect()
            elif key.name == 'f5':          # Manual decrease width
                self.decrease_rect_width()
                self._update_rect()
            elif key.name == 'f9':          # Manual increase height
                self.increase_rect_height()
                self._update_rect()
            elif key.name == 'f10':          # Manual decrease height
                self.decrease_rect_height()
                self._update_rect()
            elif key.name == 'f11':         # Take shot and recognize
                self.take_shot_of_area()
                
        else:
            print(key.char)

    def _on_release(self, key):
        pass

    def _ms_move(self, x, y):
       # print('Mouse move: x - %d y - %d' % (x, y))
        self._lx, self._ly = x, y
        if self._track_rect_show:
            self._update_rect()

    def _update_rect(self):
        self.hide_track_rect()
        self.show_track_rect()
        

        
    
