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
        if self.__init == True:
            return self.__sets.get("lang")
        else:
            return None

    def get_filter(self):
        if self.__init == True:
            return self.__sets.get("filter")
        else:
            return None

if __name__ == "__main__":
    cfg = Cfg("sets.cfg")
    print(cfg.get_language())
    print(cfg.get_filter())
