import sqlite3
import networkx as nx
import matplotlib.pyplot as plt

class CitiesInitializer:

	def __init__(self):
		self.conn = sqlite3.connect("TrainSchedule.db")
		self.cursor = self.conn.cursor()
		self.create_cities_table()
		self.create_neighbors_table()
		self.create_distances_table()
		self.G = self.create_simple_graph()

	def create_cities_table(self):
		self.cursor.execute("DROP TABLE IF EXISTS cities")
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS 
							cities (city_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE ON CONFLICT REPLACE, 
									city_name TEXT NOT NULL UNIQUE);""")

		cities   = [(1, 'Torzhok'),
					(2, 'Likhoslavl'),
					(3, 'Tver'),
					(4, 'Vyshny Volochek'),
					(5, 'Spirovo'),
					(6, 'Bologoye'),
					(7, 'Firovo'),
					(8, 'Ostashkov'),
					(9, 'Peno'),
					(10, 'Selijarovo'),
					(11, 'Kuvshinovo'),
					(12, 'Staritsa'),
					(13, 'Rzhev'),
					(14, 'Olenino'),
					(15, 'Nelidovo'),
					(16, 'Zap Dvina'),
					(17, 'Zharkovsky'),
					(18, 'Andreapol'),
					(19, 'Toropets'),
					(20, 'Udomlya'),
					(21, 'Maksatiha'),
					(22, 'Bezhetsk'),
					(23, 'Sonkovo'),
					(24, 'Kashin'),
					(25, 'Kalyazin'),
					(26, 'Savyolovo'),
					(27, 'Sandovo'),
					(28, 'Krasnyy Kholm'),
					(29, 'Vesegonsk')]

		self.cursor.executemany("INSERT INTO cities VALUES(?, ?)", cities)
		self.conn.commit()

	def create_neighbors_table(self):
		self.cursor.execute("DROP TABLE IF EXISTS neighbors")
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS 
							neighbors (city_id INTEGER PRIMARY KEY UNIQUE ON CONFLICT REPLACE, 
									   first_neighbor INTEGER NOT NULL,
									   second_neighbor INTEGER,
									   third_neighbor INTEGER);""")
		neighbors = [(1, 11, 2, 12),
					(2, 1, 3, 5),
					(3, 2, None, None),
					(4, 5, 6, None),
					(5, 4, 2, None),
					(6, 4, 7, 20),
					(7, 6, 8, None),
					(8, 7, 9, None),
					(9, 8, 10, 18),
					(10, 9, 11, None),
					(11, 10, 1, None),
					(12, 1, 13, None),
					(13, 12, 14, None),
					(14, 13, 15, None ),
					(15, 16, 14, 17),
					(16, 15, 17, None),
					(17, 15, 16, None),
					(18, 19, 9, None),
					(19, 18, None, None),
					(20, 21, 6, None),
					(21, 20, 22, None),
					(22, 21, 23, None),
					(23, 24, 28, 22),
					(24, 25, 23, None),
					(25, 24, 26, None),
					(26, 25, None, None),
					(27, 28, 29, None),
					(28, 27, 23, 29),
					(29, 28, 27, None)]

		self.cursor.executemany("INSERT INTO neighbors VALUES(?, ?, ?, ?)", neighbors)
		self.conn.commit()

	def create_distances_table(self):
		self.cursor.execute("DROP TABLE IF EXISTS distances")
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS 
							distances (distance_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE ON CONFLICT REPLACE, 
										city_name_1 TEXT NOT NULL,
										city_name_2 TEXT NOT NULL,
										distance INTEGER NOT NULL);""")

		distances   = [	(1, 'Torzhok', 'Likhoslavl', 34),
						(2, 'Torzhok', 'Kuvshinovo', 53),
						(3, 'Torzhok', 'Staritsa', 59),
						(4, 'Likhoslavl', 'Tver', 40),
						(5, 'Likhoslavl', 'Spirovo', 44),
						(6, 'Vyshny Volochek', 'Spirovo', 31),
						(7, 'Vyshny Volochek', 'Bologoye', 45),
						(8, 'Bologoye', 'Firovo', 50),
						(9, 'Bologoye', 'Udomlya', 56),
						(10, 'Firovo', 'Ostashkov', 51),
						(11, 'Ostashkov', 'Peno', 33),
						(12, 'Peno', 'Selijarovo', 44),
						(13, 'Peno', 'Andreapol', 42),
						(14, 'Selijarovo', 'Kuvshinovo', 48),
						(15, 'Staritsa', 'Rzhev', 47),
						(16, 'Rzhev', 'Olenino', 53),
						(17, 'Olenino', 'Nelidovo', 44),
						(18, 'Nelidovo', 'Zap Dvina', 43),
						(19, 'Nelidovo', 'Zharkovsky', 52),
						(20, 'Zap Dvina', 'Zharkovsky', 47),
						(21, 'Andreapol', 'Toropets', 42),
						(22, 'Udomlya', 'Maksatiha', 53),
						(23, 'Maksatiha', 'Bezhetsk', 48),
						(24, 'Bezhetsk', 'Sonkovo', 28),
						(25, 'Sonkovo', 'Kashin', 54),
						(26, 'Sonkovo', 'Krasnyy Kholm', 31),
						(27, 'Kashin', 'Kalyazin', 18),
						(28, 'Kalyazin', 'Savyolovo', 54),
						(29, 'Sandovo', 'Krasnyy Kholm', 61),
						(30, 'Sandovo', 'Vesegonsk', 55),
						(31, 'Krasnyy Kholm', 'Vesegonsk', 68)
						]

		self.cursor.executemany("INSERT INTO distances VALUES(?, ?, ?, ?)", distances)
		self.conn.commit()

	def create_simple_graph(self):
		self.G = nx.Graph()
		#1 Torzhok
		self.G.add_edge('Torzhok', 'Likhoslavl', weight=34)
		self.G.add_edge('Torzhok', 'Kuvshinovo', weight=53)
		self.G.add_edge('Torzhok', 'Staritsa', weight=59)

		#2 Likhoslavl
		self.G.add_edge('Likhoslavl', 'Tver', weight=40)
		self.G.add_edge('Likhoslavl', 'Spirovo', weight=44)

		#4 Vyshny Volochek
		self.G.add_edge('Vyshny Volochek', 'Spirovo', weight=31)
		self.G.add_edge('Vyshny Volochek', 'Bologoye', weight=45)

		#6 Bologoye
		self.G.add_edge('Bologoye', 'Firovo', weight=50)
		self.G.add_edge('Bologoye', 'Udomlya', weight=56)

		#7 Firovo
		self.G.add_edge('Firovo', 'Ostashkov', weight=51)

		#8 Ostashkov
		self.G.add_edge('Ostashkov', 'Peno', weight=33)

		#9 Peno
		self.G.add_edge('Peno', 'Selijarovo', weight=44)
		self.G.add_edge('Peno', 'Andreapol', weight=42)

		#10 Selijarovo
		self.G.add_edge('Selijarovo', 'Kuvshinovo', weight=48)

		#12 Staritsa
		self.G.add_edge('Staritsa', 'Rzhev', weight=47)

		#13 Rzhev
		self.G.add_edge('Rzhev', 'Olenino', weight=53)

		#14 Olenino
		self.G.add_edge('Olenino', 'Nelidovo', weight=44)

		#15 Nelidovo
		self.G.add_edge('Nelidovo', 'Zap Dvina', weight=43)
		self.G.add_edge('Nelidovo', 'Zharkovsky', weight=52)

		#16 Zap Dvina
		self.G.add_edge('Zap Dvina', 'Zharkovsky', weight=47)

		#18 Andreapol
		self.G.add_edge('Andreapol', 'Toropets', weight=42)

		#20 Udomlya
		self.G.add_edge('Udomlya', 'Maksatiha', weight=53)

		#21 Maksatiha
		self.G.add_edge('Maksatiha', 'Bezhetsk', weight=48)

		#22 Bezhetsk
		self.G.add_edge('Bezhetsk', 'Sonkovo', weight=28)

		#23 Sonkovo
		self.G.add_edge('Sonkovo', 'Kashin', weight=54)
		self.G.add_edge('Sonkovo', 'Krasnyy Kholm', weight=31)

		#24 Kashin
		self.G.add_edge('Kashin', 'Kalyazin', weight=18)

		#25 Kalyazin
		self.G.add_edge('Kalyazin', 'Savyolovo', weight=54)

		#27 Sandovo
		self.G.add_edge('Sandovo', 'Krasnyy Kholm', weight=61)
		self.G.add_edge('Sandovo', 'Vesegonsk', weight=55)

		#28 Krasnyy Kholm
		self.G.add_edge('Krasnyy Kholm', 'Vesegonsk', weight=68)


		#nx.draw_networkx(self.G, weight='weight')

		#print(self.G.edges(data=True))
		#print(len(self.G.edges(data=True)))
		
		#plt.show()
		return self.G





