import sqlite3

# App database backend

class Database:
    conn=sqlite3.connect(database="data.db")
    def __init__(self, db):
        self.cur=self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, title text, path text, imagelink text)")
        self.conn.commit()

    def insert(self, title, path,imagelink):
        self.cur.execute("INSERT INTO data (title,path,imagelink) VALUES (?,?,?)", (title,path,imagelink))
        self.conn.commit()

    def view(self):
        #cur.execute("INSERT INTO store VALUES('%s','%s','%s')" % (item,quantity,price))
        self.cur.execute("SELECT * FROM data")
        rows=self.cur.fetchall()
        return rows
    #
    # def search(self,title="",path="",date="",link="",imagelink="" ):
    #     #cur.execute("INSERT INTO store VALUES('%s','%s','%s')" % (item,quantity,price))
    #     self.cur.execute("SELECT * FROM data WHERE title=? OR path=? OR date=? OR link=? OR imagelink=?", (title,path,date,link,imagelink))
    #     rows=self.cur.fetchall()
    #     return rows
    #
    # def delete(self,id):
    #     self.cur.execute("DELETE FROM book WHERE id=?",(id,))
    #     self.conn.commit()
    #
    # def update(self, title, path, date, link, imagelink):
    #     self.cur.execute("UPDATE book SET title=?, path=?,date=?, link=?, imagelink=? WHERE id=?",(title,path,date,link,imagelink))
    #     self.conn.commit()


    def __del__(self):
        self.conn.close()
