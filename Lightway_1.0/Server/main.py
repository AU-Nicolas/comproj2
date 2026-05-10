from Business.db_updater import*
from Data.data_receiver import*
from Data.db_writer import*


dbWriter = DBWriter()
dbUpdater = DBUpdater(dbWriter)
dataReceiever = DataReceiver(dbUpdater.InsertIntoDB, "172.18.157.211")
dataReceiever.Loop()