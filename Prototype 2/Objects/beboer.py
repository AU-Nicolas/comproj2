import pygame

class Beboer:
    def __init__(self, x, y, speed, 
                 color = (36, 123, 160), 
                 width = 10, 
                 height = 10):
        self.prev_x = x
        self.prev_y = y
        self.speed = speed
        self.width = width
        self.height = height
        self.color = color
        self.body = pygame.Rect(x,y,width, height)
    
    def move(self, x, y):
        self.prev_x = self.body.x
        self.prev_y = self.body.y
        self.body.x += x*self.speed
        self.body.y += y*self.speed
    
    def checkCollision(self, object):
        if(self.body.colliderect(object)):
            self.body.x = self.prev_x
            self.body.y = self.prev_y
    
    def draw(self,surface):
        pygame.draw.rect(surface, self.color, self.body)

