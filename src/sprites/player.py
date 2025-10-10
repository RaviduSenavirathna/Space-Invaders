import os
import pygame
from ..constants import WIDTH, HEIGHT, GREEN, WHITE, IMG_DIR

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load player ship image
        try:
            self.image = pygame.image.load(os.path.join(IMG_DIR, 'blue_ship.png')).convert_alpha()
            # Scale image if needed (adjust size as necessary)
            self.image = pygame.transform.scale(self.image, (50, 40))
        except pygame.error:
            # Fallback to original triangle shape if image loading fails
            self.image = pygame.Surface((50, 40))
            self.image.fill(GREEN)
            pygame.draw.polygon(self.image, WHITE, [(25, 0), (0, 40), (50, 40)])
        
        # Set initial position and properties
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5
        
        # Health system
        self.max_health = 5
        self.health = self.max_health

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self, all_sprites, bullets):
        from .bullet import Bullet
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

    def take_damage(self):
        self.health -= 1
        return self.health <= 0

    def heal(self):
        if self.health < self.max_health:
            self.health += 1

    def reset_health(self):
        self.health = self.max_health