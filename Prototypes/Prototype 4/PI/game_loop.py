import pygame
from Objects.beboer import *

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
        layer1 = pygame.Surface((self.W, self.H), pygame.SRCALPHA)

        # Creating two beboere
        beboer1 = Beboer(100, 100, 5)   # Arrow keys
        beboer2 = Beboer(300, 100, 5, color=(171, 78, 104))   # WASD

        # Game loop
        run = True

        while run:
            # Filling in background
            screen.fill((196, 162, 135))
            layer1.fill((0, 0, 0, 0))

            # Checking if the user wants to quit
            for e in pygame.event.get():
                # Stopping the game
                if e.type == pygame.QUIT:
                    run = False

            # Checking for pressed keys
            keys = pygame.key.get_pressed()

            # -----------------------------
            # Movement for beboer1 (Arrow keys)
            # -----------------------------
            new_x1 = 0
            new_y1 = 0

            if keys[pygame.K_LEFT]:
                new_x1 -= 1
            if keys[pygame.K_RIGHT]:
                new_x1 += 1
            if keys[pygame.K_UP]:
                new_y1 -= 1
            if keys[pygame.K_DOWN]:
                new_y1 += 1

            beboer1.move(new_x1, new_y1)

            # -----------------------------
            # Movement for beboer2 (WASD)
            # -----------------------------
            new_x2 = 0
            new_y2 = 0

            if keys[pygame.K_a]:
                new_x2 -= 1
            if keys[pygame.K_d]:
                new_x2 += 1
            if keys[pygame.K_w]:
                new_y2 -= 1
            if keys[pygame.K_s]:
                new_y2 += 1

            beboer2.move(new_x2, new_y2)

            # Checking for collisions
            for wall in self.walls:
                # Checking collisions for both beboere
                beboer1.checkCollision(wall.body)
                beboer2.checkCollision(wall.body)

            # Checking for sensor occupancy
            for sensor in self.sensors:
                sensor.setOccupancy(beboer1.body, beboer2.body)

            # Drawing LED's
            for light in self.lights:
                light.draw(screen)

            # Drawing the beboere
            beboer1.draw(screen)
            beboer2.draw(screen)

            # Drawing the sensors
            for sensor in self.sensors:
                sensor.draw(layer1)

            # Drawing walls
            for wall in self.walls:
                wall.draw(layer1)

            screen.blit(layer1, (0, 0))

            pygame.display.flip()
            clock.tick(60)