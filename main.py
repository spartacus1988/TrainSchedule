from initializer.initializer import Initializer
from tracerouter.tracerouter import Tracerouter
from dbrouter.dbrouter import DBrouter
from calculator.calculator import Calc
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, GLib

import sqlite3
import datetime
import itertools


class MyWindow(Gtk.Window):

	def __init__(self, Tracerouter, DBrouter, Calc):
		self.tracerouter = Tracerouter
		self.dbrouter = DBrouter
		self.calculator = Calc	
		self.conn = sqlite3.connect("TrainSchedule.db")
		self.cursor = self.conn.cursor()
		self.route = None
		Gtk.Window.__init__(self, title="TrainSchedule")
		self.set_default_size(640, 480)

		self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.add(self.vbox) 

		self.hbox = Gtk.Box()
		self.hboxLabel = Gtk.Box()
		self.hboxButton = Gtk.Box()
		self.lbl_left_city = Gtk.Label("Departure station")
		self.hboxLabel.pack_start(self.lbl_left_city, True, True, 0)
		self.lbl_left_city = Gtk.Label("Destination station")
		self.hboxLabel.pack_start(self.lbl_left_city, True, True, 0)
		self.lbl_left_city = Gtk.Label("Numbre of route")
		self.hboxLabel.pack_start(self.lbl_left_city, True, True, 0)
		self.vbox.pack_start(self.hboxLabel, False, False , 0)
		self.vbox.pack_start(self.hbox, False, False , 0)
		self.vbox.pack_start(self.hboxButton, False, False , 0)


		self.scrolledwindow = Gtk.ScrolledWindow()
		self.scrolledwindow.set_hexpand(True)
		self.scrolledwindow.set_vexpand(True)

		self.textview = Gtk.TextView()
		self.textview.set_editable(False)
		self.textview.props.wrap_mode=2 #2 = Gtk.WRAP_WORD
		self.textview.props.justification=0 #0 = Gtk.JUSTIFY_LEFT
		self.textbuffer = self.textview.get_buffer()
		self.textbuffer.set_text("TrainSchedule\r\n")
		self.scrolledwindow.add(self.textview)
		self.vbox.pack_start(self.scrolledwindow, True, True, 0)


		self.city_store = Gtk.ListStore(str)
		self.init_db_cities_data()
		self.city_combo_left = Gtk.ComboBox.new_with_model_and_entry(self.city_store)
		self.city_combo_left.connect("changed", self.on_city_combo_changed)
		self.city_combo_left.set_entry_text_column(0)
		self.city_combo_left.set_active(0)
		self.hbox.pack_start(self.city_combo_left, True, True, 0)

		self.city_combo_right = Gtk.ComboBox.new_with_model_and_entry(self.city_store)
		self.city_combo_right.connect("changed", self.on_city_combo_changed)
		self.city_combo_right.set_entry_text_column(0)
		self.city_combo_right.set_active(2)
		self.hbox.pack_start(self.city_combo_right, True, True, 0)

		self.route_store = Gtk.ListStore(str)
		self.init_db_route_data()
		self.route_combo = Gtk.ComboBox.new_with_model_and_entry(self.route_store)
		self.route_combo.connect("changed", self.on_route_combo_changed)
		self.route_combo.set_entry_text_column(0)
		self.hbox.pack_start(self.route_combo, True, True, 0)

		self.buttonSave = Gtk.Button(label="Save")
		self.buttonSave.connect("clicked", self.on_buttonSave_clicked)
		self.hboxButton.pack_start(self.buttonSave, True, True, 0)

		self.buttonAdd = Gtk.Button(label="Add new")
		self.buttonAdd.connect("clicked", self.on_buttonAdd_clicked)
		self.hboxButton.pack_start(self.buttonAdd, True, True, 0)

		self.buttonRemove = Gtk.Button(label="Remove")
		self.buttonRemove.connect("clicked", self.on_buttonRemove_clicked)
		self.hboxButton.pack_start(self.buttonRemove, True, True, 0)

	def on_buttonSave_clicked(self, widget):
		print("Saving...")

		left_city = self.get_left_city()
		right_city = self.get_right_city()
		
		shortest_path, start_time, end_time = self.calculator.calculate_data(left_city, right_city)

		end_iter = self.textbuffer.get_end_iter()
		if left_city != right_city:				
			#print("self.route = %s" % str(self.route))
			#print("len(self.route_store) = %s" % str(len(self.route_store)))
			if len(self.route_store) == 0:
				self.route = None
				self.textbuffer.insert(end_iter, "Please add first a new route\r\n\r\n")
			elif self.route is None and len(self.route_store) > 0:
				self.textbuffer.insert(end_iter, "Please select a route\r\n\r\n")
			else:
				shortest_path_str = "-->".join(str(item) for item in shortest_path)
				self.dbrouter.save(int(self.route), left_city, right_city, start_time, end_time)			
				self.textbuffer.insert(end_iter, "Route №" + str(self.route) + " from " + left_city +
				" through "	+ shortest_path_str + 
				" to " + right_city + " departure at " + str(start_time) + 
				" arrival at " + str(end_time) + " was saved in databse\r\n\r\n")
				self.print_details_of_route(shortest_path)
		else:
			self.textbuffer.insert(end_iter, "Please select a different cities\r\n\r\n")

	def get_left_city(self):
		left_tree_iter = self.city_combo_left.get_active_iter()
		if left_tree_iter is not None:
			left_model = self.city_combo_left.get_model()
			left_city = left_model[left_tree_iter][0]
		print("Selected: left city=%s" % left_city)
		return left_city

	def get_right_city(self):
		right_tree_iter = self.city_combo_right.get_active_iter()
		if right_tree_iter is not None:
			right_model = self.city_combo_right.get_model()
			right_city = right_model[right_tree_iter][0]
		print("Selected: right city=%s" % right_city)
		return right_city

	def on_buttonAdd_clicked(self, widget):
		print("Adding...")

		left_city = self.get_left_city()
		right_city = self.get_right_city()

		shortest_path, start_time, end_time = self.calculator.calculate_data(left_city, right_city)
		end_iter = self.textbuffer.get_end_iter()

		if left_city != right_city:			
			if len(self.route_store) == 0:
				shortest_path_str = "-->".join(str(item) for item in shortest_path)
				self.route = 1
				self.route_store.append([str(1)])
				self.dbrouter.save(int(self.route), left_city, right_city, start_time, end_time)			
				self.textbuffer.insert(end_iter, "New route number " +'№1' + " from " + left_city +
				" through "	+ shortest_path_str +
				" to " + right_city + " departure at " + start_time + 
				" arrival at " + end_time + " was added to databse\r\n")
				self.print_details_of_route(shortest_path)
			else:
				shortest_path_str = "-->".join(str(item) for item in shortest_path)
				route_numbers_list = list()
				item = self.route_store.get_iter_first()

				while(item != None):
					route_numbers_list.append (self.route_store.get_value (item, 0))
					item = self.route_store.iter_next(item)
				route_numbers_list = list(map(int, route_numbers_list))
				current_number = int(max(route_numbers_list)) + 1

				self.dbrouter.save(current_number, left_city, right_city, start_time, end_time)
				self.route_store.append([str(current_number)])			
				self.textbuffer.insert(end_iter, "New route №" + str(current_number) + " from " + left_city +
				" through "	+ shortest_path_str +
				" to " + right_city + " departure at " + str(start_time) + 
				" arrival at " + str(end_time) + " was added to databse\r\n")
				self.print_details_of_route(shortest_path)								
		else:
			self.textbuffer.insert(end_iter, "Please select a different cities\r\n\r\n")

	def print_details_of_route(self, shortest_path):
		end_iter = self.textbuffer.get_end_iter()
		i = 0
		j = 2
		total_time_to_distance = datetime.timedelta(hours=float(0))
		for item in shortest_path:
			string_item = "-->".join(str(item) for item in shortest_path[i:j])
			print("string_item is " + str(string_item))
			first_city, second_city = string_item.split('-->')
			time_to_distance_str, time_to_distance = self.calculator.get_time(first_city, second_city)
			total_time_to_distance += time_to_distance
			self.textbuffer.insert(end_iter, "Time to distance between " + string_item + " is: " + time_to_distance_str + "\r\n")
			end_iter = self.textbuffer.get_end_iter()
			i+=1
			j+=1
			if j > len(shortest_path):
				time_to_stop = 0.084 # 5 min
				time_to_stops = time_to_stop * (i-1)
				time_to_stops = datetime.timedelta(hours=float(time_to_stops))
				total_time = total_time_to_distance + time_to_stops

				time_to_stops_str = (datetime.datetime(2000,1,1)+time_to_stops).strftime("%H:%M")
				total_time_to_distance_str = (datetime.datetime(2000,1,1)+total_time_to_distance).strftime("%H:%M")
				total_time_str = (datetime.datetime(2000,1,1)+total_time).strftime("%H:%M")

				end_iter = self.textbuffer.get_end_iter()
				self.textbuffer.insert(end_iter, "Total time to stops is: " + time_to_stops_str + "\r\n")
				end_iter = self.textbuffer.get_end_iter()
				self.textbuffer.insert(end_iter, "Total time to distance is: " + total_time_to_distance_str + "\r\n")
				end_iter = self.textbuffer.get_end_iter()
				self.textbuffer.insert(end_iter, "Total time is: " + total_time_str + "\r\n\r\n")
				break
			else:
				end_iter = self.textbuffer.get_end_iter()
				time_to_stop = 0.084 # 5 min
				time_to_stop = datetime.timedelta(hours=float(time_to_stop))
				time_to_stop_str = (datetime.datetime(2000,1,1)+time_to_stop).strftime("%H:%M")
				#print("time_to_stop is " + str(time_to_stop_str))
				self.textbuffer.insert(end_iter, "Time to stop is: " + time_to_stop_str + "\r\n")

	def on_buttonRemove_clicked(self, widget):
		print("Removing...")
		end_iter = self.textbuffer.get_end_iter()
		if self.route is None and len(self.route_store) == 0:
			self.textbuffer.insert(end_iter, "Nothing to delete, you first need to add a new route.\r\n\r\n")
		elif self.route is None and len(self.route_store) > 0:
			print("len of self.route_store is " + str(len(self.route_store)))
			print("self.route is " + str(self.route))
			self.textbuffer.insert(end_iter, "Please select a route\r\n\r\n")
		else:
			focus = self.route_combo.get_active_iter()
			if focus is not None:
				self.dbrouter.remove(int(self.route))
				self.route_store.remove(focus)		
				self.textbuffer.insert(end_iter, "Route number №" + str(self.route) +
				" was deleted from database\r\n\r\n")
			else:
				self.textbuffer.insert(end_iter, "Route number №" + str(self.route) +
				" has already been deleted previously\r\n\r\n")
		
	def on_city_combo_changed(self, combo):
		tree_iter = combo.get_active_iter()
		if tree_iter is not None:
			model = combo.get_model()
			city = model[tree_iter][0]
			

	def on_route_combo_changed(self, combo):
		print("route_combo was changed!!!")
		tree_iter = combo.get_active_iter()
		if tree_iter is not None:
			model = combo.get_model()
			self.route = model[tree_iter][0]

			city_number_left, city_number_right = self.get_city_number_by_route_id(self.route)
			print("city_number_left is " + str(city_number_left))
			print("city_number_right is " + str(city_number_right))

			self.city_combo_left.set_active(city_number_left-1)
			self.city_combo_right.set_active(city_number_right-1)


	def get_city_number_by_route_id(self, route_id):
		route = self.dbrouter.get_route_by_route_id(route_id)
		route_id, left_city, right_city, start_time,  end_time = route[0]

		self.cursor.execute("SELECT * FROM cities WHERE city_name = '" + str(left_city) + "' ")
		city_list = self.cursor.fetchall() 
		city_number_left, city_name_left = city_list[0]

		self.cursor.execute("SELECT * FROM cities WHERE city_name = '" + str(right_city) + "' ")
		city_list = self.cursor.fetchall() 
		city_number_right, city_name_right = city_list[0]

		return city_number_left, city_number_right


	def init_db_cities_data(self):
		self.cursor.execute("SELECT * FROM cities")
		rows = self.cursor.fetchall()
		for row in rows:
			self.city_store.append([row[1]])

	def init_db_route_data(self):	
		rows = self.dbrouter.read_all()
		for row in rows:
			self.route_store.append([str(row[0])])

		

if __name__ == '__main__':

	initializer = Initializer()
	Graph = initializer.G
	tracerouter = Tracerouter(Graph)
	dbrouter = DBrouter()
	calculator = Calc(tracerouter)
	
	win = MyWindow(tracerouter, dbrouter, calculator)
	win.connect("destroy", Gtk.main_quit)
	win.show_all()
	Gtk.main()
