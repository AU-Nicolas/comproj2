from database_manager import DatabaseManager
from listener import Listener

dbManager = DatabaseManager()
listener = Listener(dbManager)
listener.loop()