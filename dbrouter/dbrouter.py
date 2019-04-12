import logging
import sqlite3


class DBrouter:

    def __init__(self):
        logging.basicConfig(filename="TrainSchedule.log",
                            format='%(asctime)s   %(name)s  %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p',
                            filemode='w',
                            level=logging.INFO)
        self.logger = logging.getLogger("DBrouter")
        self.logger.info("DBrouter init start...")

        self.conn = sqlite3.connect("TrainSchedule.db")
        self.cursor = self.conn.cursor()

        self.read()

        self.logger.info("DBrouter init finished")

    def read(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS 
                            routes (route_id INTEGER PRIMARY KEY UNIQUE ON CONFLICT REPLACE, 
                                    left_city TEXT NOT NULL,
                                    right_city TEXT NOT NULL, 
                                    start_time TEXT NOT NULL,
                                    end_time TEXT NOT NULL);""")
        self.cursor.execute("SELECT * FROM routes")
        rows = self.cursor.fetchall()
        self.route_store = []
        for row in rows:
            self.route_store.append([row])
            print(row)
        return self.route_store



    def save(self, routeNumber, startPoint, endPoint, startTime, endTime):
        self.cursor.execute("INSERT INTO routes VALUES(?, ?, ?, ?, ?)", (routeNumber, startPoint, endPoint, startTime, endTime))
        self.conn.commit()


