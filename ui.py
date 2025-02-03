import pygame
import sys

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

background_color = WHITE  # Default background

# Initialize screen
screen = pygame.display.set_mode()
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("Sidebar with Buttons, Labels, and Headings")

# Fonts
font_heading = pygame.font.Font(None, 48)  # Larger font for headings
font_button = pygame.font.Font(None, 36)  # Font for buttons

# Text Class
class Text:
    def __init__(self, text, font, color):
        self.text = text
        self.font = font
        self.color = color
        self.render_text()

    def render_text(self):
        """Renders the text surface."""
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect()

    def draw(self, screen, position):
        """Draws the text on the screen at the specified position."""
        screen.blit(self.surface, position)

# Button Class
class Button:
    def __init__(self, x, y, width, height, color, hover_color, text_obj=None, icon=None, callback=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text_obj = text_obj
        self.color = color
        self.hover_color = hover_color
        self.hovered = False
        self.icon = icon
        self.callback = callback

    def draw(self, screen):
        pygame.draw.rect(screen, self.hover_color if self.hovered else self.color, self.rect)

        if self.text_obj:
            text_position = (
                self.rect.centerx - self.text_obj.rect.width // 2,
                self.rect.centery - self.text_obj.rect.height // 2
            )
            self.text_obj.draw(screen, text_position)

        if self.icon:
            icon_x = self.rect.x + 10
            icon_y = self.rect.centery - self.icon.get_height() // 2
            screen.blit(self.icon, (icon_x, icon_y))

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.hovered and pygame.mouse.get_pressed()[0]

    def handle_click(self):
        if self.callback:
            self.callback()

# Panel Class
class Panel:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.buttons = []

    def add_button(self, button):
        self.buttons.append(button)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        for button in self.buttons:
            button.draw(screen)

    def handle_event(self, mouse_pos):
        for button in self.buttons:
            button.check_hover(mouse_pos)
            if button.is_clicked(mouse_pos):
                button.handle_click()

# Load Icon Image
try:
    icon_image = pygame.image.load("add-outline.png")
    icon_image = pygame.transform.scale(icon_image, (30, 30))
except pygame.error:
    print("Error: Image 'add-outline.png' not found. Make sure it's in the correct directory.")
    icon_image = None

# Create a panel
sidebar = Panel(SCREEN_WIDTH - 350, 0, 350, SCREEN_HEIGHT, LIGHT_GRAY)

# Create text objects for buttons
button_text1 = Text("New Holder", font_button, WHITE)
button_text2 = Text("New Bone", font_button, WHITE)

# List to store dynamically created text objects for each pair
dynamic_texts_pair1 = []
dynamic_texts_pair2 = []

# Track initial positions of the buttons
initial_positions_pair1 = {
    "button1": (SCREEN_WIDTH - 270, 270),
    "icon_button": (SCREEN_WIDTH - 325, 270),
}
initial_positions_pair2 = {
    "button2": (SCREEN_WIDTH - 270, 420),
    "icon_button1": (SCREEN_WIDTH - 325, 420),
}

# Track the number of added text objects for each pair
text_count_pair1 = 0
text_count_pair2 = 0

# Function to handle the "+" button click for the first pair
def add_new_text_pair1():
    global dynamic_texts_pair1, text_count_pair1
    # Create new text object at the initial position of the display button
    new_text = Text(f"New Holder Item {text_count_pair1 + 1}", font_button, WHITE)
    dynamic_texts_pair1.append((new_text, (initial_positions_pair1["button1"][0], initial_positions_pair1["button1"][1] + 60 * text_count_pair1)))
    text_count_pair1 += 1
    # Shift all elements below the first pair down
    shift_amount = 60
    for element in all_elements:
        if element.rect.y >= initial_positions_pair1["button1"][1]:
            element.rect.y += shift_amount
    # Update positions of dynamic texts in pair2
    for i, (text_obj, pos) in enumerate(dynamic_texts_pair2):
        if pos[1] >= initial_positions_pair1["button1"][1]:
            dynamic_texts_pair2[i] = (text_obj, (pos[0], pos[1] + shift_amount))

# Function to handle the "+" button click for the second pair
def add_new_text_pair2():
    global dynamic_texts_pair2, text_count_pair2
    # Create new text object at the initial position of the display button
    new_text = Text(f"New Bone Item {text_count_pair2 + 1}", font_button, WHITE)
    dynamic_texts_pair2.append((new_text, (initial_positions_pair2["button2"][0], initial_positions_pair2["button2"][1] + 60 * text_count_pair2)))
    text_count_pair2 += 1
    # Shift all elements below the second pair down
    shift_amount = 60
    for element in all_elements:
        if element.rect.y >= initial_positions_pair2["button2"][1]:
            element.rect.y += shift_amount
    # Update positions of dynamic texts in pair1
    for i, (text_obj, pos) in enumerate(dynamic_texts_pair1):
        if pos[1] >= initial_positions_pair2["button2"][1]:
            dynamic_texts_pair1[i] = (text_obj, (pos[0], pos[1] + shift_amount))

# Add buttons to the panel
button1 = Button(SCREEN_WIDTH - 270, 270, 245, 50, DARK_GRAY, BLUE, button_text1)
button2 = Button(SCREEN_WIDTH - 270, 420, 245, 50, DARK_GRAY, BLUE, button_text2)
icon_button = Button(SCREEN_WIDTH - 325, 270, 50, 50, DARK_GRAY, BLACK, icon=icon_image, callback=add_new_text_pair1)
icon_button1 = Button(SCREEN_WIDTH - 325, 420, 50, 50, DARK_GRAY, BLACK, icon=icon_image, callback=add_new_text_pair2)

sidebar.add_button(button1)
sidebar.add_button(button2)
sidebar.add_button(icon_button)
sidebar.add_button(icon_button1)

# Create heading text objects
heading_text = Text("Character", font_heading, BLACK)
heading_text1 = Text("Holder", font_heading, BLACK)
heading_text2 = Text("Head", font_heading, BLACK)
heading_text3 = Text("Body", font_heading, BLACK)
heading_text4 = Text("Rig", font_heading, BLACK)
heading_text5 = Text("Sprite", font_heading, BLACK)

# Set initial positions for heading text
heading_text.rect.topleft = (SCREEN_WIDTH - 260, 20)
heading_text1.rect.topleft = (SCREEN_WIDTH - 325, 80)
heading_text2.rect.topleft = (SCREEN_WIDTH - 325, 150)
heading_text3.rect.topleft = (SCREEN_WIDTH - 325, 220)
heading_text4.rect.topleft = (SCREEN_WIDTH - 325, 365)
heading_text5.rect.topleft = (SCREEN_WIDTH - 325, 500)

# List to store all elements for dynamic position updates
all_elements = [button1, button2, icon_button, icon_button1, heading_text, heading_text1, heading_text2, heading_text3, heading_text4, heading_text5]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()
    sidebar.handle_event(mouse_pos)

    screen.fill(WHITE)
    sidebar.draw(screen)

    # Draw heading text
    heading_text.draw(screen, heading_text.rect.topleft)
    heading_text1.draw(screen, heading_text1.rect.topleft)
    heading_text2.draw(screen, heading_text2.rect.topleft)
    heading_text3.draw(screen, heading_text3.rect.topleft)
    heading_text4.draw(screen, heading_text4.rect.topleft)
    heading_text5.draw(screen, heading_text5.rect.topleft)

    # Draw dynamically created text objects for the first pair
    for text_obj, position in dynamic_texts_pair1:
        text_obj.draw(screen, position)

    # Draw dynamically created text objects for the second pair
    for text_obj, position in dynamic_texts_pair2:
        text_obj.draw(screen, position)

    pygame.display.flip()

pygame.quit()
sys.exit()