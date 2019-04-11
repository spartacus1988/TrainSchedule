import sqlite3
import networkx as nx
#import matplotlib
import matplotlib.pyplot as plt

class Router:

	def __init__(self, Graph):
		self.G = Graph
		self.conn = sqlite3.connect("TrainSchedule.db")
		self.cursor = self.conn.cursor()
		self.route()

	def route(self):
			
		shortest_path = nx.shortest_path(self.G, 'Torzhok', 'Kalyazin')
		print(shortest_path)

		shortest_path = nx.shortest_path(self.G, 'Zap Dvina', 'Sonkovo')
		print(shortest_path)

