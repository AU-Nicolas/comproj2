import pygame
from Underhood.collision import*
import math
class Sensor:
    def __init__(self, p0, p1, 
                 box_size = 10, 
                 light_color = (214, 209, 205, 128),
                 box_color = (171, 78, 104)):
        
        # Creating the sensor field
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
    
        self.body = (p0, p2, p3)
        self.light_color = light_color

        # Creating the sensor box
        self.box = pygame.Rect(p0[0]-box_size//2,p0[1]-box_size//2, box_size, box_size)
        self.box_color = box_color

        # Variable reflecting occupancy
        self.isOccupied = False
    

    def draw(self, surface):
        pygame.draw.rect(surface, self.box_color, self.box)
        pygame.draw.polygon(surface, self.light_color, self.body)
    
    def setOccupancy(self, object):
        self.isOccupied = collideRectPolygon(object, self.body)






        



        