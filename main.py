from initializer.initializer import Initializer
from tracerouter.tracerouter import Tracerouter
from dbrouter.dbrouter import DBrouter
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, GLib

import sqlite3
import datetime


class MyWindow(Gtk.Window):

	def __init__(self, Tracerouter, DBrouter):
		self.tracerouter = Tracerouter
		self.dbrouter = DBrouter
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
		#self.textview.set_wrap_mode(Gtk.WRAP_WORD)
		self.textview.props.wrap_mode=2 #2 = Gtk.WRAP_WORD
		#self.textview.set_justification(Gtk.JUSTIFY_LEFT)
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
		#self.route_combo.set_active(0)
		self.route_combo.set_entry_text_column(0)
		#self.route_combo.set_active(0)
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
		
		left_city, right_city, shortest_path, start_time, end_time = self.calculate_data()

		if left_city != right_city:		
			end_iter = self.textbuffer.get_end_iter()
			if self.route is None and len(self.route_store) == 0:
				self.textbuffer.insert(end_iter, "Please add first a new route\r\n")
			elif self.route is None and len(self.route_store) > 0:
				print("len of self.route_store is " + str(len(self.route_store)))
				print("self.route is " + str(self.route))
				self.textbuffer.insert(end_iter, "Please select a route\r\n")
			else:
				self.dbrouter.save(int(self.route), left_city, right_city, start_time, end_time)			
				self.textbuffer.insert(end_iter, "New route from " + left_city +
				" to " + right_city + " departure at " + start_time + 
				" arrival at " + end_time + " was added to databse\r\n")

	def on_buttonAdd_clicked(self, widget):
		print("Adding...")
		
		left_city, right_city, shortest_path, start_time, end_time = self.calculate_data()

		if left_city != right_city:		
			end_iter = self.textbuffer.get_end_iter()
			if self.route is None and len(self.route_store) == 0:
				#print("len of self.route_store is " + str(len(self.route_store)))
				self.route = 1
				self.route_store.append([str(1)])
				self.route_combo.set_active(0)
				self.dbrouter.save(int(self.route), left_city, right_city, start_time, end_time)			
				self.textbuffer.insert(end_iter, "New route from " + left_city +
				" to " + right_city + " departure at " + start_time + 
				" arrival at " + end_time + " was added to databse\r\n")
			else:
				self.dbrouter.save(len(self.route_store)+1, left_city, right_city, start_time, end_time)
				self.route_store.append([str(len(self.route_store)+1)])			
				self.textbuffer.insert(end_iter, "New route from " + left_city +
				" to " + right_city + " departure at " + start_time + 
				" arrival at " + end_time + " was added to databse\r\n")

	def calculate_data(self):
		left_tree_iter = self.city_combo_left.get_active_iter()
		if left_tree_iter is not None:
			left_model = self.city_combo_left.get_model()
			left_city = left_model[left_tree_iter][0]
		print("Selected: left city=%s" % left_city)

		right_tree_iter = self.city_combo_right.get_active_iter()
		if right_tree_iter is not None:
			right_model = self.city_combo_right.get_model()
			right_city = right_model[right_tree_iter][0]
		print("Selected: right city=%s" % right_city)

		shortest_path = self.tracerouter.route(left_city, right_city)
		start_time = datetime.datetime.now()
		start_time = start_time.strftime("%H:%M")
		end_time = datetime.datetime.now()
		end_time = end_time.strftime("%H:%M")

		return left_city, right_city, shortest_path, start_time, end_time



	def on_buttonRemove_clicked(self, widget):
		print("Removing...")
		end_iter = self.textbuffer.get_end_iter()
		if self.route is None and len(self.route_store) == 0:
			self.textbuffer.insert(end_iter, "Nothing to delete, you first need to add a new route.\r\n")
		elif self.route is None and len(self.route_store) > 0:
			print("len of self.route_store is " + str(len(self.route_store)))
			print("self.route is " + str(self.route))
			self.textbuffer.insert(end_iter, "Please select a route\r\n")
		else:
			focus = self.route_combo.get_active_iter()
			if focus is not None:
				self.dbrouter.remove(int(self.route))
				self.route_store.remove(focus)		
				self.textbuffer.insert(end_iter, "Route number " + str(self.route) +
				" was deleted from database\r\n")
			else:
				self.textbuffer.insert(end_iter, "Route number " + str(self.route) +
				" has already been deleted previously\r\n")
		
	def on_city_combo_changed(self, combo):
		tree_iter = combo.get_active_iter()
		if tree_iter is not None:
			model = combo.get_model()
			city = model[tree_iter][0]
			

	def on_route_combo_changed(self, combo):
		print("route_combo was changed!!!")
		#print("self.route is " + str(self.route))
		tree_iter = combo.get_active_iter()
		if tree_iter is not None:
			model = combo.get_model()
			self.route = model[tree_iter][0]
			#print("self.route is " + str(self.route))
			

			city_number_left, city_number_right = self.get_city_number_by_route_id(self.route)
			print("city_number_left is " + str(city_number_left))
			print("city_number_right is " + str(city_number_right))

			self.city_combo_left.set_active(city_number_left-1)
			self.city_combo_right.set_active(city_number_right-1)


	def get_city_number_by_route_id(self, route_id):
		route = self.dbrouter.get_route_by_route_id(route_id)
		#print("route is " + str(route))
		route_id, left_city, right_city, start_time,  end_time = route[0]
		#print("left_city is " + str(left_city))

		self.cursor.execute("SELECT * FROM cities WHERE city_name = '" + str(left_city) + "' ")
		city_list = self.cursor.fetchall() 
		city_number_left, city_name_left = city_list[0]
		#print("city_number_left is " + str(city_number_left))

		self.cursor.execute("SELECT * FROM cities WHERE city_name = '" + str(right_city) + "' ")
		city_list = self.cursor.fetchall() 
		city_number_right, city_name_right = city_list[0]
		#print("city_number_right is " + str(city_number_right))

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
			#print(row[0])
		



if __name__ == '__main__':

	initializer = Initializer()
	Graph = initializer.G
	tracerouter = Tracerouter(Graph)
	dbrouter = DBrouter()

	#tracerouter.route('Torzhok', 'Kalyazin')


	
	win = MyWindow(tracerouter, dbrouter)
	win.connect("destroy", Gtk.main_quit)
	win.show_all()
	Gtk.main()
