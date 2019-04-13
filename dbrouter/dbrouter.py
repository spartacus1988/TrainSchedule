import logging
import sqlite3


class DBrouter:

	def __init__(self):
		logging.basicConfig(filename="TrainSchedule.log",
							format='%(asctime)s   %(name)s  %(message)s',
							datefmt='%m/%d/%Y %I:%M:%S %p',
							filemode='w',
							level=logging.INFO)
		self.logger = logging.getLogger("DBrouter")
		self.logger.info("DBrouter init start...")

		self.conn = sqlite3.connect("TrainSchedule.db")
		self.cursor = self.conn.cursor()

	   #self.read_all()

		self.logger.info("DBrouter init finished")

	def read_all(self):
		self.cursor.execute("""CREATE TABLE IF NOT EXISTS 
							routes (route_id INTEGER PRIMARY KEY ON CONFLICT REPLACE, 
									left_city TEXT NOT NULL,
									right_city TEXT NOT NULL, 
									start_time TEXT NOT NULL,
									end_time TEXT NOT NULL);""")
		self.cursor.execute("SELECT * FROM routes")
		rows = self.cursor.fetchall() 
		return rows

	def get_route_by_route_id(self, route_id):
		self.cursor.execute("SELECT * FROM routes WHERE route_id = " + route_id)
		route = self.cursor.fetchall() 
		#print("route is " + str(route))
		return route



	def save(self, routeNumber, startPoint, endPoint, startTime, endTime):
		print("routeNumber is " + str(routeNumber))
		self.cursor.execute("INSERT OR REPLACE INTO routes VALUES(?, ?, ?, ?, ?)", (routeNumber, startPoint, endPoint, startTime, endTime))
		self.conn.commit()

	def remove(self, routeNumber):
		print("routeNumber is " + str(routeNumber))
		self.cursor.execute("DELETE FROM routes WHERE route_id = " + str(routeNumber))
		self.conn.commit()


