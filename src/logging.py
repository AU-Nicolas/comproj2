# I dette dokument logger vi
from datetime import datetime



class logging():

    def __init__(self, StartBedTime = None,
                 EndBedTime = None,
                 StartToiletTime = None,
                 EndToiletTime = None):
        self.StartBedTime = StartBedTime
        self.EndBedTime = EndBedTime
        self.StartToiletTime = StartToiletTime
        self.EndToiletTime = EndToiletTime
        pass

    def LogStartTimeBed(self, Start):
        return StartTimeBed = datetime.now()
        pass

    def LogEndTimeBed(self,):
        EndTime = datetime.now()
        pass

    def LogStartTimeToilet(self,):
        StartToiletTime = datetime.now()
        pass

    def LogEndTimeT(self):
        EndToiletTime = datetime.now()
        pass
    
    def __str__(self):
        pass
        return ( f"StartBedTime: {self.StartBedTime}, 
        EndBedTime: {self.EndBedTime}, 
        "StartToiletTime: {self.StartToiletTime}, 
        EndToiletTime: {self.EndToiletTime}"
        )
