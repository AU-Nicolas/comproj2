from Objects.wall import*
from Underhood.toggle import*

class Light(Wall):
    def __init__(self, 
                 p0,
                 p1,
                 light_width = 5,  
                 off_color = (70,70,70), 
                 on_color = (36, 123, 160)):
        
        super().__init__(p0, p1, light_width, off_color)
        self.off_color = off_color
        self.on_color = on_color
                   
    
    def toggle(self, value):
        if value == Toggle.ON:
            self.color = self.on_color
        elif value == Toggle.OFF:
            self.color = self.off_color

        
