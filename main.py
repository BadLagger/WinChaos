#!/usr/bin/python
from PrimeWindow import PrimeWindow
#import sys
#from qDrawer import qDrawer

if __name__ == '__main__':
    print('Hello, win chaos!')
    #app = qDrawer(sys.argv)
    #sys.exit(app.get_app_exec())
    app = PrimeWindow()
    app.set_track_rectangle(250, 50)
    app.show()
