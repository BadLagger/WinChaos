#!/usr/bin/python
from tkinter import *

class PrimeWindow:
    def __init__(self):
        self._win = Tk()
        self._win.overrideredirect(True)
        self._win.lift()
        self._win.wm_attributes("-topmost", True)
        self._win.wm_attributes("-disabled", True)
        self._win.wm_attributes("-transparentcolor", "white")
        
        self._scr_width = self._win.winfo_screenwidth() / 2
        self._scr_height = self._win.winfo_screenheight() / 2
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

    def set_mouse_track(self, a, b):
        self._a = a
        self._b = b
        self._track_mouse = True
        
    def show(self):
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
        print('x = %d, y = %d' % (event.x, event.y))
        if self._track_mouse:
            if self._rect_show == True:
                self._canvas.delete("rect")

            step_x = self._a / 2
            step_y = self._b / 2

            if event.x - step_x < 0:
                x_1 = 0
            else:
                x_1 = event.x - step_x

            if event.y - step_y  < 0:
                y_1 = 0
            else:
                y_1 = event.y - step_y

            if event.x + step_x > self._scr_width:
                x_2 =  self._scr_width
            else:
                x_2 = event.x + step_x

            if event.y + step_y > self._scr_height:
                y_2 =  self._scr_height
            else:
                y_2 = event.y + step_y

            self._canvas.create_rectangle(x_1, y_1, x_2, y_2, tags="rect", outline='green', width=3)
            self._rect_show = True
        
    
