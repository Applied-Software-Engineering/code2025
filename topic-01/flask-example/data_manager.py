import os
import sqlite3

class SimpleDataManager:

    def __init__(self):
        self.users = []

    def load_users(self, filename):
        with open(filename) as csv_file:
            for name in csv_file:
                self.users.append(name.strip())

    def get_db_connection(self, db_filename):
        db = sqlite3.connect(db_filename)
        db.execute('create table if not exists users(name text not null, location text,club text);')
        # db.execute('.read create_table.sql')
        # db.execute('insert into users values("Mary", "London", null);')
        return db


    def load_user_from_db(self, csv_filename, db_filename):
        with open(csv_filename, 'r') as csv_file:
            db = self.get_db_connection(db_filename)
            for line in csv_file:
                name, location, club = line.split(',')
                self.users.append(name)
                # print(db.execute('select * from users').fetchall())
                db.execute(f'insert into users values ("{name}", "{location}", "{club}");')