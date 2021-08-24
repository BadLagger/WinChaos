from pynput import keyboard, mouse
from pprint import pprint
from pickle import dump, load
from time import sleep

class ActionRecord:
    def __init__(self):
        self.__action=[]
        self.__kbd_ctrl = keyboard.Controller()
        self.__ms_ctrl = mouse.Controller()
        self.__act_delay = 0.1
    
    def update_filter(self, current_ms_x, current_ms_y):
        self.__kbd_ctrl.press(keyboard.Key.esc)
        sleep(self.__act_delay)
        self.__kbd_ctrl.release(keyboard.Key.esc)
        sleep(self.__act_delay)
        self.__ms_ctrl.position = (1974, 701)
        sleep(self.__act_delay)
        self.__ms_ctrl.click(mouse.Button.left, 1)
        sleep(self.__act_delay)
        self.__ms_ctrl.position = (406, 243)
        sleep(self.__act_delay)
        self.__ms_ctrl.click(mouse.Button.left, 1)
        sleep(self.__act_delay)
        self.__ms_ctrl.position = (1065, 438)
        sleep(self.__act_delay)
        self.__ms_ctrl.click(mouse.Button.left, 1)
        sleep(self.__act_delay)
        self.__kbd_ctrl.press(keyboard.Key.esc)
        sleep(self.__act_delay)
        self.__kbd_ctrl.release(keyboard.Key.esc)
        sleep(self.__act_delay)
        self.__ms_ctrl.position = (current_ms_x, current_ms_y)
        

    def start_record(self, stop_key=''):
        self.__kbd_lis = keyboard.Listener(on_press=self.__on_kbd_press, suppress=False)
        self.__ms_lis = mouse.Listener(on_click=self.__on_mouse_click, suppress=False)
        self.__kbd_lis.start()
        self.__ms_lis.start()
        self.__stop_key=stop_key
        
    def stop_record(self):
        self.__kbd_lis.stop()
        self.__ms_lis.stop()

    def wait(self):
        self.__kbd_lis.join()
        self.__ms_lis.join()

    def save_record(self, f_path_name=''):
        if len(f_path_name) == 0:
            pprint(self.__action)
        else:
            f = open(f_path_name, "wb")
            dump(self.__action, f)
            f.close()

    def load_record(self, f_path_name):
        with open(f_path_name, 'rb') as f:
            self.__action = load(f)
            pprint(self.__action)

    def do_action(self):
        for act in self.__action:
            if act['press'] == 'kbd':
                self.__kbd_ctrl.press(act['key'])
                self.__kbd_ctrl.release(act['key'])
            else:
                self.__ms_ctrl.position = (act['x'], act['y'])
                self.__ms_ctrl.press(act['btn'])
                self.__ms_ctrl.release(act['btn'])

    def __on_kbd_press(self, key):
        act = {'press':'kbd'}
        if str(type(key)) == "<enum 'Key'>":
            print(key.name, key.value)
            cur_key_str = key.name
            act['type'] = 'enum'
            act['key'] = key
        else:
            print(key.char, key._scan)
            act['type'] = 'ch'
            act['key'] = key
            cur_key_str = key.char

        if len(self.__stop_key) != 0:
            if cur_key_str == self.__stop_key:
                self.stop_record()
                return
                
        self.__action.append(act)
 

    def __on_mouse_click(self, x, y, button, pressed):
        print("Mouse click at (%d, %d), btn=%s pressed=%s" % (x, y, button, pressed))
        act = {'press':'ms', 'x': x, 'y': y, 'btn': button}
        self.__action.append(act)
        

if __name__ == '__main__':
    print("Bgn Action Record")
    ms = mouse.Controller()
    ms.position = (34, 2138)
    ms.press(mouse.Button.left)
    ms.release(mouse.Button.left)
   # ac = ActionRecord()
   # ac.load_record('test_action.pkl')
   # ac.do_action()
   # ac.start_record('q')
   # ac.wait()
   # ac.save_record('test_action.pkl')
    print("End Action Record")
