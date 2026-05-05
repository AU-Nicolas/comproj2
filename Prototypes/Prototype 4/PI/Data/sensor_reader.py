class SensorReader:
    def __init__(self, sensor = None):
        self.sensor = sensor
    def isOccupied(self):
        return self.sensor.isOccupied
    def ShutDown(self):
        pass