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
import pprint
from ActionRecord import ActionRecord


class PrimeWindow:
    def __init__(self):
        # Window setting
        self._win = HdpiTk()
        self._win.overrideredirect(True)
        self._win.lift()
        self._win.wm_attributes("-topmost", True)
        self._win.wm_attributes("-transparentcolor", "white")
        self._scr_width = GetSystemMetrics(0) - 5
        self._scr_height = GetSystemMetrics(1) - 5
        # Canvas setting
        self._canvas = Canvas(self._win, width=self._scr_width, height=self._scr_height, bg='white')
        self._canvas.pack()
        self._canvas.last_mouse_x = 0
        self._canvas.last_mouse_y = 0
        # Tracking rectangle
        self._track_rect_w = 0
        self._track_rect_h = 0
        self._track_rect_show = False
        self._track_rect_color_index = 0
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
        # Lootfilter file
        self._lf_file_path=r'C:\Users\lanyn\Documents\My Games\Path of Exile\duelist.filter'
        self.load_lootfilter_file()
        self._clean_word = ""
        # Item label
        self._item_lbl_show=False
        self.__ac = ActionRecord() 

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
            word=image_to_string(Image.open(self._scrshot_save_name), lang='rus')
            self._clean_word=""
            big_letter=True
            for ch in word:
                if ch.isalpha() or (ch == ' ' and len(self._clean_word)):
                    if big_letter:
                        self._clean_word += ch
                        big_letter=False
                    else:
                        self._clean_word += ch.lower()
                        if ch == ' ':
                            big_letter=True
            
            self._clean_word = "\"%s\"" % self._clean_word.strip()
            if self._clean_word == '"Twopoint Arrow Quiver"':
                self._clean_word = '"Two-Point Arrow Quiver"'
            elif self._clean_word == '"Goats Horn"':
                self._clean_word = '"Goat\'s Horn"'
            elif self._clean_word == '"Twohanded Sword"':
                self._clean_word = '"Two-Handed Sword"'
            elif self._clean_word == '"Scholars Robe"':
                self._clean_word = '"Scholar\'s Robe"'
            elif self._clean_word == '"Cats Paw"':
                self._clean_word = '"Cat\'s Paw"'
            elif self._clean_word == '"Mages Vestment"':
                self._clean_word = '"Mage\'s Vestment"'
            elif self._clean_word == '"Thiefs Garb"':
                self._clean_word = '"Thief\'s Garb"'
            elif self._clean_word == '"Soldiers Brigandine"':
                self._clean_word = '"Soldier\'s Brigandine"'
            elif self._clean_word == '"Sages Robe"':
                self._clean_word = '"Sage\'s Robe"'
                
            print("Clean: %s" % self._clean_word)
        except Exception as err:
            print(err)

    def load_lootfilter_file(self):
        self._lf_basic = []
        self._lf_normal = []
        self._lf_magic = []
        self._lf_rare = []
        with open(self._lf_file_path, 'r') as file:
            for line in file:
              #  pprint.pprint(line)
                if len(self._lf_normal) == 0:
                    if line.find('# Normal') != -1:
                        print('Get normal')
                        self._lf_normal.append(line)
                    else:
                        self._lf_basic.append(line)
                elif len(self._lf_magic) == 0:
                    if line.find('# Magic') != -1:
                        print('Get magic')
                        self._lf_magic.append(line)
                    else:
                        self._lf_normal.append(line)
                elif len(self._lf_rare) == 0:
                    if line.find('# Rare') != -1:
                        print('Get rare')
                        self._lf_rare.append(line)
                    else:
                        self._lf_magic.append(line)
                else:
                    self._lf_rare.append(line)
                    
        #pprint.pprint(self._lf_basic)
    def save_lootfilter_file(self):
        with open(self._lf_file_path, 'w') as file:
            for line in self._lf_basic:
                file.write(line)
            for line in self._lf_normal:
                file.write(line)
            for line in self._lf_magic:
                file.write(line)
            for line in self._lf_rare:
                file.write(line)
        self.__ac.update_filter(self._lx, self._ly)

    def add_item_to(self, rarity='basic', item=""):
        print('Try add %s %s' % (rarity, item))
        if rarity == 'basic':
            pprint.pprint(self._lf_basic)
        elif rarity == 'normal':
            if len(item) == 0:
                pprint.pprint(self._lf_normal)
            else:
                if len(self._lf_normal) < 3:
                    self._lf_normal = []
                    self._lf_normal.append("# Normal\n")
                    self._lf_normal.append("Hide\n")
                    self._lf_normal.append("\tRarity Normal\n")
                    self._lf_normal.append("\tBaseType\n")
                    self._lf_normal.append("\n")
                self._lf_normal[3] = self._lf_normal[3].strip()
                self._lf_normal[3] = "\t%s %s\n" % (self._lf_normal[3], item)
        elif rarity == 'magic':
            if len(item) == 0:
                pprint.pprint(self._lf_magic)
            else:
                if len(self._lf_magic) < 3:
                    self._lf_magic = []
                    self._lf_magic.append("# Magic\n")
                    self._lf_magic.append("Hide\n")
                    self._lf_magic.append("\tRarity Magic\n")
                    self._lf_magic.append("\tBaseType\n")
                    self._lf_magic.append("\n")
                self._lf_magic[3] = self._lf_magic[3].strip()
                self._lf_magic[3] = "\t%s %s\n" % (self._lf_magic[3], item)
        elif rarity == 'rare':
            if len(item) == 0:
                pprint.pprint(self._lf_rare)
            else:
                if len(self._lf_rare) < 3:
                    self._lf_rare = []
                    self._lf_rare.append("# Rare\n")
                    self._lf_rare.append("Hide\n")
                    self._lf_rare.append("\tRarity Rare\n")
                    self._lf_rare.append("\tBaseType\n")
                    self._lf_rare.append("\n")
                self._lf_rare[3] = self._lf_rare[3].strip()
                self._lf_rare[3] = "\t%s %s\n" % (self._lf_rare[3], item)

    def show_item_lbl(self):
        if self._item_lbl_show == False:
            self._canvas.create_text(self._x1 + 100, self._y1 - 20, font='Arial 23', text=self._clean_word, fill=self._track_rect_color[self._track_rect_color_index], tags='item_lbl')
            self._item_lbl_show=True
    
    def hide_item_lbl(self):
        if self._item_lbl_show == True:
            self._canvas.delete("item_lbl")
            self._item_lbl_show=False

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
       # self._clean_word=""

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
            if key.name == 'f6':           # Exit from Drawer
                self._win.destroy()
                exit()
            elif key.name == 'f2':          # On/Off Tracking Rectangle
                if self._track_rect_show:
                    self.hide_track_rect()
                    self.hide_item_lbl()
                else:
                    self.show_track_rect()
            elif key.name == 'f3':          # Change Rectange Color (Rarity)
                self._track_rect_color_index = 0 if self._track_rect_color_index >= 2 else self._track_rect_color_index + 1
                self._update_rect()
                self._update_item_lbl()
            elif key.name == 'f4':          # Manual increase width
                self.increase_rect_width()
                self._update_rect()
                self._update_item_lbl()
            elif key.name == 'f5':          # Manual decrease width
                self.decrease_rect_width()
                self._update_rect()
                self._update_item_lbl()
            elif key.name == 'f9':          # Manual increase height
                self.increase_rect_height()
                self._update_rect()
                self._update_item_lbl()
            elif key.name == 'f10':          # Manual decrease height
                self.decrease_rect_height()
                self._update_item_lbl()
                self._update_rect()
            elif key.name == 'f11':         # Take shot and recognize
                self.take_shot_of_area()
                #self._update_rect()
                self._update_item_lbl()
            elif key.name == 'insert':      # Add item to the list or show list
                if self._track_rect_color[self._track_rect_color_index] == 'grey':
                    rar = 'normal'
                elif self._track_rect_color[self._track_rect_color_index] == 'blue':
                    rar = 'magic'
                elif self._track_rect_color[self._track_rect_color_index] == 'yellow':
                    rar = 'rare'
                
                if len(self._clean_word) == 0:
                    print('Empty clean word')
                self.add_item_to(rarity=rar, item=self._clean_word)
            elif key.name == 'pause':       # Save to filter
                self.save_lootfilter_file()
                self.load_lootfilter_file()
                self.hide_item_lbl()
       # else:
       #     print(key.char)

    def _on_release(self, key):
        pass

    def _ms_move(self, x, y):
        self._lx, self._ly = x, y
        if self._track_rect_show:
            self._update_rect()
            self._update_item_lbl()

    def _update_rect(self):
        self.hide_track_rect()
        self.show_track_rect()
    
    def _update_item_lbl(self):
        self.hide_item_lbl()
        self.show_item_lbl()
        

        
    
