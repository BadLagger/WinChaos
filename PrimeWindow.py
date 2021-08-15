#!/usr/bin/python
from tkinter import *
from pynput import keyboard, mouse
from pytesseract import image_to_string
import pyscreenshot as ImageGrab
from PIL import Image
from pathlib import Path
import os


class PrimeWindow:
    def __init__(self):
        self._win = Tk()
        self._win.overrideredirect(True)
        self._win.lift()
        self._win.wm_attributes("-topmost", True)
       # self._win.wm_attributes("-disabled", True)
        self._win.wm_attributes("-transparentcolor", "white")
        
        self._scr_width = self._win.winfo_screenwidth()
        self._scr_height = self._win.winfo_screenheight()
        print("w: %d h: %d" % (self._scr_width, self._scr_height))
       # self._win.geometry("%dx%d+0+0" % (self._scr_width, self._scr_height))
        self._canvas = Canvas(self._win, width=self._scr_width, height=self._scr_height, bg='white')
        self._canvas.pack()
        self._canvas.last_mouse_x = 0
        self._canvas.last_mouse_y = 0
        self._rect_show = False
        self._track_mouse = False
        self._win.bind('<FocusIn>', self._in_focus)
        self._win.bind('<FocusOut>', self._out_focus)  
        self._win.bind('<Motion>', self._motion)
        self._scrshot_save_name='src.png'
        self._x1 = 0
        self._x2 = 0
        self._y1 = 0
        self._y2 = 0
        self._lx = 0
        self._ly = 0
        self._tx1 = 0
        self._tx2 = 0
        self._ty1 = 0
        self._ty2 = 0

    def set_mouse_track(self, a, b):
        self._a = a
        self._b = b
        self._track_mouse = True

    def take_shot_of_area(self):
        print('take shot')
        try:
            print("x1=%d y1=%d x2=%d y2=%d" % (self._x1, self._y1, self._x2, self._y2))
            pic_file = Path(self._scrshot_save_name)
            if pic_file.is_file():
               # print('file exist')
                os.remove(self._scrshot_save_name)
            im = ImageGrab.grab(backend="pil", bbox=(int(self._x1 * 1.5), int(self._y1 * 1.5), int(self._x2 * 1.5), int(self._y2 * 1.5)))
            im.save(self._scrshot_save_name)
            print(image_to_string(Image.open(self._scrshot_save_name)))
        except Exception as err:
            print(err)
       # im.save(self._scrshot_save_name)
        
        
    def show(self):
        listener_kbd = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
        listener_kbd.start()
        #listener_ms = mouse.Listener(on_move=self._ms_move)
        #listener_ms.start()
        self._win.mainloop()

    def _in_focus(self, event):
        #if self._canvas.last_mouse_x != 0 and self._canvas.last_mouse_y != 0:
        #    self._canvas.create_rectangle(10, 10, 190, 60, tags="rect")
        #    self._rect_show = True
        print('Focus IN!!!')

    def _out_focus(self, event):
        self._canvas.delete("rect")
        print('Focus OUT!!!')

    def _motion(self, event):
       # print('x = %d, y = %d' % (event.x, event.y))
        if self._track_mouse:
            if self._rect_show == True:
                self._canvas.delete("rect")

            step_x = self._a / 2
            step_y = self._b / 2

            if event.x - step_x < 0:
                self._x1 = 0
            else:
                self._x1 = event.x - step_x

            if event.y - step_y  < 0:
                self._y1 = 0
            else:
                self._y1 = event.y - step_y

            if event.x + step_x > self._scr_width:
                self._x2 =  self._scr_width
            else:
                self._x2 = event.x + step_x

            if event.y + step_y > self._scr_height:
                self._y2 =  self._scr_height
            else:
                self._y2 = event.y + step_y

            self._canvas.create_rectangle(self._x1, self._y1, self._x2, self._y2, tags="rect", outline='green', width=3)
            self._rect_show = True

    def _on_press(self, key):
        if str(type(key)) == "<enum 'Key'>":
           # print(key.name, key.value)
            if key.name == 'esc':
                self._win.destroy()
                exit()
            elif key.name == 'f10':
                self.take_shot_of_area()
                
        else:
            print(key.char)

    def _on_release(self, key):
        pass

    def _ms_move(self, x, y):
       # print('Mouse move: x - %d y - %d' % (x, y))
        self._lx, self._ly = x, y
        

        
    
