import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Player
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

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Alien
class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 1

    def update(self):
        self.rect.x += self.speed

# Bullet
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
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

# Alien Bullet
class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 15))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Create sprite groups
all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()
alien_bullets = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create aliens
def create_aliens():
    for row in range(5):
        for col in range(10):
            alien = Alien(col * 70 + 50, row * 50 + 50)
            all_sprites.add(alien)
            aliens.add(alien)

create_aliens()

# Game variables
score = 0
game_over = False
alien_direction = 1
alien_move_down = False
shoot_timer = 0

# Font
font = pygame.font.Font(None, 36)

# Game loop
running = True
while running:
    clock.tick(FPS)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player.shoot()
            if event.key == pygame.K_r and game_over:
                # Restart game
                game_over = False
                score = 0
                all_sprites.empty()
                aliens.empty()
                bullets.empty()
                alien_bullets.empty()
                player = Player()
                all_sprites.add(player)
                create_aliens()
                alien_direction = 1

    if not game_over:
        # Update
        all_sprites.update()

        # Check if aliens hit edges
        alien_move_down = False
        for alien in aliens:
            if alien.rect.right >= WIDTH or alien.rect.left <= 0:
                alien_direction *= -1
                alien_move_down = True
                break

        # Move aliens down and reverse direction
        if alien_move_down:
            for alien in aliens:
                alien.rect.y += 30
                alien.speed = alien_direction

        # Check if aliens reached bottom
        for alien in aliens:
            if alien.rect.bottom >= player.rect.top:
                game_over = True

        # Aliens shoot randomly
        shoot_timer += 1
        if shoot_timer > 30 and len(aliens) > 0:
            shoot_timer = 0
            shooting_alien = random.choice(list(aliens))
            alien_bullet = AlienBullet(shooting_alien.rect.centerx, shooting_alien.rect.bottom)
            all_sprites.add(alien_bullet)
            alien_bullets.add(alien_bullet)

        # Check bullet-alien collisions
        for bullet in bullets:
            hit_aliens = pygame.sprite.spritecollide(bullet, aliens, True)
            if hit_aliens:
                bullet.kill()
                score += 10

        # Check alien bullet-player collision
        if pygame.sprite.spritecollide(player, alien_bullets, True):
            game_over = True

        # Check if all aliens destroyed
        if len(aliens) == 0:
            create_aliens()
            alien_direction = 1

    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    # Draw game over
    if game_over:
        game_over_text = font.render("GAME OVER", True, RED)
        restart_text = font.render("Press R to Restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
        screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 20))

    pygame.display.flip()

pygame.quit()
sys.exit()