import threading
import time

from Underhood.toggle import*

class ZoneManager:
    def __init__(self, lightWriter = None, sensorReader = None):
        self.lightWriter = lightWriter
        self.sensorReader = sensorReader
        self.isRunning = False

    def loop(self):
        while self.isRunning:
            if(self.sensorReader.isOccupied()):
                self.lightWriter.setLight(Toggle.ON)
            else:
                self.lightWriter.setLight(Toggle.OFF)
            time.sleep(0.1)

    def start(self):
        self.isRunning = True
        thread = threading.Thread(
            target=self.loop,
            daemon=True
        )
        thread.start()
    
    def stop(self):
        self.isRunning = False
