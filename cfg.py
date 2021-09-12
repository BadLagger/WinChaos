import json

class Cfg:
    def __init__(self, fpath):
        try:
            with open(fpath, "r") as input:
                self.__sets = json.load(input)
            self.__init = True
        except Exception as err:
            print("error: " + str(err))
            self.__init = False


    def get_language(self):
        return self.__get_prm('lang')

    def get_filter(self):
        return self.__get_prm('filter')

    def get_trayicon(self):
        return self.__get_prm('icontray')

    def __get_prm(self, prm_name):
        return self.__sets.get(prm_name) if self.__init == True else None

if __name__ == "__main__":
    cfg = Cfg("sets.cfg")
    print(cfg.get_language())
    print(cfg.get_filter())
    print(cfg.get_trayicon())
