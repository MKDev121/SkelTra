import pygame as pg
import shared 

class bone:

    def __init__(self,color):
        self.position=pg.Vector2(0,0)
        self.rotation=[0,0]
        self.size=pg.Vector2(0,0)
        self.color=color

    

class holder:

    def __init__(self,position=pg.Vector2(0,0),rotation=[0,0],scale=[50,50]):
        self.position=position
        self.rotation=rotation
        self.scale=scale

    def load(self,screen):
        
        if(shared.current_holder_state==shared.holder_states[2]):


            pg.draw.rect(screen,'black',(self.position,self.scale))
            pg.draw.rect(screen,'grey',(self.position+pg.Vector2(10,10),self.scale-pg.Vector2(20,20)))
        
class frame:
    def __init__(self):
        self.parts=[]
    def add_parts(self,location):
        self.parts.append(pg.image.load(location))
    # def load_frame(self,pos,screen=pg.display.set_mode(0,0)):
    #     for part in self.parts:
    #         screen.blit(part,pos)


# class Button: #class
#     def __init__(icon,colour,cuisine_type): #method
#         self.restaurant_name = restaurant_name
#         self.cuisine_type = cuisine_type
    
#     def describe_restaurant(self): #method
#         print(f"the name of the restaurant is {self.restaurant_name}")
#         print(f"cuisine type : {self.cuisine_type}")

#     def open_restaurant(self): #method
#         print("OPEN")