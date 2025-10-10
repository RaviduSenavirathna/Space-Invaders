import os
import random
import pygame
from ..constants import RED, IMG_DIR, ENEMY_SPRITES

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Load random alien ship image
        try:
            self.alien_type = random.choice(ENEMY_SPRITES)
            self.image = pygame.image.load(os.path.join(IMG_DIR, self.alien_type)).convert_alpha()
            self.image = pygame.transform.scale(self.image, (40, 30))
        except pygame.error:
            self.alien_type = 'enemy1.png'
            self.image = pygame.Surface((40, 30))
            self.image.fill(RED)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1  # Initial movement speed (positive = right, negative = left)

    def update(self):
        self.rect.x += self.speed