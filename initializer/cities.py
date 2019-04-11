import sqlite3
import networkx as nx

class CitiesInitializer:

	def __init__(self):
		self.conn = sqlite3.connect("TrainSchedule.db")
		self.cursor = self.conn.cursor()
		self.create_cities_table()
		self.create_neighbors_table()
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

	def create_simple_graph(self):
		self.G = nx.Graph()
		#1 Torzhok
		self.G.add_edge('Torzhok', 'Likhoslavl', weight=1)
		self.G.add_edge('Torzhok', 'Kuvshinovo', weight=1)
		self.G.add_edge('Torzhok', 'Staritsa', weight=1)

		#2 Likhoslavl
		self.G.add_edge('Likhoslavl', 'Tver', weight=1)
		self.G.add_edge('Likhoslavl', 'Spirovo', weight=1)

		#4 Vyshny Volochek
		self.G.add_edge('Vyshny Volochek', 'Spirovo', weight=1)
		self.G.add_edge('Vyshny Volochek', 'Bologoye', weight=1)

		#6 Bologoye
		self.G.add_edge('Bologoye', 'Firovo', weight=1)
		self.G.add_edge('Bologoye', 'Udomlya', weight=1)

		#7 Firovo
		self.G.add_edge('Firovo', 'Ostashkov', weight=1)

		#8 Ostashkov
		self.G.add_edge('Ostashkov', 'Peno', weight=1)

		#9 Peno
		self.G.add_edge('Peno', 'Selijarovo', weight=1)
		self.G.add_edge('Peno', 'Andreapol', weight=1)

		#10 Selijarovo
		self.G.add_edge('Selijarovo', 'Kuvshinovo', weight=1)

		#12 Staritsa
		self.G.add_edge('Staritsa', 'Rzhev', weight=1)

		#13 Rzhev
		self.G.add_edge('Rzhev', 'Olenino', weight=1)

		#14 Olenino
		self.G.add_edge('Olenino', 'Nelidovo', weight=1)

		#15 Nelidovo
		self.G.add_edge('Nelidovo', 'Zap Dvina', weight=1)
		self.G.add_edge('Nelidovo', 'Zharkovsky', weight=1)

		#16 Zap Dvina
		self.G.add_edge('Zap Dvina', 'Zharkovsky', weight=1)

		#18 Andreapol
		self.G.add_edge('Andreapol', 'Toropets', weight=1)

		#20 Udomlya
		self.G.add_edge('Udomlya', 'Maksatiha', weight=1)

		#21 Maksatiha
		self.G.add_edge('Maksatiha', 'Bezhetsk', weight=1)

		#22 Bezhetsk
		self.G.add_edge('Bezhetsk', 'Sonkovo', weight=1)

		#23 Sonkovo
		self.G.add_edge('Sonkovo', 'Kashin', weight=1)
		self.G.add_edge('Sonkovo', 'Krasnyy Kholm', weight=1)

		#24 Kashin
		self.G.add_edge('Kashin', 'Kalyazin', weight=1)

		#25 Kalyazin
		self.G.add_edge('Kalyazin', 'Savyolovo', weight=1)

		#27 Sandovo
		self.G.add_edge('Sandovo', 'Krasnyy Kholm', weight=1)
		self.G.add_edge('Sandovo', 'Vesegonsk', weight=1)

		#28 Krasnyy Kholm
		self.G.add_edge('Krasnyy Kholm', 'Vesegonsk', weight=1)


		#nx.draw_networkx(self.G)
		#plt.show()
		return self.G





