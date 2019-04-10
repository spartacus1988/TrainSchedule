import sqlite3

conn = sqlite3.connect("TrainSchedule.db")

# Create table
cursor.execute("""create table if not exists cities (name text)""")

#cursor.execute("""CREATE TABLE cities
#                  (name text)
#               """)


cities = [('Torzhok'),
          ('Likhoslavl'),
          ('Tver'),
          ('Vyshny Volochek'),
          ('Spirovo'),
          ('Bologoye'),
          ('Firovo'),
          ('Ostashkov'),
          ('Peno'),
          ('Selijarovo'),
          ('Kuvshinovo'),
          ('Staritsa'),
          ('Rzhev'),
          ('Olenino'),
          ('Nelidovo'),
          ('Zap Dvina'),
          ('Zharkovsky'),
          ('Andreapol'),
          ('Toropets'),
          ('Udomlya'),
          ('Maksatiha'),
          ('Bezhetsk'),
          ('Sonkovo'),
          ('Kashin'),
          ('Kalyazin'),
          ('Savyolovo'),
          ('Sandovo'),
          ('Krasnyy Kholm'),
          ('Vesegonsk')]
 
cursor.executemany("INSERT INTO albums VALUES (?,?,?,?,?)", albums)
conn.commit()