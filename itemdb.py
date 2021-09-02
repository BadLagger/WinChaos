from sqlite3 import *

class ItemDb:
    def __init__(self, db_file, db_open=True):
        self.__db_con = None
        self.__db_file = db_file
        if db_open == True:
            self.open()

    def open(self):
        if self.__db_con == None:
            try:
                self.__db_con = connect(self.__db_file)
                tab_list = self.get_tables()
                self.__item_tabs_list = []
                for tab in tab_list:
                    if tab != 'sqlite_sequence' and tab != 'alternatives':
                        self.__item_tabs_list.append(tab)
               # print(self.__tab_list)
               # print(self.__item_tabs_list)
            except Error as db_err:
                self.__db_con = None
                print('db %s connection error: %s' % (self.__db_file, db_err))

    def close(self):
        if self.__db_con != None:
            self.__db_con.close()
            self.__db_con = None

    def get_version(self):
        return self.__simple_request('SELECT sqlite_version();')

    def get_tables(self):
        ret_list = self.__simple_request("SELECT name FROM sqlite_master WHERE type='table'")
        return [el[0] for el in ret_list]

    def search_for_item(self, item_name=None, item_translate=None):
        if item_name != None:
            for tab in self.__item_tabs_list:
                result = self.__simple_request("SELECT * FROM %s WHERE name = '%s'" % (tab, item_name))
                if len(result) != 0:
                    return result
            return None

        if item_translate != None:
            for tab in self.__item_tabs_list:
                result = self.__simple_request("SELECT * FROM %s WHERE ru_translation = '%s'" % (tab, item_translate))
                if len(result) != 0:
                    return result
        
        return None;

    def check_for_alternatives(self, item_name):
        result = self.__simple_request("SELECT * FROM alternatives WHERE name = '%s'" % item_name)
        if len(result) != 0:
            return result

        return None

    def get_table(self, tab):
        return self.__simple_request("SELECT * FROM %s;" % tab)

    def get_table_size(self, tab_name):
        return self.__simple_request("SELECT count(*) FROM %s;" % tab_name)
        
    def get_tab_raw(self, tab, id):
        return self.__simple_request("SELECT * FROM %s WHERE id = %d;" % (tab, id))
        
    def __simple_request(self, req):
        ret = None
        if self.__db_con != None:
            cur = self.__db_con.cursor()
            cur.execute(req)
            ret = cur.fetchall()
            cur.close()
        return ret
        

if __name__ == '__main__':
    print('Hello dbg itemdb.py')
    i_db = ItemDb('items.db')
    item = 'Windbreak Boots'
    result = i_db.check_for_alternatives(item)
    if result != None:
        print(result)
        in_data = result[0]
        result = i_db.get_tab_raw(tab=in_data[2], id=in_data[3])
        print(result)
    else:
        result = i_db.search_for_item(item_name=item)
        if result != None:
            print(result)
        else:
            print("No item found")
        
    i_db.close()
