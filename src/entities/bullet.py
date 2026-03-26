import os
import pygame
from ..utils.constants import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load(os.path.join(IMG_PROJECTILE_DIR, PLAYER_LASER)).convert_alpha()
            # Scale the laser image to appropriate size
            self.image = pygame.transform.scale(self.image, (40, 120))
        except pygame.error:
            # Fallback to original rectangle if image fails to load
            self.image = pygame.Surface((4, 15))
            self.image.fill(YELLOW)
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()