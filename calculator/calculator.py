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
		shortest_path, shortest_path_edge_distance = self.tracerouter.route(left_city, right_city)
		print(shortest_path)
		print(shortest_path_edge_distance)

		number_of_stops = len(shortest_path) - 2
		time_to_stop = 0.0833333 # 5 min
		time_to_stops = time_to_stop * number_of_stops
		time_to_stops = datetime.timedelta(hours=float(time_to_stops))
		time_to_stops_str = (datetime.datetime(2000,1,1)+time_to_stops).strftime("%H:%M")
		print("time_to_stops is " + str(time_to_stops_str))

		start_time = datetime.datetime.now()
		print("start_time is " + str(start_time))
		start_time_str = start_time.strftime("%H:%M")
		print("start_time is " + str(start_time_str))

		train_speed = 60
		time_to_distance = shortest_path_edge_distance/train_speed
		print("time_to_distance is " + str(time_to_distance))
		time_to_distance = datetime.timedelta(hours=float(time_to_distance))
		time_to_distance_str = (datetime.datetime(2000,1,1)+time_to_distance).strftime("%H:%M")
		print("time_to_distance is " + str(time_to_distance_str))

		end_time = start_time + time_to_distance + time_to_stops
		end_time_str = end_time.strftime("%H:%M")
		print("end_time is " + str(end_time_str))
		#end_time = datetime.datetime.now()
		#end_time = end_time.strftime("%H:%M")

		return shortest_path, start_time_str, end_time_str 

	def get_time(self, from_city, to_city):
		train_speed = 60
		shortest_path, shortest_path_edge_distance = self.tracerouter.route(from_city, to_city)
		time_to_distance = shortest_path_edge_distance/train_speed
		time_to_distance = datetime.timedelta(hours=float(time_to_distance))
		time_to_distance_str = (datetime.datetime(2000,1,1)+time_to_distance).strftime("%H:%M")
		return time_to_distance_str
