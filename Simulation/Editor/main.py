from walls import*
from sensors import*
from lightstrips import*
from zones import*
from exporter import*

W,H = 800,600

# Initializing pygame
pygame.init()

# Initializing clock
clock = pygame.time.Clock()

# Creating a window
screen = pygame.display.set_mode((W, H))

# Creating layers
layer1 = pygame.Surface((W,H), pygame.SRCALPHA)
layer2 = pygame.Surface((W,H), pygame.SRCALPHA)

# Creating editors for the objects
walls = Walls()
sensors = Sensors()
lights = Lightstrips()
zones = Zones(sensors, lights)

# Creating the exporter
exporter = Exporter(zones, walls)

# Setting the initial editor to the walls
curObject = walls

# Game loop
run = True

while run:
    # Filling in background
    screen.fill((196, 162, 135))
    layer1.fill((0,0,0,0))
    layer2.fill((0,0,0,0))

    # Getting events from the user
    for e in pygame.event.get():
        # Stopping the game
        if e.type == pygame.QUIT:
            run = False
        
        # Mouse clicks
        if e.type == pygame.MOUSEBUTTONDOWN:
            curObject.handleClick(pygame.mouse.get_pos(), e.type)

        if e.type == pygame.MOUSEBUTTONUP:
            curObject.handleClick(pygame.mouse.get_pos(), e.type)
    
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_BACKSPACE:
                curObject.activateDeletion()
            
            # Switching between different objects
            if e.key == pygame.K_w:
                curObject.handOverControl()
                curObject = walls
            
            if e.key == pygame.K_s and (e.mod & pygame.KMOD_CTRL):
                # for zone in zones.zones:
                #     print(zone.lights)
                exporter.export("game_map.json")

            elif e.key == pygame.K_s:
                curObject.handOverControl()
                curObject = sensors
            
            
            if e.key == pygame.K_l:
                curObject.handOverControl()
                curObject = lights
            
            if e.key == pygame.K_z:
                curObject.handOverControl()
                curObject = zones

    sensors.drawObjects(layer1)
    walls.drawObjects(screen)
    lights.drawObjects(screen)
    zones.drawObjects(layer2)
    
    # Checking for pressed keys
    keys = pygame.key.get_pressed()
    
    # Flattening layers
    layer1.blit(layer2, (0,0))
    screen.blit(layer1, (0, 0))

    pygame.display.flip()
    clock.tick(60)