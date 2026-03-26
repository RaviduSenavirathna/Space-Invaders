import os
import pygame
from ..utils.constants import *

class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, alien_type):
        super().__init__()
        try:
            laser_image = ENEMY_LASERS.get(alien_type, 'enemy1l.png')
            self.image = pygame.image.load(os.path.join(IMG_PROJECTILE_DIR, laser_image)).convert_alpha()
            # Scale the laser image to appropriate size
            self.image = pygame.transform.scale(self.image, (6, 20))
        except pygame.error:
            # Fallback to original rectangle if image fails to load
            self.image = pygame.Surface((4, 15))
            self.image.fill(RED)
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = 3 # Speed of the alien bullet

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()