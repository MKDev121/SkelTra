import pygame as pg
import sys

# Initialize pg
pg.init()

# Colors
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Initialize screen
screen = pg.display.set_mode()
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pg.display.set_caption("Scrollable Sidebar")

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
    global dynamic_texts_pair1, button1, icon_button
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
    
    screen.blit()
    # Move the "New Holder" button and icon button down by 60 pixels
    button1.rect.y += 60
    icon_button.rect.y += 60

# Function to handle "New Bone" addition
def add_new_text_pair2():
    global dynamic_texts_pair2, button2, icon_button1
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

    # Move the "New Bone" button and icon button down by 60 pixels
    button2.rect.y += 60
    icon_button1.rect.y += 60

# Create buttons and add to sidebar
button1 = Button(SCREEN_WIDTH - 270, 270, 245, 50, DARK_GRAY, (109, 93, 110), button_text1)
button2 = Button(SCREEN_WIDTH - 270, 420, 245, 50, DARK_GRAY, (109, 93, 110), button_text2)
icon_button = Button(SCREEN_WIDTH - 325, 270, 50, 50, DARK_GRAY, (109, 93, 110), icon=icon_image, callback=add_new_text_pair1)
icon_button1 = Button(SCREEN_WIDTH - 325, 420, 50, 50, DARK_GRAY, (109, 93, 110), icon=icon_image, callback=add_new_text_pair2)

sidebar.add_element(button1)
sidebar.add_element(button2)
sidebar.add_element(icon_button)
sidebar.add_element(icon_button1)

pause_button = pg.transform.smoothscale(pg.image.load('UI_Pics/pause.png'),(64,64))
play_button = pg.transform.smoothscale(pg.image.load('UI_Pics/play.png'),(64,64))
record_button = pg.transform.smoothscale(pg.image.load('UI_Pics/BtnR.png'),(64,64))
# Main loop
running = True
while running:
    screen.fill((57, 54, 70))
    pg.draw.rect(screen, (79,69,87), (0,screen.get_height()-200,screen.get_width(),200))
    pg.draw.rect(screen, (109,93,110), (0,screen.get_height()-200,screen.get_width()/5,200))  
    mouse_pos = pg.mouse.get_pos()

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        sidebar.handle_event(event)

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            # Adjust mouse position for scroll offset
            adjusted_mouse_pos = (mouse_pos[0], mouse_pos[1] + sidebar.content_offset)
            if icon_button.is_clicked(adjusted_mouse_pos):
                icon_button.handle_click()
            if icon_button1.is_clicked(adjusted_mouse_pos):
                icon_button1.handle_click()

    
    sidebar.draw(screen)


    pause = pause_button.get_rect(center = (50,screen.get_height()-100))
    play = play_button.get_rect(center = (150,screen.get_height()-100))
    record = record_button.get_rect(center = (250,screen.get_height()-100))
    screen.blit(pause_button,pause)
    screen.blit(play_button,play)
    screen.blit(record_button,record)


    pg.display.flip()

pg.quit()
sys.exit()