import sqlite3

conn = sqlite3.connect("readings.sqlite")

c = conn.cursor()
c.execute('''
          CREATE TABLE buy_event
          (id INTEGER PRIMARY KEY ASC,
           purchase_id VARCHAR(250) NOT NULL,
           traceId VARCHAR(250) NOT NULL, 
           stockTicker VARCHAR(10) NOT NULL,
           sellVolume INTEGER NOT NULL,
           buyPrice FLOAT(24) NOT NULL,
           buyDate VARCHAR(100) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

c.execute('''
          CREATE TABLE price_event
          (id INTEGER PRIMARY KEY ASC,
           traceId VARCHAR(250) NOT NULL,
           stockTicker VARCHAR(10) NOT NULL,
           timespanUnit VARCHAR(25) NOT NULL,
           timespanLen INTEGER NOT NULL,
           dateStartMonth INTEGER NOT NULL,
           dateStartDay INTEGER NOT NULL,
           dateSort VARCHAR(10) NOT NULL,
           date_created VARCHAR(100) NOT NULL)
          ''')

conn.commit()
conn.close()
