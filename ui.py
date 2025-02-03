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
    def __init__(self, x, y, width, height, color, hover_color, text_obj=None, icon=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text_obj = text_obj
        self.color = color
        self.hover_color = hover_color
        self.hovered = False
        self.icon = icon

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
                if button.text_obj:
                    print(f"Button '{button.text_obj.text}' clicked!")
                else:
                    print("Icon button clicked!")  # Prevent quitting when clicking icon
                    return  # Prevent it from acting like a normal button

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

# Add buttons to the panel
button1 = Button(SCREEN_WIDTH - 270, 270, 225, 50, DARK_GRAY, BLUE, button_text1)
button2 = Button(SCREEN_WIDTH - 325, 420, 300, 50, DARK_GRAY, BLUE, button_text2)
icon_button = Button(SCREEN_WIDTH - 325, 270, 50, 50, DARK_GRAY, BLACK, icon=icon_image)  # ✅ Assign the icon

sidebar.add_button(button1)
sidebar.add_button(button2)
sidebar.add_button(icon_button)

heading_text = Text("Character", font_heading, BLACK)
heading_text1 = Text("Holder", font_heading, BLACK)
heading_text2 = Text("Head", font_heading, BLACK)
heading_text3 = Text("Body", font_heading, BLACK)
heading_text4 = Text("Rig", font_heading, BLACK)
heading_text5 = Text("Sprite", font_heading, BLACK)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()
    sidebar.handle_event(mouse_pos)

    screen.fill(WHITE)
    sidebar.draw(screen)

    heading_text.draw(screen, (SCREEN_WIDTH - 260, 20))
    heading_text1.draw(screen, (SCREEN_WIDTH - 325, 80))
    heading_text2.draw(screen, (SCREEN_WIDTH - 325, 150))
    heading_text3.draw(screen, (SCREEN_WIDTH - 325, 220))
    heading_text4.draw(screen, (SCREEN_WIDTH - 325, 365))
    heading_text5.draw(screen, (SCREEN_WIDTH - 325, 500))

    pygame.display.flip()

pygame.quit()
sys.exit()
