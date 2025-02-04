import pygame as pg
import character
import shared 
import math
import impObj
# pg setup
pg.init()
clock = pg.time.Clock()
running = True
pg.display.set_caption("SkelTra")
char = character.Character()
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Initialize screen
screen = pg.display.set_mode()
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

# Fonts
font_heading = pg.font.Font(None, 48)
font_button = pg.font.Font(None, 36)

# Load Icon Image
try:
    icon_image = pg.image.load("add-outline.png")
    icon_image = pg.transform.scale(icon_image, (30, 30))

except pg.error:
    print("Error: Image 'add-outline.png' not found.")
    icon_image = None

# Scrollable Panel Class
class ScrollablePanel:
    def __init__(self, x, y, width, height, color):
        self.rect = pg.Rect(x, y, width, height)
        self.color = color
        self.content_offset = 0
        self.elements = []
        self.max_scroll = 0  

    def add_element(self, element):
        self.elements.append(element)
        self.max_scroll = max(self.max_scroll, len(self.elements) * 60 - self.rect.height)

    def scroll(self, amount):
        self.content_offset += amount
        self.content_offset = max(min(self.content_offset, self.max_scroll), 0)

    def draw(self, screen):
        panel_surface = pg.Surface((self.rect.width, self.rect.height))
        panel_surface.fill(self.color)

        for element in self.elements:
            y_position = element.rect.y - self.content_offset
            if self.rect.top <= y_position <= self.rect.bottom:
                element.draw(panel_surface, (element.rect.x - self.rect.x, y_position - self.rect.y))

        screen.blit(panel_surface, self.rect.topleft)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.scroll(-30)
            elif event.button == 5:  # Scroll down
                self.scroll(30)

# Text Class
class Text:
    def __init__(self, text, font, color, x, y):
        self.text = text
        self.font = font
        self.color = color
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(topleft=(x, y))

    def draw(self, screen, position):
        screen.blit(self.surface, position)

# Button Class
class Button:
    def __init__(self, x, y, width, height, color, hover_color, text_obj=None, icon=None, callback=None):
        self.rect = pg.Rect(x, y, width, height)
        self.text_obj = text_obj
        self.color = color
        self.hover_color = hover_color
        self.hovered = False
        self.icon = icon
        self.callback = callback

    def draw(self, screen, position):
        pg.draw.rect(screen, self.hover_color if self.hovered else self.color, position + self.rect.size)
        if self.text_obj:
            self.text_obj.draw(screen, (position[0] + 10, position[1] + 10))
        if self.icon:
            screen.blit(self.icon, (position[0] + self.rect.width - 40, position[1] + 10))

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos, content_offset):
        adjusted_rect = self.rect.move(0, -content_offset)
        return adjusted_rect.collidepoint(mouse_pos)

    def handle_click(self):
        if self.callback:
            self.callback()

# Panel Class
class Panel:
    def __init__(self,x,y,height,width1,width2,color1,color2):
        self.height = height
        self.width1 = width1
        self.width2 = width2
        self.color1 = color1
        self.color2 = color2
        self.x = x
        self.y = y

    def draw_rectangle(self,screen):
        pg.draw.rect(screen, self.color1, (self.x , self.y,self.width1 , self.height))
        pg.draw.rect(screen, self.color2,(self.x , self.y, self.width2, self.height))

    def draw_lines(self,screen,width_spacing,margin,color):
        i = 0
        while i < screen.get_width() - margin : 
            pg.draw.rect(screen, color,(i + screen.get_width()/4, self.y,1 , self.height))
            i += (screen.get_width()) / width_spacing

# Function to handle "New Holder" addition
def add_new_text_pair1():
    global dynamic_texts_pair1, button1, icon_button
    if dynamic_texts_pair1:
        last_element = dynamic_texts_pair1[-1]
        y_offset = last_element.rect.y + 60  # Place new element 60 pixels below the last one
    else:
        y_offset = icon_button.rect.y - 5  # Initial y-coordinate for the first element

    # Shift all elements below the "New Holder" section down by 60 pixels
    for element in sidebar.elements:
        if element.rect.y >= y_offset:
            element.rect.y += 60

    # Add the new "New Holder" item
    new_text = impObj.RenamableText(f"New Holder Item {len(dynamic_texts_pair1) + 1}", font_button, (234, 248, 224), SCREEN_WIDTH - 325, y_offset)
    sidebar.add_element(new_text)
    dynamic_texts_pair1.append(new_text)

    # button1.rect.y +=20
    # icon_button.rect.y +=20

