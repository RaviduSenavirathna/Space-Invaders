import os
import pygame
import random
import sys
from .constants import *
from .sprites.player import Player
from .sprites.alien import Alien
from .sprites.bullet import Bullet
from .sprites.alien_bullet import AlienBullet

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        
        # Load custom font with error handling
        try:
            if not os.path.exists(BYTE_BOUNCE_FONT):
                raise FileNotFoundError(f"Font file not found: {BYTE_BOUNCE_FONT}")
            self.font = pygame.font.Font(BYTE_BOUNCE_FONT, FONT_SIZE)
            print("ByteBounce font loaded successfully")
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading ByteBounce font: {e}")
            print("Falling back to default font")
            self.font = pygame.font.Font(None, FONT_SIZE)
        
        # Load and scale background
        bg_path = os.path.join(IMG_DIR, 'background.png')
        try:
            self.background = pygame.image.load(bg_path).convert()
            self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        except pygame.error:
            print(f"Could not load background image from {bg_path}")
            self.background = None
        
        # Create sprite groups for game objects
        self.all_sprites = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()
        
        # Initialize game state variables
        self.score = 0
        self.game_over = False
        self.alien_direction = 1  # 1 for right, -1 for left
        self.shoot_timer = 0
        
        # Create player and initial aliens
        self.player = Player()
        self.all_sprites.add(self.player)
        self.create_aliens()

        # Load health bar images
        self.health_bars = []
        try:
            for hb_file in HEALTH_BAR_IMAGES:
                img = pygame.image.load(os.path.join(IMG_DIR, hb_file)).convert_alpha()
                # Scale the health bar image if needed
                img = pygame.transform.scale(img, (140, 20))  # Adjust size as needed
                self.health_bars.append(img)
        except pygame.error as e:
            print(f"Error loading health bar images: {e}")
            self.health_bars = None

        # Load sound effects
        try:
            self.explosion_sound = pygame.mixer.Sound(os.path.join(SOUND_DIR, 'explosion.wav'))
            self.explosion_sound.set_volume(0.2)  # Set volume to a reasonable level
        except pygame.error as e:
            print(f"Could not load sound effects: {e}")
            self.explosion_sound = None

        # Load score icon
        try:
            self.score_icon = pygame.image.load(os.path.join(IMG_DIR, 'star.png')).convert_alpha()
            self.score_icon = pygame.transform.scale(self.score_icon, SCORE_ICON_SIZE)
        except pygame.error as e:
            print(f"Error loading score icon: {e}")
            self.score_icon = None

    def create_aliens(self):
        for row in range(5):
            for col in range(10):
                alien = Alien(col * 70 + 50, row * 50 + 50)
                self.all_sprites.add(alien)
                self.aliens.add(alien)

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            running = self.handle_events()
            if not self.game_over:
                self.update()
            self.draw()
        
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.game_over:  # Left mouse button
                    self.player.shoot(self.all_sprites, self.bullets)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()
        return True

    def update(self):
        self.all_sprites.update()
        self.handle_alien_movement()
        self.handle_alien_shooting()
        self.check_collisions()

    def handle_alien_movement(self):
        # Check if any alien hits screen edges
        alien_move_down = False
        for alien in self.aliens:
            if alien.rect.right >= WIDTH or alien.rect.left <= 0:
                self.alien_direction *= -1
                alien_move_down = True
                break

        # Move aliens down when they hit screen edges
        if alien_move_down:
            for alien in self.aliens:
                alien.rect.y += 30
                alien.speed = self.alien_direction

        # Check if aliens reached player level
        for alien in self.aliens:
            if alien.rect.bottom >= self.player.rect.top:
                self.game_over = True

    def handle_alien_shooting(self):
        self.shoot_timer += 1
        if self.shoot_timer > 30 and len(self.aliens) > 0:
            self.shoot_timer = 0
            
            # Create a dictionary to track the frontmost alien in each column
            frontline_aliens = {}
            
            # Find the frontmost alien in each column
            for alien in self.aliens:
                column = alien.rect.centerx
                if column not in frontline_aliens or alien.rect.bottom > frontline_aliens[column].rect.bottom:
                    frontline_aliens[column] = alien
            
            # Randomly select one of the frontline aliens to shoot
            if frontline_aliens:
                shooting_alien = random.choice(list(frontline_aliens.values()))
                alien_bullet = AlienBullet(
                    shooting_alien.rect.centerx, 
                    shooting_alien.rect.bottom,
                    shooting_alien.alien_type
                )
                self.all_sprites.add(alien_bullet)
                self.alien_bullets.add(alien_bullet)

    def check_collisions(self):
        # Check bullet-alien collisions
        for bullet in self.bullets:
            hit_aliens = pygame.sprite.spritecollide(bullet, self.aliens, True)
            if hit_aliens:
                bullet.kill()
                if self.explosion_sound: # Play explosion sound
                    self.explosion_sound.play() 
                self.score += 10

        # Check alien bullet-player collision
        if pygame.sprite.spritecollide(self.player, self.alien_bullets, True):
            if self.player.take_damage():  # Will return True if health reaches 0
                self.game_over = True
            # Flash the player or show hit animation here if desired

        # Check if all aliens destroyed
        if len(self.aliens) == 0:
            self.create_aliens()
            self.alien_direction = 1
            self.player.heal()  # Heal player after clearing a wave

    def draw(self):
        # Draw background
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(BLACK)
        
        # Draw sprites
        self.all_sprites.draw(self.screen)
        
        # Draw score
        self.draw_score()
        
        # Draw health bar
        self.draw_health_bar()
        
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()

    def draw_score(self):
        # Draw score icon
        if self.score_icon:
            self.screen.blit(self.score_icon, SCORE_POSITION)
        
        # Draw score text with ByteBounce font in yellow
        score_text = self.font.render(f"{self.score}", True, YELLOW)
        score_pos = (SCORE_POSITION[0] + SCORE_TEXT_OFFSET, SCORE_POSITION[1])
        self.screen.blit(score_text, score_pos)

        # Draw health bar if implemented
        if hasattr(self, 'draw_health_bar'):
            self.draw_health_bar()

    def draw_health_bar(self):
        if self.health_bars:
            # Clamp health value to valid range for array index
            health_index = max(0, min(self.player.health, len(self.health_bars) - 1))
            health_bar = self.health_bars[health_index]
            self.screen.blit(health_bar, HEALTH_BAR_POSITION)

    def draw_game_over(self):
        game_over_text = self.font.render("GAME OVER", True, RED)
        restart_text = self.font.render("Press R to Restart", True, WHITE)
        self.screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
        self.screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 20))

    def reset_game(self):
        self.game_over = False
        self.score = 0
        self.all_sprites.empty()
        self.aliens.empty()
        self.bullets.empty()
        self.alien_bullets.empty()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.create_aliens()
        self.alien_direction = 1