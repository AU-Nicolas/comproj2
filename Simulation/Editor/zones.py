from objects import*

class Zone:
    def __init__(self):
        self.sensor = None
        self.lights = []
        

class Zones(Objects):
    def __init__(self, sensors, lights, smallest = 50, color = (100,100,100,50)):
        super().__init__(smallest)
        self.color = color
        self.zones = []
        self.sensors = sensors
        self.lights = lights
        self.font = pygame.font.Font('freesansbold.ttf', 10)


    def makeRect(self, p0, p1):
        x,y,width,height = self.getRectSpecs(p0,p1)
        return pygame.Rect(x,y,width,height)
    
    def addObject(self, p0, p1):
        p0,p1 = self.standardizePoints(p0,p1)
        area = self.makeRect(p0,p1)
        zone = Zone()
        hasSensor = False
        for sensor in self.sensors.objects:
            duplicate = False
            for prev_zone in self.zones:
                if sensor == prev_zone.sensor:
                    duplicate = True
            if duplicate:
                continue
            if (area.collidepoint(sensor[0]) and hasSensor):
                print("Error: Too many sensors in area")
                return
            elif(area.collidepoint(sensor[0])):
                zone.sensor = sensor
                hasSensor = True
        if(not hasSensor):
            print("Error: Zone contains no sensor")
            return
        for light in self.lights.objects:
            rect = self.lights.makeRect(light[0], light[1])
            if area.colliderect(rect):
                zone.lights.append(light)
        self.zones.append(zone)
        self.objects.append((p0,p1))
        
                
    def deleteObject(self, object):
        self.objects.pop(-1)
        self.zones.pop(-1)
        
    def drawZone(self, zone, surface):
        rect = self.makeRect(zone[0], zone[1])
        pygame.draw.rect(surface, self.color, rect)

    def drawObjects(self, surface):
        if self.creatingObject:
            self.drawZone((self.pos, pygame.mouse.get_pos()), surface)

        index = 1
        for zone in self.objects:
            self.drawZone(zone, surface)
            text = self.font.render(f"{index}", True, (100,100,100))
            textRect = text.get_rect()
            x,y,width,height = self.getRectSpecs(zone[0], zone[1])
            textRect.center = (x + width//2, y+height//2)
            surface.blit(text, textRect)
            index += 1

