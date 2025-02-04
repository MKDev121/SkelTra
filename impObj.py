import pygame as pg
import shared 
import tkinter as tk
from tkinter import filedialog
import os
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
        self.rect=pg.rect.Rect(position,scale)

    def load(self,screen):
        pg.draw.rect(screen,'black',(self.position,self.scale))
        pg.draw.rect(screen,'grey',(self.position+pg.Vector2(4,4),self.scale-pg.Vector2(8,8)))
  
class frame:
    def __init__(self):
        self.parts={}
    def add_parts(self,holder,location):
        self.parts[holder]=pg.transform.smoothscale(pg.image.load(location),holder.scale)
    # def load_frame(self,pos,screen=pg.display.set_mode(0,0)):
    #     for part in self.parts:
    #         screen.blit(part,pos)
def open_file_explorer():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title = "Select a File", 
                                           filetypes = [("Portable Network Graphics", ".png"),
                                                        ("Joint Photographic Experts Group", ".jpg"),
                                                        ("Joint Photographic Experts Group", ".jpeg")])
    
    if file_path:   
        return file_path
        #paths.append(file_path)

