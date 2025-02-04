import pygame as pg
import shared 
import tkinter as tk
from tkinter import filedialog
import os
class bone:

    def __init__(self,position,size):
        self.position=position
        self.rotation=0
        self.size=size
        self.color='green'
        self.rect=pg.Rect(position.x,position.y,size[0],size[1])


class HolderButton:
    def __init__(self,position=pg.Vector2(0,0),scale=(0,0),color=(0,0,0),name="image",name1="image"):
        self.position=position
        self.scale=scale
        self.color=color
        self.name=name
        self.name1=name1
        self.rect=pg.Rect(position[0],position[1],scale[0],scale[1])   

class holder:

    def __init__(self,position=pg.Vector2(0,0),rotation=[0,0],scale=[50,50]):
        self.position=position
        self.rotation=rotation
        self.scale=scale
        self.rect=pg.rect.Rect(position,scale)
        self.selected=False
        self.holder_buttons=[HolderButton(self.position+pg.Vector2(0,-20),(16,16),(0,0,255)),HolderButton(self.position+pg.Vector2(10,-20),(16,16),(0,255,0))]

    def load(self, screen):
    # Draw the rectangle
        pg.draw.rect(screen, 'black', (self.position, self.scale), 3)

    # Create a rectangle object to get the correct corners
        rect = pg.Rect(self.position, self.scale)  
        corners = [rect.topleft, rect.topright, rect.bottomleft, rect.bottomright]

    # Draw circles at the corners
        for corner in corners:
            pg.draw.circle(screen, (0, 0, 0), corner, 5)  # Increased radius for visibility


        #pg.draw.rect(screen,'grey',(self.position+pg.Vector2(4,4),self.scale-pg.Vector2(8,8)))
    def display_holder_buttons(self,screen):
        count=0
        for holder_button in self.holder_buttons:
            pos=pg.Vector2(holder_button.position[0]+count*20,holder_button.position[1])
            pg.draw.rect(screen,holder_button.color,(pos,holder_button.scale))
            holder_button.rect.topleft=(pos.x,pos.y)
            if (self.holder_buttons[0]== holder_button):
                if(holder_button.rect.collidepoint(shared.mouse_pos) and shared.mouse_down):
                    shared.current_selected_options=shared.holder_selected_options[count+1]
                
                    shared.mouse_down=False
                    print("Selected")
                count+=1
                image_box = pg.transform.smoothscale(pg.image.load('UI_Pics/image.jpg'),(20,20))
                img = image_box.get_rect(center = (pos[0]+10,pos[1]+6))
                screen.blit(image_box, img)
            else:
                if(holder_button.rect.collidepoint(shared.mouse_pos) and shared.mouse_down):
                    shared.current_selected_options=shared.holder_selected_options[count+1]
                
                    shared.mouse_down=False
                    print("Selected")
                count+=1
                image_box = pg.transform.smoothscale(pg.image.load('UI_Pics/Bone.jpg'),(20,20))
                img = image_box.get_rect(center = (pos[0]+10,pos[1]+6))
                screen.blit(image_box, img)






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
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
class RenamableText:
    def __init__(self, text, font, color, x, y, editable=False):
        self.text = text
        self.font = font
        self.color = color
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(topleft=(x, y))
        self.editing = False
        self.cursor_visible = True
        self.cursor_timer = pg.time.get_ticks()
        self.cursor_pos = len(self.text)
        self.selection_start = 0
        self.selection_end = len(self.text)
        self.highlighted = False
        self.editable = editable  # New flag to indicate if the text is editable

    def draw(self, screen, position):
        current_time = pg.time.get_ticks()

        if self.editing:
            # Draw input box background
            pg.draw.rect(screen, LIGHT_GRAY, self.rect.inflate(10, 10))  

            # Check cursor blink
            if current_time - self.cursor_timer > 500:  # Cursor blink speed in milliseconds
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = current_time

            # Handle text rendering with highlighting
            if self.highlighted:
                pg.draw.rect(screen, BLUE, self.rect)  # Highlight full text
                self.surface = self.font.render(self.text, True, BLACK)
            else:
                self.surface = self.font.render(self.text, True, BLACK)

            # Draw text
            screen.blit(self.surface, position)

            # Draw cursor if visible
            if self.cursor_visible and not self.highlighted:
                cursor_x = position[0] + self.font.size(self.text[:self.cursor_pos])[0] + 2
                # Calculate cursor height based on font metrics
                cursor_height = self.font.get_height()  # Get the height of the font
                pg.draw.line(screen, BLACK, (cursor_x, position[1]), (cursor_x, position[1] + cursor_height), 2)

        else:
            # Draw static text
            self.surface = self.font.render(self.text, True, WHITE)  # Change text color to white when not editing
            screen.blit(self.surface, position)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and self.editable:  # Only allow editing if editable is True
                self.editing = True
                self.cursor_pos = len(self.text)  # Place cursor at end
                self.selection_start, self.selection_end = 0, len(self.text)  # Select all text
                self.highlighted = True  # Enable highlighting
                return self  # Return self to indicate this is the active object
            else:
                self.editing = False  # Disable editing if another object is clicked
                self.highlighted = False
        
        elif event.type == pg.KEYDOWN and self.editing:
            if event.key == pg.K_RETURN:  # Press Enter to save
                self.editing = False
                self.highlighted = False
            
            elif event.key == pg.K_BACKSPACE:  # Handle backspace
                if self.highlighted:  # If all text is selected, remove everything
                    self.text = ""
                    self.cursor_pos = 0
                    self.highlighted = False
                elif self.cursor_pos > 0:
                    self.text = self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:]
                    self.cursor_pos -= 1
            
            elif event.key == pg.K_LEFT:  # Move cursor left
                if self.cursor_pos > 0:
                    self.cursor_pos -= 1
                self.highlighted = False
            
            elif event.key == pg.K_RIGHT:  # Move cursor right
                if self.cursor_pos < len(self.text):
                    self.cursor_pos += 1
                self.highlighted = False
            
            elif event.key == pg.K_a and pg.key.get_mods() & pg.KMOD_CTRL:  # Ctrl + A for select all
                self.selection_start, self.selection_end = 0, len(self.text)
                self.highlighted = True

            else:
                # Ensure character limit is not exceeded
                if len(self.text) < 25:  # Character limit
                    if event.unicode.isprintable():  # Only register printable characters
                        if self.highlighted:  # If all text is selected, replace it
                            self.text = event.unicode
                            self.cursor_pos = len(self.text)
                            self.highlighted = False
                        else:
                            self.text = self.text[:self.cursor_pos] + event.unicode + self.text[self.cursor_pos:]
                            self.cursor_pos += 1

        return None  # Return None if no object is active

