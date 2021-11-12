from declarations import *
import sqlite3


class Database:
    def __init__(self, name: str = DATABASE_NAME):
        self.name = name
        self.con = None
        self.cursor = None

    def __enter__(self):
        self.con = sqlite3.connect(self.name)
        self.cursor = self.con.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.con is not None:
            self.con.close()

    def commit(self):
        self.con.commit()