# Function to handle "New Bone" addition
def add_new_text_pair2():
    global dynamic_texts_pair1, dynamic_texts_pair2
    # Calculate the difference between the number of "New Holder" items and "New Bone" items
    difference = len(dynamic_texts_pair1) - len(dynamic_texts_pair2)
    
    # If there are no "New Holder" items, do nothing
    if difference <= 0:
        return

    # Add the necessary number of "New Bone" items
    for _ in range(difference):
        if dynamic_texts_pair2:
            last_element = dynamic_texts_pair2[-1]
            y_offset = last_element.rect.y + 60  # Place new element 60 pixels below the last one
        else:
            y_offset = icon_button1.rect.y - 5  # Initial y-coordinate for the first element

        # Shift all elements below the "New Bone" section down by 60 pixels
        for element in sidebar.elements:
            if element.rect.y >= y_offset:
                element.rect.y += 60

        # Add the new "New Bone" item
        new_text = Text(f"New Bone Item {len(dynamic_texts_pair2) + 1}", font_button, (234, 248, 224), SCREEN_WIDTH - 325, y_offset)
        sidebar.add_element(new_text)
        dynamic_texts_pair2.append(new_text)
        
# Function to recreate All Bones.
def recreate_bones():
    char.Rig.bones.clear()
    for i in range(len(char.Body.holders)):
        #list_holders=char.Body.holders.values()
        holder=char.Body.holders["holder_"+str(i)]
        bone_x=holder.position[0]+holder.scale[0]/2
        char.Rig.add_bone(pg.Vector2(bone_x-3,holder.position[1]+10),(30,holder.scale.y-20))


# Create scrollable sidebar
sidebar = ScrollablePanel(SCREEN_WIDTH - 350, 0, 350, SCREEN_HEIGHT, (79, 69, 87))

# Create initial headings
headings = [
    Text("Character", font_heading, (244, 238, 224), SCREEN_WIDTH - 325, 20),
    Text("Holder", font_heading, (244, 238, 224), SCREEN_WIDTH - 325, 80),
    Text("Rig", font_heading, (244, 238, 224), SCREEN_WIDTH - 325, 365),
    Text("Sprite", font_heading, (244, 238, 224), SCREEN_WIDTH - 325, 500),
]

for heading in headings:
    sidebar.add_element(heading)

# Create button text objects
button_text1 = Text("New Holder", font_button, (244, 238, 224), 0, 0)
button_text2 = Text("Add Bones", font_button, (244, 238, 224), 0, 0)

# Store dynamically created text objects
dynamic_texts_pair1 = []
dynamic_texts_pair2 = []

# Create buttons and add to sidebar
button1 = Button(SCREEN_WIDTH - 270, 130, 245, 50, DARK_GRAY, (109, 93, 110), button_text1)
button2 = Button(SCREEN_WIDTH - 270, 420, 245, 50, DARK_GRAY, (109, 93, 110), button_text2)

icon_button = Button(SCREEN_WIDTH - 325, 130, 50, 50, DARK_GRAY, (109, 93, 110), icon=icon_image, callback=add_new_text_pair1)
icon_button1 = Button(SCREEN_WIDTH - 325, 420, 60, 50, DARK_GRAY, (109, 93, 110), icon=icon_image, callback=add_new_text_pair2)

sidebar.add_element(button1)
sidebar.add_element(button2)
sidebar.add_element(icon_button)
sidebar.add_element(icon_button1)

pause_button = pg.transform.smoothscale(pg.image.load('Main_UI/Pause.png'),(64,64))
play_button = pg.transform.smoothscale(pg.image.load('Main_UI/Play.png'),(75,75))
record_button = pg.transform.smoothscale(pg.image.load('Main_UI/Record.png'),(64,64))
rewind_button = pg.transform.smoothscale(pg.image.load('Main_UI/Rewind.png'),(64,64))
fast_forward_button = pg.transform.smoothscale(pg.image.load('Main_UI/Fast_Forward.png'),(64,64))


