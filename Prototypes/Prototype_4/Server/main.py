from Business.db_updater import*
from Data.data_receiver import*
from Data.db_writer import*


dbWriter = DBWriter()
dbUpdater = DBUpdater(dbWriter)
dataReceiever = DataReceiver(dbUpdater.InsertIntoDB, "localhost")
dataReceiever.Loop()