import sqlite3
import networkx as nx

class Router:

	def __init__(self):
		self.conn = sqlite3.connect("TrainSchedule.db")
		self.cursor = self.conn.cursor()
		self.route()

	def route(self):
		G = nx.Graph()
		#1 Torzhok
		G.add_edge('Torzhok', 'Likhoslavl', weight=1)
		G.add_edge('Torzhok', 'Kuvshinovo', weight=1)
		G.add_edge('Torzhok', 'Staritsa', weight=1)

		#2 Likhoslavl
		G.add_edge('Likhoslavl', 'Tver', weight=1)
		G.add_edge('Likhoslavl', 'Spirovo', weight=1)

		#4 Vyshny Volochek
		G.add_edge('Vyshny Volochek', 'Spirovo', weight=1)
		G.add_edge('Vyshny Volochek', 'Bologoye', weight=1)

		#6 Bologoye
		G.add_edge('Bologoye', 'Firovo', weight=1)
		G.add_edge('Bologoye', 'Udomlya', weight=1)

		#7 Firovo
		G.add_edge('Firovo', 'Ostashkov', weight=1)

		#8 Ostashkov
		G.add_edge('Ostashkov', 'Peno', weight=1)

		#9 Peno
		G.add_edge('Peno', 'Selijarovo', weight=1)
		G.add_edge('Peno', 'Andreapol', weight=1)

		#10 Selijarovo
		G.add_edge('Selijarovo', 'Kuvshinovo', weight=1)

		#12 Staritsa
		G.add_edge('Staritsa', 'Rzhev', weight=1)

		#13 Rzhev
		G.add_edge('Rzhev', 'Olenino', weight=1)

		#14 Olenino
		G.add_edge('Olenino', 'Nelidovo', weight=1)

		#15 Nelidovo
		G.add_edge('Nelidovo', 'Zap Dvina', weight=1)
		G.add_edge('Nelidovo', 'Zharkovsky', weight=1)

		#16 Zap Dvina
		G.add_edge('Zap Dvina', 'Zharkovsky', weight=1)

		#18 Andreapol
		G.add_edge('Andreapol', 'Toropets', weight=1)

		#20 Udomlya
		G.add_edge('Udomlya', 'Maksatiha', weight=1)

		#21 Maksatiha
		G.add_edge('Maksatiha', 'Bezhetsk', weight=1)

		#22 Bezhetsk
		G.add_edge('Bezhetsk', 'Sonkovo', weight=1)

		#23 Sonkovo
		G.add_edge('Sonkovo', 'Kashin', weight=1)
		G.add_edge('Sonkovo', 'Krasnyy Kholm', weight=1)

		#24 Kashin
		G.add_edge('Kashin', 'Kalyazin', weight=1)

		#25 Kalyazin
		G.add_edge('Kalyazin', 'Savyolovo', weight=1)

		#27 Sandovo
		G.add_edge('Sandovo', 'Krasnyy Kholm', weight=1)
		G.add_edge('Sandovo', 'Vesegonsk', weight=1)

		#28 Krasnyy Kholm
		G.add_edge('Krasnyy Kholm', 'Vesegonsk', weight=1)


		pass
		




