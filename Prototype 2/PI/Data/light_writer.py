from Enums.toggle import*


class LightWriter:
    def __init__(self, lights = []):
        self.lights = lights

    def setLight(self, value):
        for light in self.lights:
            light.toggle(value)