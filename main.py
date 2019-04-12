from initializer.initializer import Initializer
from tracerouter.tracerouter import Tracerouter
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, GLib

import sqlite3


class MyWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="TrainSchedule")
		self.set_default_size(640, 480)

		self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.add(self.vbox) 

		self.hbox = Gtk.Box()
		self.vbox.pack_start(self.hbox, False, False , 0)

		self.entry = Gtk.Entry()
		self.entry.set_editable(False)
		self.entry.set_text("TrainSchedule")
		self.vbox.pack_start(self.entry, True, True, 0)


		self.city_store = Gtk.ListStore(str)
		self.init_db_data()
		self.city_combo_left = Gtk.ComboBox.new_with_model_and_entry(self.city_store)
		self.city_combo_left.connect("changed", self.on_city_combo_changed)
		self.city_combo_left.set_entry_text_column(0)
		self.city_combo_left.set_title("StartPoint")
		self.hbox.pack_start(self.city_combo_left, False, False, 0)

		self.city_combo_right = Gtk.ComboBox.new_with_model_and_entry(self.city_store)
		self.city_combo_right.connect("changed", self.on_city_combo_changed)
		self.city_combo_right.set_entry_text_column(0)
		self.hbox.pack_start(self.city_combo_right, False, False, 0)

		

		self.buttonAdd = Gtk.Button(label="Add")
		self.buttonAdd.connect("clicked", self.on_buttonAdd_clicked)
		self.hbox.pack_start(self.buttonAdd, True, True, 0)

		self.buttonSave = Gtk.Button(label="Save")
		self.buttonSave.connect("clicked", self.on_buttonSave_clicked)
		self.hbox.pack_start(self.buttonSave, True, True, 0)

	def on_buttonAdd_clicked(self, widget):
		print("Adding...")

	def on_buttonSave_clicked(self, widget):
		print("Saving...")

	def on_city_combo_changed(self, combo):
		tree_iter = combo.get_active_iter()
		if tree_iter is not None:
			model = combo.get_model()
			country = model[tree_iter][0]
			print("Selected: country=%s" % country)

	def init_db_data(self):
		self.conn = sqlite3.connect("TrainSchedule.db")
		self.cursor = self.conn.cursor()
		self.cursor.execute("SELECT * FROM cities")
		rows = self.cursor.fetchall()
		for row in rows:
			self.city_store.append([row[1]])







if __name__ == '__main__':

	initializer = Initializer()
	Graph = initializer.G
	tracerouter = Tracerouter(Graph)
	tracerouter.route('Torzhok', 'Kalyazin')


	
	win = MyWindow()
	win.connect("destroy", Gtk.main_quit)
	win.show_all()
	Gtk.main()
