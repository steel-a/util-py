import sqlite3

class Vault:

    def __init__(self, file:str):
        self.conn = sqlite3.connect(file)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS vault (
                key TEXT NOT NULL,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                PRIMARY KEY(key)
            );
        """)

    def __del__(self):
        self.conn.close()


    def __insert(self, key:str, username:str, password:str):
        self.cursor.execute(f"""
            insert into vault (key, username, password)
            values ('{key}','{username}','{password}')
        """)
        self.conn.commit()


    def __update(self, key:str, username:str, password:str):
        self.cursor.execute(f"""
            update vault set username = '{username}', password = '{password}'
            where key = '{key}'
        """)
        self.conn.commit()


    def put(self, key:str, username:str, password:str):
        if self.get(key) == None:
            self.__insert(key, username, password)
        else:
            self.__update(key, username, password)


    def get(self, key:str):
        self.cursor.execute(f"""
            select username, password from vault
            where key = '{key}'
        """)

        if self.cursor.rowcount == 0:
            return None

        res = self.cursor.fetchone()
        return res

    def getAll(self):
        self.cursor.execute(f"""
            select key, username, password from vault
        """)

        if self.cursor.rowcount == 0:
            return None

        res = self.cursor.fetchall()
        return res

    def delete(self, key:str):
        return self.cursor.execute(f"""
            delete from vault
            where key = '{key}'
        """)

    def close(self):
        self.conn.close()
