import pygame as pg
import impObj
import shared
class Character:
    def __init__(self):
        self.Rig=Rig()
        self.Sprite=Sprite()
        self.Body=Body()
    def load(self,screen):
        for item in self.Body.holders.values():
            item.load(screen)
        

class Rig:

    def __init__(self):
        self.bones={}

    def add_bone(self,name):
        self.bones[name]=impObj.bone()

class Sprite:

    def __init__(self):
        self.frames=[impObj.frame()]
        self.selected_frame=self.frames[0]

class Body:

    def __init__(self):
        self.holders={}
        self.intial_pos=pg.Vector2(0,0)
        self.sprite=Sprite()

    def add_holder(self,name="",pos=pg.Vector2(0,0),scale=[100,100]):
        self.holders[name]=impObj.holder(position=pos,scale=scale)
    
    def add_frame_part(self):
        for holder in self.holders.values():
            if(holder.rect.collidepoint(shared.mouse_pos) and shared.mouse_down):
                shared.current_holder_state=shared.holder_states[2]
                shared.mouse_state="buffer"

            if(shared.current_holder_state==shared.holder_states[2]):
                location=r"test\1_ORK_"+input("Enter name: ")+".png"
                self.sprite.selected_frame.add_parts(holder,location)
                shared.current_holder_state=shared.holder_states[1]
    def load_frame(self,screen):
        for holder,part in self.sprite.selected_frame.parts.items():
            screen.blit(part,holder.position)

        
        
        
