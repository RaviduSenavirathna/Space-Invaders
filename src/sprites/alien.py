import os
import pygame
from ..constants import RED, IMG_DIR

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load alien ship image
        try:
            self.image = pygame.image.load(os.path.join(IMG_DIR, 'enemy1.png')).convert_alpha()
            # Scale image if needed (adjust size as necessary)
            self.image = pygame.transform.scale(self.image, (40, 30))
        except pygame.error:
            # Fallback to original rectangle shape if image loading fails
            self.image = pygame.Surface((40, 30))
            self.image.fill(RED)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1  # Initial movement speed (positive = right, negative = left)

    def update(self):
        self.rect.x += self.speed