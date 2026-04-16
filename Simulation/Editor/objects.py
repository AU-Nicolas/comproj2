from abc import ABC, abstractmethod
import pygame

class Objects(ABC):
    def __init__(self, smallest = 20):
        self.deleting = False
        self.objects = []
        self.creatingObject = False
        self.smallest = smallest
        # The current starting position of the square to be created
        self.pos = (0,0)

    def handleClick(self, pos, event):
        # If walls currently are being deleted
        if(self.deleting):
            if(event == pygame.MOUSEBUTTONUP):
                for object in self.objects:
                    body = self.makeRect(object[0], object[1])
                    if(body.collidepoint(pos)):
                        self.deleteObject(object)
                self.deleting = False

        if(event == pygame.MOUSEBUTTONDOWN):
            self.pos = pos
            self.creatingObject = True
        
        if(event == pygame.MOUSEBUTTONUP and self.creatingObject):
            if(self.bigEnough(self.pos, pos)):
                self.addObject(self.pos, pos)
            self.creatingObject = False
    
    def bigEnough(self, p0, p1):
        dx = abs(p0[0] - p1[0])
        dy = abs(p0[1] - p1[1])
        if(dy > self.smallest or dx > self.smallest):
            return True
        else:
            return False
    

    def standardizePoints(self, p0, p1):
        x0 = p0[0]
        x1 = p1[0]
        y0 = p0[1]
        y1 = p1[1]
        if(p0[0] > p1[0]):
            x0 = p1[0]
            x1 = p0[0]
        if(p0[1] > p1[1]):
            y0 = p1[1]
            y1 = p0[1]
        return (x0,y0), (x1,y1)

    def getRectSpecs(self, p0, p1):
        p0,p1 = self.standardizePoints(p0,p1)
        width = p1[0] - p0[0]
        height = p1[1] - p0[1] 
        return p0[0],p0[1],width,height

    def deleteObject(self, object):
        self.objects.remove(object)
    
    def handOverControl(self):
        self.creatingObject = False
        self.deleting = False

    def activateDeletion(self):
        self.deleting = True
        self.creatingObject = False   
    
    @abstractmethod
    def makeRect(self, p0, p1):
        pass
    
    @abstractmethod
    def addObject(self, p0, p1):
        pass

    @abstractmethod
    def drawObjects(self, surface):
        pass

         
