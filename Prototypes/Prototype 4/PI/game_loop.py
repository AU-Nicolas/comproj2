import pygame
from Objects.beboer import*

class GameLoop:
    def __init__(self):
        self.W = 800
        self.H = 600
        self.walls = []
        self.sensors = []
        self.lights = []


    def run(self):
        # Initializing pygame
        pygame.init()

        # Initializing clock
        clock = pygame.time.Clock()

        screen = pygame.display.set_mode((self.W, self.H))

        # Creating screen which everything will be displayed on
        layer1 = pygame.Surface((self.W,self.H), pygame.SRCALPHA)

        # Creating the beboer
        beboer = Beboer(50,50,5)

        # Game loop
        run = True

        while run:
            # Filling in background
            screen.fill((196, 162, 135))
            layer1.fill((0,0,0,0))

            # Checking if the user wants to quit
            for e in pygame.event.get():
                # Stopping the game
                if e.type == pygame.QUIT:
                    run = False
            
            # Checking for pressed keys
            keys = pygame.key.get_pressed()
            # Movement of beboer
            new_x = 0
            new_y = 0
            if keys[pygame.K_LEFT]:
                new_x -= 1
            if keys[pygame.K_RIGHT]:
                new_x += 1
            if keys[pygame.K_UP]:
                new_y -= 1
            if keys[pygame.K_DOWN]:
                new_y += 1
            
            beboer.move(new_x, new_y)
            
            # Checking for collisions
            for wall in self.walls:
                # Checking if the beboer is colliding with a wall
                beboer.checkCollision(wall.body)
            
            # Checking for sensor occupancy
            for sensor in self.sensors:
                sensor.setOccupancy(beboer.body)

            # Drawing LED's
            for light in self.lights:
                light.draw(screen)

            # Drawing the beboer
            beboer.draw(screen)

            # Drawing the sensors
            for sensor in self.sensors:
                sensor.draw(layer1)

            # Drawing walls
            for wall in self.walls:
                wall.draw(layer1)

            screen.blit(layer1, (0, 0))

            pygame.display.flip()
            clock.tick(60)