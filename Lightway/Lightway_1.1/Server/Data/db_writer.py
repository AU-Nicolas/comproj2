import mysql.connector
from datetime import datetime

class DBWriter:
    def __init__(self, host="localhost",
                  user="lightway",
                  password="bean",
                  database="lightway",
                  table="toilet_visits"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.table = table
        self.db = None
        self.Connect()
    
    def Connect(self):
        # If already connected, nothing happens
        if self.db:
            return
        try:
            # Connecting as the user
            self.db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            # Setting the cursor
            self.db.cursor().execute(f"USE {self.database}")
            # Creating the table
            self.CreateTable()


        # If something went wrong when logging into the database
        except mysql.connector.Error as err:

            # If the database didn't already exist
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                self.CreateDatabase()

            # If something else was the issue
            else:
                print(f"Database error: {err}")
        

    
    def CreateDatabase(self):
        # Creating the database
        cursor = self.db.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")

        # Setting the database as the active database
        cursor.execute(f"USE {self.database}")

        # Creating the table
        self.CreateTable()

    # Can only be called when the database exists
    def CreateTable(self):
        # Creating the table - time is stored in whole seconds
        cursor = self.db.cursor()
        cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.table} (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       start DATETIME,
                       total_time INT,
                       completed BOOLEAN,
                       to_toilet INT,
                       on_toilet INT,
                       to_bed INT
                       )""")
    
    def WriteToDB(self, start, total_time, completed=False, to_toilet=0, on_toilet=0, to_bed=0):
        print("I Write into the database")
        sql = f"INSERT INTO {self.table} (start, total_time, completed, to_toilet, on_toilet, to_bed)\
              VALUES (%s, %s, %s, %s, %s, %s)"
        self.db.cursor().execute(sql, (start, total_time, completed, to_toilet, on_toilet, to_bed))
        self.db.commit()
