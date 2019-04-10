import logging
from tracerouter.wave_algo import Router

class Tracerouter:

    def __init__(self):
        logging.basicConfig(filename="TrainSchedule.log",
                            format='%(asctime)s   %(name)s  %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            filemode='w',
                            level=logging.INFO)
        self.logger = logging.getLogger("Tracerouter")
        self.logger.info("Tracerouter start...")

        Router()


        self.logger.info("Tracerouter finished")
