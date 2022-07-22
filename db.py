import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS parts_list (id INTEGER PRIMARY KEY, day text, "
            "hour text, minute text, zoom text)")
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM parts_list")
        rows = self.cur.fetchall()
        return rows

    def insert(self, day, hour, minute, zoom):
        self.cur.execute("INSERT INTO parts_list VALUES (NULL, ?, ?, ?, ?)",
                         (day, hour, minute, zoom))
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM parts_list WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, day, hour, minute, zoom):
        self.cur.execute("UPDATE parts_list SET day = ?, hour = ?, minute = ?, zoom = ? WHERE id = ?",
                         (day, hour, minute, zoom, id))
        self.conn.commit()

    def fetchLastRow(self):
        self.cur.execute("SELECT * FROM parts_list ORDER BY ID DESC LIMIT 1")
        row = self.cur.fetchone()
        return row

    def __del__(self):
        self.conn.close()
