from initializer.initializer import Initializer
from tracerouter.tracerouter import Tracerouter
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gtk, GLib


def button_clicked(button):
	print( 'Hello World!' )


class MainWindow:
	def __init__(self):
		self.window = Gtk.Window()
		self.window.set_default_size(640, 480)
		self.window.set_title('Hello World!')
		self.window.connect('destroy', lambda w: Gtk.main_quit())
		self.window.show()

		self.button = Gtk.Button("Привет, Мир!")
		self.button.props.halign = Gtk.Align.CENTER
		self.button.props.valign = Gtk.Align.CENTER
		self.window.add(self.button)
		self.button.show()
 
	def main(self):
		Gtk.main()


if __name__ == '__main__':

	initializer = Initializer()
	Graph = initializer.G
	tracerouter = Tracerouter(Graph)
	tracerouter.route('Torzhok', 'Kalyazin')



	'''window = Gtk.Window()
	window.set_default_size(640, 480)
	window.set_title('Hello World!')
	window.connect('destroy', lambda w: Gtk.main_quit())
 
	button = Gtk.Button('Press Me')
	button.connect('clicked', button_clicked)
	button.show()
 
	window.add(button)
	window.present()
 
	Gtk.main()'''

	MainWindow = MainWindow()
	MainWindow.main()