while running:
    shared.mouse_pos = mouse_pos = pg.mouse.get_pos()
    panel=Panel(0,screen.get_height()-200,200,screen.get_width(),screen.get_width()/4,(79,69,87),(109,93,110))
    # poll for events  
    # pg.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        
        sidebar.handle_event(event)
        if event.type == pg.MOUSEBUTTONDOWN:
            # Only handle left mouse button clicks (button == 1)
            shared.mouse_down = True
            if event.button == 1:
                if(shared.current_holder_state==shared.holder_states[1]):
                    if icon_button.is_clicked(mouse_pos, sidebar.content_offset):
                        icon_button.handle_click()
                        shared.current_holder_state=shared.holder_states[3]
                        shared.mouse_down=False
                    if icon_button1.is_clicked(mouse_pos, sidebar.content_offset):
                        icon_button1.handle_click()
                        recreate_bones()
                # Handle text object clicks
                for element in sidebar.elements:
                    if isinstance(element, impObj.RenamableText):
                        result = element.handle_event(event)
                        if result:  # If a text object is clicked, set it as active
                            if active_text_object and active_text_object != result:
                                active_text_object.editing = False  # Reset the previous active object
                            active_text_object = result
            
                
    # if(shared.current_holder_state==shared.holder_states[4]):
    #     shared.current_holder_state=shared.holder_states[3]
    #     shared.mouse_down=False
    #     shared.mouse_state="buffer"     
    if(shared.current_holder_state==shared.holder_states[3] and shared.mouse_down):
            char.Body.intial_pos = position = pg.mouse.get_pos()
            print(char.Body.intial_pos)
            name = "holder_" + str(len(char.Body.holders))
            shared.current_holder_state = shared.holder_states[0]
            shared.mouse_down=False
            shared.mouse_state="buffer"
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")
    i = 1
    while i < screen.get_width():
        pg.draw.rect(screen, (0, 0, 0), (i, 0, 1, screen.get_height()), 5, 1)
        i += (screen.get_width()) / 20

    j = 1
    while j < screen.get_height():
        pg.draw.rect(screen, (0, 0, 0), (0, j, screen.get_width(), 1), 5, 1)
        j += (screen.get_height()) / 12
    panel.draw_rectangle(screen)
    panel.draw_lines(screen,15,30,(255,255,255))
    
    pg.draw.line(screen, WHITE , (383, 835), (0, 835), 3)
    pg.draw.line(screen, WHITE , (383, screen.get_height() - 200), (383, screen.get_height()), 3)
    pg.draw.line(screen, WHITE , (1200, screen.get_height() - 200), (1200, screen.get_height()), 3)
    

    pause = pause_button.get_rect(center = (120, screen.get_height() - 165))
    play = play_button.get_rect(center = (258, screen.get_height()-165))
    record = record_button.get_rect(center = (190, screen.get_height()-165))
    fastforward = fast_forward_button.get_rect(center = (50,screen.get_height()-165))
    rewind = rewind_button.get_rect(center = (330,screen.get_height()-165))
    
    screen.blit(pause_button,pause)
    screen.blit(play_button,play)
    screen.blit(record_button,record)
    screen.blit(fast_forward_button, fastforward)
    screen.blit(rewind_button, rewind)

    # IO
    if(shared.current_holder_state==shared.holder_states[0]):

       scale=mouse_pos-pg.Vector2(char.Body.intial_pos)
       pg.draw.rect(screen,"black",(char.Body.intial_pos,scale),5)
       #pg.draw.rect(screen,"grey",(char.Body.intial_pos+pg.Vector2(4,4),scale-pg.Vector2(8,8)))
       if(shared.mouse_down):
          char.Body.add_holder(name,pos=position,scale=scale)
          shared.current_holder_state=shared.holder_states[1]
          shared.mouse_down=False
    if(shared.mouse_state=="buffer"):
       shared.mouse_down=False
       shared.mouse_state=""
    # RENDER YOUR GAME HERE
    char.load(screen)
    char.Body.load_frame(screen)
    #print(char.Body.holders.keys())

    # flip() the display to put your work on screen
    sidebar.draw(screen)
    char.Body.add_frame_part(screen,char.Rig)
    char.Rig.display_bones(screen)
    pg.display.flip()
   
    clock.tick(60)  # limits FPS to 60

pg.quit()