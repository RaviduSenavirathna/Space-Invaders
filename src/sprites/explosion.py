import pygame
import os
from ..constants import *

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y):
        super().__init__()
        self.images = []

        # Load the 3 snowflake images
        try:
            for i in range(3):  # Using 3 frames for the explosion
                img = pygame.image.load(os.path.join(IMG_DIR, f'explosion{i}.png')).convert_alpha()
                img = pygame.transform.scale(img, (30, 30))  # Adjust size as needed
                self.images.append(img)
        except pygame.error:
            # Fallback if images not found
            self.images = [pygame.Surface((30, 30)) for _ in range(3)]
            for img in self.images:
                img.fill((135, 206, 235))  # Light blue color as fallback


        # Load sound effects
        try:
            self.explosion_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, 'explosion.wav'))
            self.explosion_sound.set_volume(0.3)  # Set volume to a reasonable level
        except pygame.error as e:
            print(f"Could not load sound effects: {e}")
            self.explosion_sound = None
        if self.explosion_sound:
            self.explosion_sound.play() 

        
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (center_x, center_y)
        self.frame_rate = 8  # Speed of animation
        self.frame_count = 0

    def update(self):
        self.frame_count += 1
        if self.frame_count >= self.frame_rate:
            self.frame_count = 0
            self.index += 1
            if self.index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.index]