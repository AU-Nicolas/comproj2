from objects import*

class Walls(Objects):
    def __init__(self, wall_size = 10, color = (83, 55, 69)):
        super().__init__() 
        # Color of the wall
        self.color = color
        self.wall_size = wall_size

    def quantizePoint(self, p):
        x = (p[0] // self.wall_size) * self.wall_size
        y = (p[1] // self.wall_size) * self.wall_size
        return (x,y)

    def makeWallSpecs(self, _p0, _p1):
        p0 = self.quantizePoint(_p0)
        p1 = self.quantizePoint(_p1)
        dx = abs(p1[0] - p0[0])
        dy = abs(p1[1] - p0[1])
        x1 = p1[0]
        y1 = p1[1]
        if(dx > dy):
            y1 = p0[1]
        else:
            x1 = p0[0]
        return self.standardizePoints(p0,(x1,y1))

    def addObject(self, p0, p1):
        p0, p1 = self.makeWallSpecs(p0,p1)
        self.objects.append((p0,p1))

    def makeRect(self, p0, p1):
        width = p1[0] - p0[0]
        height = p1[1] - p0[1]
        if(width > height):
            height = self.wall_size
        else:
            width = self.wall_size
        return pygame.Rect(p0[0], p0[1], width, height)

    # Drawing all the walls
    def drawObjects(self, surface):
        if(self.creatingObject):
            p0,p1 = self.makeWallSpecs(self.pos, pygame.mouse.get_pos())
            body = self.makeRect(p0,p1)
            pygame.draw.rect(surface, self.color, body)

        for wall in self.objects:
            body = self.makeRect(wall[0],wall[1])
            pygame.draw.rect(surface, self.color, body)