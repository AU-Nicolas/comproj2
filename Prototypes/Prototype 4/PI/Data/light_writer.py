from Enums.toggle import*
import threading

class LightWriter:
    def __init__(self, lights = [], changeTime = 0.4):
        self.settingToValue = Toggle.OFF
        self.lights = lights
        self.timer = None
        self.changeTime = changeTime
        self.lock = threading.Lock()

    def SetLight(self, value):
        # Ensuring only one instance can run
        with self.lock:
            # If we already are setting to the current value, we abort
            if(value == self.settingToValue):
                return
            
            # Updating the value we are setting to
            self.settingToValue = value

            # If something is currently setting, we cancel that proces
            if self.timer:
                self.timer.cancel()
            
            # We will now change the light in self.changeTime time
            self.timer = threading.Timer(
                interval=self.changeTime,
                function=self.ChangeLight,
                args=(value,)
            )
            self.timer.start()

    def ChangeLight(self, value):
        with self.lock:
            # Returns if we somehow are setting to some value different than
            # the most recently desired one
            if value != self.settingToValue:
                return
            
            # The light is changed
            for light in self.lights:
                light.toggle(value)

    def ShutDown(self):
        pass