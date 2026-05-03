import pygame

# Creating square on screen
class Wall:
    def __init__(self, p0, p1, wall_width = 10, color = (83, 55, 69)):
        
        self.color = color
        
        # Creating the body of the wall
        x = p0[0]
        y = p0[1]
        width = p1[0] - x
        height = p1[1] - y
        # The dimension with no length becomes wall_width
        if(width == 0):
            width = wall_width
        else:
            height = wall_width
        
        self.body = pygame.Rect(x,y,width,height)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.body)


    

