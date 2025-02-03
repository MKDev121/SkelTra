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
        self.bones[name]=impObj.bone(0)

class Sprite:

    def __init__(self):
        pass
class Body:

    def __init__(self):
        self.holders={}
        self.intial_pos=pg.Vector2(0,0)

    def add_holder(self,name="",pos=pg.Vector2(0,0),scale=[100,100]):
        self.holders[name]=impObj.holder(position=pos,scale=scale)

        
        
        
