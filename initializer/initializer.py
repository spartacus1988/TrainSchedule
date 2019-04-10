import logging
import sqlite3

class Initializer:

    def __init__(self):
        logging.basicConfig(filename="TrainSchedule.log",
                            format='%(asctime)s   %(name)s  %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            filemode='w',
                            level=logging.INFO)
        self.logger = logging.getLogger("Initializer")
        self.logger.info("Initializing Initializer...")

      


        self.logger.info("Initializer is initialized")

