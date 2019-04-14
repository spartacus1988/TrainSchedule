from initializer.initializer import Initializer
from tracerouter.tracerouter import Tracerouter
from dbrouter.dbrouter import DBrouter
from calculator.calculator import Calc
from gui.gui import MyWindow


if __name__ == '__main__':

	initializer = Initializer()
	Graph = initializer.G
	tracerouter = Tracerouter(Graph)
	dbrouter = DBrouter()
	calculator = Calc(tracerouter)
	
	win = MyWindow(tracerouter, dbrouter, calculator)
	
