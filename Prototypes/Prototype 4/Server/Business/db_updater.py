from datetime import datetime

class DBUpdater:
    def __init__(self, db_writer):
        # Creating component that can write into databases
        self.db_writer = db_writer

    def InsertIntoDB(self, data):
        # Checking that the message has the correct properties
        # if not, we return and print an error statement
        if("start" not in data or
           "total_time" not in data or
           "completed" not in data or
           "to_toilet" not in data or
           "on_toilet" not in data or
           "to_bed" not in data):
            print("DBUpdater: ERROR: Wrong MQTT message format")
            return
        
        # Converting the start time back to a datetime object
        start_time = datetime.strptime(data["start"], "%Y-%m-%d %H:%M:%S")
        # Sending the message to the database
        self.db_writer.WriteToDB(start_time, 
                                 data["total_time"], 
                                 data["completed"], 
                                 data["to_toilet"], 
                                 data["on_toilet"],
                                 data["to_bed"])