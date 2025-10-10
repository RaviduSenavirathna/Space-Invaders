import pygame
from ..constants import WIDTH, HEIGHT, GREEN, WHITE

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)
        pygame.draw.polygon(self.image, WHITE, [(25, 0), (0, 40), (50, 40)])
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5
        self.max_health = 3
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