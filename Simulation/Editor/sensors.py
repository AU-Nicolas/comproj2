import math
from objects import*

class Sensors(Objects):
    def __init__(self, box_size = 10,
                 light_color = (214, 209, 205, 128),
                 box_color = (171, 78, 104)):
        super().__init__()
        self.box_color = box_color
        self.box_size = box_size
        self.light_color = light_color
    


    def addObject(self, p0, p1):
        self.objects.append((p0,p1))

    def makePolygon(self, p0, p1):
        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]
        angle = math.atan2(dy, dx)
        length = math.sqrt(dx**2 + dy**2) * math.sqrt(2)
        x1 = math.cos(angle  + math.pi/4)*length
        y1 = math.sin(angle  + math.pi/4)*length
        x2 = math.cos(angle  - math.pi/4)*length
        y2 = math.sin(angle  - math.pi/4)*length
        p2 = (x1+p0[0], y1+p0[1])
        p3 = (x2+p0[0], y2+p0[1])
        return (p0, p2, p3)
    
    def makeBox(self, p):
        x = p[0]
        y = p[1]
        return pygame.Rect(x-self.box_size//2,y-self.box_size//2, self.box_size, self.box_size)


    def makeRect(self, p0, p1):
        x,y,dx,dy = self.getRectSpecs(p0,p1)
        length = math.sqrt(dx**2 + dy**2)
        x += dx/2 - length/2
        y += dy/2 - length/2
        return pygame.Rect(x,y,length,length)
        

    def drawObjects(self, surface):
        if(self.creatingObject):
            box = self.makeBox(self.pos)
            polygon = self.makePolygon(self.pos, pygame.mouse.get_pos())
            pygame.draw.rect(surface, self.box_color, box)
            pygame.draw.polygon(surface, self.light_color, polygon)

        for sensor in self.objects:
            p0 = sensor[0]
            p1 = sensor[1]
            pygame.draw.rect(surface, self.box_color, self.makeBox(p0))
            pygame.draw.polygon(surface, self.light_color, self.makePolygon(p0, p1))
            


