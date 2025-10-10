import os
import pygame

# Game window dimensions
WIDTH, HEIGHT = 800, 600

# Asset paths
IMG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')
FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fonts')

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

# Health bar images
HEALTH_BAR_IMAGES = [f'hb{i}.png' for i in range(6)]  # hb0 to hb5
HEALTH_BAR_POSITION = (WIDTH - 150, 10)  # Position in top right corner

# Score display settings
SCORE_POSITION = (10, 10)  # Moved down 2 pixels from original (10, 10)
SCORE_ICON_SIZE = (28 ,28)  # Adjust based on your star.png size
SCORE_TEXT_OFFSET = 40  # Distance between icon and text

# Font settings
BYTE_BOUNCE_FONT = os.path.join(FONT_DIR, 'ByteBounce.ttf') # Path to ByteBounce font
FONT_SIZE = 40 # Font size for score and other text
