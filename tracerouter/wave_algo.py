import sqlite3

class Router:

	def __init__(self):
		self.conn = sqlite3.connect("TrainSchedule.db")
		self.cursor = self.conn.cursor()
		self.route()

	def route(self):
		pass
		




