import logging
import sqlite3
import datetime

class Calc:

	def __init__(self, Tracerouter):
		logging.basicConfig(filename="TrainSchedule.log",
							format='%(asctime)s   %(name)s  %(message)s',
							datefmt='%m/%d/%Y %I:%M:%S %p',
							filemode='w',
							level=logging.INFO)
		self.logger = logging.getLogger("Calc")
		self.logger.info("Calc init start...")

		self.conn = sqlite3.connect("TrainSchedule.db")
		self.cursor = self.conn.cursor()

		self.tracerouter = Tracerouter

		self.logger.info("Calc init finished")

	def calculate_data(self, left_city, right_city):		
		shortest_path = self.tracerouter.route(left_city, right_city)
		print(shortest_path)
		start_time = datetime.datetime.now()
		start_time = start_time.strftime("%H:%M")
		
		end_time = datetime.datetime.now()
		end_time = end_time.strftime("%H:%M")

		return shortest_path, start_time, end_time 



