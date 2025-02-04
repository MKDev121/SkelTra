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
        self.bones=[]

    def add_bone(self,position,size):
        self.bones.append(impObj.bone(position,size))

    def display_bones(self,screen):
        for bone in self.bones:
            pg.draw.rect(screen,'green',(bone.position,bone.size),border_radius=5)


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
    
    def add_frame_part(self,screen,rig):
        
        for holder in self.holders.values():
            if(holder.rect.collidepoint(shared.mouse_pos) and shared.mouse_down):
                shared.current_holder_state =shared.holder_states[2]
                holder.selected=True
                shared.mouse_down=False

            if(shared.current_holder_state==shared.holder_states[2] and holder.selected):
                holder.display_holder_buttons(screen)
                if(shared.current_selected_options==shared.holder_selected_options[1] ):
                    location=impObj.open_file_explorer()
                    self.sprite.selected_frame.add_parts(holder,location)
                    shared.current_holder_state=shared.holder_states[1]
                    shared.current_selected_options=shared.holder_selected_options[0]
                    holder.selected=False
                #print("selected")
                #location=impObj.open_file_explorer()
                #
                #shared.current_holder_state=shared.holder_states[1]
    def load_frame(self,screen):
        for holder,part in self.sprite.selected_frame.parts.items():
            screen.blit(part,holder.position)


    

        
        
