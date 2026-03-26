from walls import*

class Lightstrips(Walls):
    def __init__(self, strip_size = 5, color = (70,70,70)):
        super().__init__(strip_size, color)