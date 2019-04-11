from initializer.initializer import Initializer
from tracerouter.tracerouter import Tracerouter



if __name__ == '__main__':

	initializer = Initializer()
	Graph = initializer.G
	tracerouter = Tracerouter(Graph)
