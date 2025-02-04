import pygame as pg
import sys
import tkinter as tk
from tkinter import filedialog

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
font_numbers = pg.font.Font(None, 24)  # Font for the numbers

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

class Panel:
    def __init__(self, x, y, height, width1, width2, color1, color2):
        self.height = height
        self.width1 = width1
        self.width2 = width2
        self.color1 = color1
        self.color2 = color2
        self.x = x
        self.y = y

    def draw_rectangle(self, screen):
        pg.draw.rect(screen, self.color1, (self.x, self.y, self.width1, self.height))
        pg.draw.rect(screen, self.color2, (self.x, self.y, self.width2, self.height))

    def draw_lines(self, screen, width_spacing, margin, color):
        i = 0
        number = 0
        while i < screen.get_width() - margin:
            x_position = i + screen.get_width() / 4
            pg.draw.rect(screen, color, (x_position, self.y, 1, self.height))
            
            # Draw the number to the right of the line
            number_text = RenamableText(str(number), font_numbers, WHITE, x_position + 5, self.y + 10)
            number_text.draw(screen, (x_position + 5, self.y + 10))
            
            i += (screen.get_width()) / width_spacing
            number += 15

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

    # Add the new "New Holder" item (editable)
    new_text = RenamableText(f"New Holder Item {len(dynamic_texts_pair1) + 1}", font_button, (234, 248, 224), SCREEN_WIDTH - 325, y_offset, editable=True)
    sidebar.add_element(new_text)
    dynamic_texts_pair1.append(new_text)
    
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

    # Add the new "New Bone" item (editable)
    new_text = RenamableText(f"New Bone Item {len(dynamic_texts_pair2) + 1}", font_button, (234, 248, 224), SCREEN_WIDTH - 325, y_offset, editable=True)
    sidebar.add_element(new_text)
    dynamic_texts_pair2.append(new_text)

    # Move the "New Bone" button and icon button down by 60 pixels
    button2.rect.y += 60
    icon_button1.rect.y += 60

    # Add the new "New Bone" item
    new_text = RenamableText(f"New Bone Item {len(dynamic_texts_pair2) + 1}", font_button, (234, 248, 224), SCREEN_WIDTH - 325, y_offset)
    sidebar.add_element(new_text)
    dynamic_texts_pair2.append(new_text)

    # Move the "New Bone" button and icon button down by 60 pixels
    button2.rect.y += 60
    icon_button1.rect.y += 60

def open_file_explorer(paths):
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    file_path = filedialog.askopenfilename(title = "Select a File", 
                                           filetypes = [("Portable Network Graphics", ".png"),
                                                        ("Joint Photographic Experts Group", ".jpg"),
                                                        ("Joint Photographic Experts Group", ".jpeg")])

    if file_path:
        paths.append(file_path)

# Create scrollable sidebar
sidebar = ScrollablePanel(SCREEN_WIDTH - 350, 0, 350, SCREEN_HEIGHT, (79, 69, 87))

# Create initial headings (not editable)
headings = [
    RenamableText("Character", font_heading, (244, 238, 224), SCREEN_WIDTH - 325, 20, editable=False),
    RenamableText("Holder", font_heading, (244, 238, 224), SCREEN_WIDTH - 325, 80, editable=False),
    RenamableText("Head", font_heading, (244, 238, 224), SCREEN_WIDTH - 325, 150, editable=False),
    RenamableText("Body", font_heading, (244, 238, 224), SCREEN_WIDTH - 325, 220, editable=False),
    RenamableText("Rig", font_heading, (244, 238, 224), SCREEN_WIDTH - 325, 365, editable=False),
    RenamableText("Sprite", font_heading, (244, 238, 224), SCREEN_WIDTH - 325, 500, editable=False),
]

for heading in headings:
    sidebar.add_element(heading)

# Create button text objects
button_text1 = RenamableText("New Holder", font_button, (244, 238, 224), 0, 0)
button_text2 = RenamableText("New Bone", font_button, (244, 238, 224), 0, 0)

# Store dynamically created text objects
dynamic_texts_pair1 = []
dynamic_texts_pair2 = []

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
play_button = pg.transform.smoothscale(pg.image.load('UI_Pics/right.png'),(64,64))
record_button = pg.transform.smoothscale(pg.image.load('UI_Pics/BtnMisc.png'),(64,64))

paths = []

# Track the active text object being edited
active_text_object = None

running = True
while running:
    screen.fill((57, 54, 70))
    panel = Panel(0, screen.get_height() - 200, 200, screen.get_width(), screen.get_width() / 4, (79, 69, 87), (109, 93, 110))
    panel.draw_rectangle(screen)
    panel.draw_lines(screen, 15, 30, (255, 255, 255))

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

            # Handle text object clicks
            for element in sidebar.elements:
                if isinstance(element, RenamableText):
                    result = element.handle_event(event)
                    if result:  # If a text object is clicked, set it as active
                        if active_text_object and active_text_object != result:
                            active_text_object.editing = False  # Reset the previous active object
                        active_text_object = result

        if event.type == pg.KEYDOWN:
            if active_text_object:
                active_text_object.handle_event(event)
            else:
                if event.key == pg.K_f:
                    open_file_explorer(paths)
                elif event.key == pg.K_q:
                    running = False
    
    sidebar.draw(screen)

    pause = pause_button.get_rect(center=(85, screen.get_height() - 167))
    play = play_button.get_rect(center=(185, screen.get_height() - 167))
    record = record_button.get_rect(center=(285, screen.get_height() - 167))
    screen.blit(pause_button, pause)
    screen.blit(play_button, play)
    screen.blit(record_button, record)

    pg.display.flip()

pg.quit()
sys.exit() 