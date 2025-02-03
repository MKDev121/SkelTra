import pygame
import sys

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode()
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("Sidebar with Buttons, Labels, and Headings")

# Fonts
font_heading = pygame.font.Font(None, 48)  # Larger font for headings
font_label = pygame.font.Font(None, 24)   # Smaller font for labels
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
    def __init__(self, x, y, width, height, text_obj, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text_obj = text_obj
        self.color = color
        self.hover_color = hover_color
        self.hovered = False

    def draw(self, screen):
        # Change color if hovered
        if self.hovered:
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        
        # Draw the text centered on the button
        text_position = (
            self.rect.centerx - self.text_obj.rect.width // 2,
            self.rect.centery - self.text_obj.rect.height // 2
        )
        self.text_obj.draw(screen, text_position)

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
                print(f"Button '{button.text_obj.text}' clicked!")
                # You can add specific functionality for each button here

# Create a panel
sidebar = Panel(SCREEN_WIDTH - 350, 0, 350, SCREEN_HEIGHT, LIGHT_GRAY)

# Create text objects for buttons
button_text1 = Text("Head", font_button, WHITE)
button_text2 = Text("Body", font_button, WHITE)
button_text3 = Text("New Holder", font_button, WHITE)
button_text4 = Text("Bone-1", font_button, WHITE)

# Add buttons to the panel
button1 = Button(SCREEN_WIDTH - 325, 150, 300, 50, button_text1, DARK_GRAY, BLUE)
button2 = Button(SCREEN_WIDTH - 325, 220, 300, 50, button_text2, DARK_GRAY, BLUE)
button3 = Button(SCREEN_WIDTH - 290, 290, 260, 50, button_text3, DARK_GRAY, BLUE)
button4 = Button(SCREEN_WIDTH - 325, 425, 300, 50, button_text4, DARK_GRAY, BLUE)


sidebar.add_button(button1)
sidebar.add_button(button2)
sidebar.add_button(button3)
sidebar.add_button(button4)

heading_text = Text("Character", font_heading, BLACK)
heading_text1 = Text("Holder",font_heading,BLACK)
heading_text2 = Text("Rig",font_heading,BLACK)

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
    heading_text2.draw(screen, (SCREEN_WIDTH - 325, 365))

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()