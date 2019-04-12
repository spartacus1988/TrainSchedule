from initializer.initializer import Initializer
from tracerouter.tracerouter import Tracerouter
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, GLib


class MyWindow(Gtk.Window):

	def __init__(self):
		Gtk.Window.__init__(self, title="TrainSchedule")
		self.set_default_size(640, 480)

		self.name_store = Gtk.ListStore(int, str)
		self.name_store.append([1, "Billy Bob"])
		self.name_store.append([11, "Billy Bob Junior"])
		self.name_store.append([12, "Sue Bob"])
		self.name_store.append([2, "Joey Jojo"])
		self.name_store.append([3, "Rob McRoberts"])
		self.name_store.append([31, "Xavier McRoberts"])

		self.vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
		self.add(self.vbox)

		self.hbox = Gtk.Box()
		#self.add(self.hbox)
		self.vbox.pack_start(self.hbox, False, False , 0)

		self.entry = Gtk.Entry()
		self.entry.set_editable(False)
		self.entry.set_text("TrainSchedule")
		self.vbox.pack_start(self.entry, True, True, 0)

		self.name_combo_left = Gtk.ComboBox.new_with_model_and_entry(self.name_store)
		self.name_combo_left.connect("changed", self.on_name_combo_changed)
		self.name_combo_left.set_entry_text_column(1)
		self.hbox.pack_start(self.name_combo_left, False, False, 0)

		self.name_combo_right = Gtk.ComboBox.new_with_model_and_entry(self.name_store)
		self.name_combo_right.connect("changed", self.on_name_combo_changed)
		self.name_combo_right.set_entry_text_column(1)
		self.hbox.pack_start(self.name_combo_right, False, False, 0)

		

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

	def on_name_combo_changed(self, combo):
		tree_iter = combo.get_active_iter()
		if tree_iter is not None:
			model = combo.get_model()
			row_id, name = model[tree_iter][:2]
			print("Selected: ID=%d, name=%s" % (row_id, name))
		else:
			entry = combo.get_child()
			print("Entered: %s" % entry.get_text())







if __name__ == '__main__':

	initializer = Initializer()
	Graph = initializer.G
	tracerouter = Tracerouter(Graph)
	tracerouter.route('Torzhok', 'Kalyazin')


	
	win = MyWindow()
	win.connect("destroy", Gtk.main_quit)
	win.show_all()
	Gtk.main()
