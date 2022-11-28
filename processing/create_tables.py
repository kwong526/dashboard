import sqlite3
conn = sqlite3.connect('stats.sqlite')
c = conn.cursor()
c.execute('''
    CREATE TABLE stats
    (id INTEGER PRIMARY KEY ASC, 
    num_buy_readings INTEGER NOT NULL,
    num_price_readings INTEGER NOT NULL,
    max_buy_reading INTEGER,
    max_price_reading INTEGER,
    min_buy_reading INTEGER,
    min_price_reading INTEGER,
    last_updated VARCHAR(100) NOT NULL)
    ''')

conn.commit()
conn.close()