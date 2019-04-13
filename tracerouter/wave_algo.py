import sqlite3
import networkx as nx
#import matplotlib
import matplotlib.pyplot as plt

class Router:

	def __init__(self, Graph):
		self.G = Graph
		self.conn = sqlite3.connect("TrainSchedule.db")
		self.cursor = self.conn.cursor()
		#self.route()

	def route(self, startPoint, endPoint):		
		shortest_path = nx.shortest_path(self.G, startPoint, endPoint)
		#print(shortest_path)
		return shortest_path


