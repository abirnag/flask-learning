import sqlite3

DB_FILE='data.db'

class Db:
    def execute_and_commit(self,query,*args):
        global DB_FILE
        self.__connection = sqlite3.connect(DB_FILE)
        cursor = self.__connection.cursor()
        result = cursor.execute(query,args)
        self.__connection.commit()
        return result
    def connection_close(self):
        self.__connection.close()


