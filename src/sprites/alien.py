import pygame
from ..constants import RED

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Create alien appearance
        self.image = pygame.Surface((40, 30))
        self.image.fill(RED)
        
        # Set initial position and movement speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1  # Initial movement speed (positive = right, negative = left)

    def update(self):
        self.rect.x += self.speed