from tkinter import *
from infi.systray import SysTrayIcon
from threading import Thread
from time import sleep

icon_tray=None
close=None
quit_flag=False
interrupt_flag=False
exec_th=None

def IconTrayStart(app_title, icon_file, app_close):
    global icon_tray
    global close
    global exec_th
    
    menu = (("Settings", None, __settings),)
    icon_tray = SysTrayIcon(icon_file, app_title, menu, on_quit=__on_quit)
    close = app_close
    icon_tray.start()
    exec_th = Thread(target=__quit_wait)
    exec_th.start()

def IconTrayQuit():
    global quit_flag
    global exec_th
    global interrupt_flag
    
    if quit_flag == False:
        interrupt_flag = True
        quit_flag = True
        exec_th.join()
        
def __settings(ti):
    print("Settings")

def __on_quit(ti):
    global quit_flag
    
    quit_flag=True
    
def __quit_wait():
    global quit_flag
    global close
    global icon_tray
    global interrupt_flag
    
    while quit_flag == False:
        sleep(0.1)
    icon_tray.shutdown()
    if interrupt_flag == False:
      close()
