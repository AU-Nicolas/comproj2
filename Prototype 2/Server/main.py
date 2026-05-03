from Business.db_updater import*
from Data.data_retriever import*
from Data.db_writer import*


dbWriter = DBWriter()
dbUpdater = DBUpdater(dbWriter)
dataRetriever = DataRetriever(dbUpdater.InsertIntoDB)
dataRetriever.Loop()