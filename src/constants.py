import os
import pygame

# Game window dimensions
WIDTH, HEIGHT = 800, 600

# Asset paths
IMG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')

# RGB color definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Game performance settings
FPS = 60  # Frames per second

# Enemy sprites
ENEMY_SPRITES = ['enemy1.png', 'enemy2.png', 'enemy3.png', 'enemy4.png']
