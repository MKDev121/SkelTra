import pygame as pg
import character
import shared 
import math
# pg setup
pg.init()
#screen = pg.display.set_mode((1280, 720))
clock = pg.time.Clock()
running = True
pg.display.set_caption("SkelTra")
char=character.Character()
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Initialize screen
screen = pg.display.set_mode()
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
#pg.display.set_caption("Scrollable Sidebar")

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
            if event.button == 4:
                self.scroll(-30)
            elif event.button == 5:
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

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def handle_click(self):
        if self.callback:
            self.callback()

# Create scrollable sidebar
sidebar = ScrollablePanel(SCREEN_WIDTH - 350, 0, 350, SCREEN_HEIGHT, (79, 69, 87))

# Create initial headings
headings = [
    Text("Character", font_heading, (244, 238, 224), SCREEN_WIDTH - 325, 20),
    Text("Holder", font_heading, (244, 238, 224), SCREEN_WIDTH - 325, 80),
    Text("Head", font_heading, (244, 238, 224), SCREEN_WIDTH - 325, 150),
    Text("Body", font_heading, (244, 238, 224), SCREEN_WIDTH - 325, 220),
    Text("Rig", font_heading, (244, 238, 224), SCREEN_WIDTH - 325, 365),
    Text("Sprite", font_heading, (244, 238, 224), SCREEN_WIDTH - 325, 500),
]

for heading in headings:
    sidebar.add_element(heading)

# Create button text objects
button_text1 = Text("New Holder", font_button, (244, 238, 224), 0, 0)
button_text2 = Text("New Bone", font_button, (244, 238, 224), 0, 0)

# Store dynamically created text objects
dynamic_texts_pair1 = []
dynamic_texts_pair2 = []

# Function to handle "New Holder" addition
def add_new_text_pair1():
    global dynamic_texts_pair1,button1,icon_button
    if dynamic_texts_pair1:
        last_element = dynamic_texts_pair1[-1]
        y_offset = last_element.rect.y + 60  # Place new element 60 pixels below the last one
    else:
        y_offset = 280  # Initial y-coordinate for the first element

    # Shift all elements below the "New Holder" section down by 60 pixels
    for element in sidebar.elements:
        if element.rect.y >= y_offset:
            element.rect.y += 60

    # Add the new "New Holder" item
    new_text = Text(f"New Holder Item {len(dynamic_texts_pair1) + 1}", font_button, (234, 248, 224), SCREEN_WIDTH - 325, y_offset)
    sidebar.add_element(new_text)
    dynamic_texts_pair1.append(new_text)

    button1.rect.y +=60
    icon_button.rect.y +=60

# Function to handle "New Bone" addition
def add_new_text_pair2():
    global dynamic_texts_pair2
    if dynamic_texts_pair2:
        last_element = dynamic_texts_pair2[-1]
        y_offset = last_element.rect.y + 60  # Place new element 60 pixels below the last one
    else:
        
        y_offset = 430  # Initial y-coordinate for the first element

    # Shift all elements below the "New Bone" section down by 60 pixels
    for element in sidebar.elements:
        if element.rect.y >= y_offset:
            element.rect.y += 60

    # Add the new "New Bone" item
    new_text = Text(f"New Bone Item {len(dynamic_texts_pair2) + 1}", font_button, (234, 248, 224), SCREEN_WIDTH - 325, y_offset)
    sidebar.add_element(new_text)
    dynamic_texts_pair2.append(new_text)

# Create buttons and add to sidebar
button1 = Button(SCREEN_WIDTH - 270, 270, 245, 50, DARK_GRAY, (109, 93, 110), button_text1)
button2 = Button(SCREEN_WIDTH - 270, 420, 245, 50, DARK_GRAY, (109, 93, 110), button_text2)
icon_button = Button(SCREEN_WIDTH - 325, 270, 50, 50, DARK_GRAY, (109, 93, 110), icon=icon_image, callback=add_new_text_pair1)
icon_button1 = Button(SCREEN_WIDTH - 325, 420, 50, 50, DARK_GRAY, (109, 93, 110), icon=icon_image, callback=add_new_text_pair2)

sidebar.add_element(button1)
sidebar.add_element(button2)
sidebar.add_element(icon_button)
sidebar.add_element(icon_button1)

while running:
    shared.mouse_pos=mouse_pos=pg.mouse.get_pos()
    # poll for events
    # pg.QUIT event means the user clicked X to close your window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type==pg.KEYDOWN:
           if event.key ==pg.K_a:
            char.Body.intial_pos = position = pg.mouse.get_pos()
            name="holder_"+str(len(char.Body.holders))
            shared.current_holder_state=shared.holder_states[0]
            

            keydown=True
        if event.type==pg.MOUSEBUTTONDOWN:
            if icon_button.is_clicked(mouse_pos):
                icon_button.handle_click()
            if icon_button1.is_clicked(mouse_pos):
                icon_button1.handle_click()
            shared.mouse_down=True
    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("grey")
    i = 1
    while i < screen.get_width():
        pg.draw.rect(screen,(0,0,0),(i,0,1,screen.get_height()),5,1)
        i += (screen.get_width())/15

    j = 1
    while j < screen.get_height():
        pg.draw.rect(screen,(0,0,0),(0,j,screen.get_width(),1),5,1)
        j += (screen.get_height())/10

    
    # draw a rectangle
    # pg.draw.rect(screen, (0,0,0), (1,screen.get_height(),100,150)) #-> Rect
    # pg.draw.rect(screen, (0,0,0), (10,10,100,150), width=0, border_radius=0, border_top_left_radius=-1, border_top_right_radius=-1, border_bottom_left_radius=-1, border_bottom_right_radius=-1) #-> Rect

    # IO
    if(shared.current_holder_state==shared.holder_states[0]):
       
       scale=mouse_pos-pg.Vector2(char.Body.intial_pos)
       pg.draw.rect(screen,"black",(char.Body.intial_pos,scale))
       pg.draw.rect(screen,"grey",(char.Body.intial_pos+pg.Vector2(10,10),scale-pg.Vector2(20,20)))
       if(shared.mouse_down):
          char.Body.add_holder(name,pos=position,scale=scale)
          shared.current_holder_state=shared.holder_states[1]
          shared.mouse_state="buffer"
    if(shared.mouse_state=="buffer"):
       shared.mouse_down=False
       shared.mouse_state=""
    # RENDER YOUR GAME HERE
    char.load(screen)
    char.Body.load_frame(screen)
    char.Body.add_frame_part()
    # flip() the display to put your work on screen
    
    sidebar.draw(screen)
    pg.display.flip()
    clock.tick(60)  # limits FPS to 60

pg.quit()