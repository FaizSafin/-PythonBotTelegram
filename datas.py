import sqlite3

db = sqlite3.connect('database.db')

cursor = db.cursor()

async def start_db():
    cursor.execute('''
CREATE TABLE IF NOT EXISTS cars(
                   name TEXT,
                   phone_num TEXT
)
''')
async def add_to_db(name,phone_num):
    cursor.execute('''
INSERT INTO cars(
                   name,phone_num
)
                   VALUES(?,?)
''',(name,phone_num))
    db.commit()
