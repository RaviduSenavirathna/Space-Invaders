import os

# Game window dimensions
WIDTH, HEIGHT = 800, 600

# Asset paths
IMG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'images')

# Enemy sprites
ENEMY_SPRITES = ['enemy1.png', 'enemy2.png', 'enemy3.png', 'enemy4.png']

# Laser images
PLAYER_LASER = 'laser1.png'
ENEMY_LASERS = {
    'enemy1.png': 'enemy1l.png',
    'enemy2.png': 'enemy2l.png',
    'enemy3.png': 'enemy3l.png',
    'enemy4.png': 'enemy4l.png'
}

# Health bar images
HEALTH_BAR_IMAGES = [f'hb{i}.png' for i in range(6)]
HEALTH_BAR_POSITION = (WIDTH - 150, 10)

# Score display settings
SCORE_POSITION = (10, 10)
SCORE_ICON_SIZE = (30, 30)
SCORE_TEXT_OFFSET = 40

# RGB color definitions
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Game performance settings
FPS = 60

# Font settings
FONT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'fonts')
BYTE_BOUNCE_FONT = os.path.join(FONT_DIR, 'ByteBounce.ttf')
FONT_SIZE = 36

# Sound paths
SOUND_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'sound effects')
# Sound effects
LASER_SOUND = 'laser_shoot.wav'
HIT_SOUND = 'hit_hurt.wav'
EXPLOSION_SOUND = 'explosion.wav'