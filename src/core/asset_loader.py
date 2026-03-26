import pygame
import os
from src.utils.constants import IMG_DIR, SOUND_DIR

class AssetLoader:
    def __init__(self):
        self.images = {}
        self.sounds = {}

    def load_image(self, name, path):
        if name not in self.images:
            self.images[name] = pygame.image.load(path).convert_alpha()
        return self.images[name]

    def load_sound(self, name, path):
        if name not in self.sounds:
            self.sounds[name] = pygame.mixer.Sound(path)
        return self.sounds[name]