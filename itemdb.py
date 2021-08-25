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
                # Create basic tables
                self.__simple_request("CREATE TABLE IF NOT EXISTS ru_translate(" \
                                          "id INTEGER PRIMARY KEY, translate TEXT NOT NULL);")
                
                self.__simple_request("CREATE TABLE IF NOT EXISTS equipment(" \
                                          "id INTEGER PRIMARY KEY, name TEXT NOT NULL," \
                                          "ru_translate_id INTEGER,"\
                                          "FOREIGN KEY (ru_translate_id) REFERENCES ru_translate (id));")
                
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
        return self.__simple_request("SELECT name FROM sqlite_master WHERE type='table';")

    def get_table(self, tab):
        return self.__simple_request("SELECT * FROM %s;" % tab)

    def get_table_size(self, tab_name):
        return self.__simple_request("SELECT count(*) FROM %s;" % tab_name)

    def add_to_table(self, tab_name, value, col='name'):
        if self.__db_con != None:
            tab_current_id = self.get_table_size(tab)[0][0] + 1
            cur = self.__db_con.cursor()
            cur.execute("INSERT INTO %s (id, %s) VALUES (%d, '%s')" % (tab_name, col, tab_current_id, value))
            cur.close()
            self.__db_con.commit()

    def delete_table(self, tab):
        if self.__db_con != None:
            cur = self.__db_con.cursor()
            cur.execute("DROP TABLE IF EXISTS %s" % tab)
            cur.close()
            self.__db_con.commit()

    def set_translation(self, tab, tab_id, trans_id):
        if self.__db_con != None:
            cur = self.__db_con.cursor()
            cur.execute("UPDATE %s SET ru_translate_id = %d WHERE id = %d" % (tab, trans_id, tab_id))
            cur.close()
            self.__db_con.commit()

    def get_translation(self, tab, word):
        return self.__simple_request("SELECT translate FROM ru_translate WHERE id = (SELECT ru_translate_id FROM %s WHERE name = '%s');" % (tab, word))
        
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
    #i_db.delete_table('ru_translate')
    print(i_db.get_version())

    #i_db.set_translation('equipment', 1, 1)
    tables = i_db.get_tables()
    for tab in tables:
        tab_size = i_db.get_table_size(tab[0])[0][0]
        print("Table: %s with size %d" % (tab[0], tab_size))
        if tab_size > 0:
            for n in range(1, tab_size + 1):
                print("  Row %d: %s" % (n, i_db.get_tab_raw(tab[0], n)))

    #i_db.add_to_table('ru_translate', 'броня', 'translate')
    #print(i_db.get_table('ru_translate'))
    #i_db.add_to_table('equipment', 'armour')
    #
    print(i_db.get_translation('equipment', 'armour'))
    i_db.close()
