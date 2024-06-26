import pygame

class Button():
    def __init__(self, x: int, y: int, image: object, scale: float):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.clicked = False
    
    def is_clicked(self) -> bool:
        # Returns True when the button is clicked, False otherwise
        clicked = False
        # Gets the mouse position
        mouse_pos = pygame.mouse.get_pos()
        # Check if the mouse clicks the button
        if self.rect.collidepoint(mouse_pos) and pygame.MOUSEBUTTONDOWN and not self.clicked:
            self.clicked = True
            clicked = True
        # Makes sures we can click the button again later
        if pygame.MOUSEBUTTONUP:
            self.clicked = False
        return clicked

    def draw(self, window: object):
        # Draws the button onto the screen
        window.blit(self.image, (self.rect.x, self.rect.y))