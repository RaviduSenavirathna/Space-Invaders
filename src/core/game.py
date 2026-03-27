import os
import pygame
import random
import sys

from .state import GameState

from ..utils.constants import *
from ..utils.config import get_config

from ..entities.player import Player
from ..entities.alien import Alien
from ..entities.bullet import Bullet
from ..entities.alien_bullet import AlienBullet

from ..effects.explosion import Explosion

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.state = GameState.MENU

        # Load config for runtime behavior
        self.config = get_config()

        # Convert string key names from config into pygame constants
        self.control_keys = {}
        for action, key_name in self.config.get('controls', {}).items():
            self.control_keys[action] = getattr(pygame, key_name, None)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Invaders RM")
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
        
        # Load and play background music, using user config volume
        try:
            music_path = os.path.join(SOUND_DIR, BACKGROUND_MUSIC)
            pygame.mixer.music.load(music_path)
            volume_pct = self.config.get('music_volume')
            volume = max(0, min(100, volume_pct)) / 100.0
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Could not load background music: {e}")
        
        # Load and scale background
        bg_path = os.path.join(IMG_BG_DIR, 'bg0.png')
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
        self.explosions = pygame.sprite.Group()
        
        # Initialize game state variables
        self.score = 0
        self.state = GameState.MENU
        self.alien_direction = 1  # 1 for right, -1 for left
        self.shoot_timer = 0
        self.paused = False  # Add pause state variable
        
        # Load or create pause text
        try:
            self.pause_text = self.font.render("PAUSED", True, WHITE)
            self.pause_hint = self.font.render("Press ESC to Resume", True, WHITE)
        except AttributeError:
            # Fallback if font isn't loaded
            self.pause_text = pygame.font.Font(None, 74).render("PAUSED", True, WHITE)
            self.pause_hint = pygame.font.Font(None, 36).render("Press ESC to Resume", True, WHITE)

        # Create player and initial aliens
        self.player = Player()
        self.player.control_keys = self.control_keys
        self.all_sprites.add(self.player)
        self.create_aliens()

        # Load health bar images
        self.health_bars = []
        try:
            for hb_file in HEALTH_BAR_IMAGES:
                img = pygame.image.load(os.path.join(IMG_UTIL_DIR, hb_file)).convert_alpha()
                # Scale the health bar image if needed
                img = pygame.transform.scale(img, (140, 20))  # Adjust size as needed
                self.health_bars.append(img)
        except Exception as e:
            print(f"Error loading health bar images: {e}")
            self.health_bars = None

        # Load score icon
        try:
            self.score_icon = pygame.image.load(os.path.join(IMG_UTIL_DIR, 'star.png')).convert_alpha()
            self.score_icon = pygame.transform.scale(self.score_icon, SCORE_ICON_SIZE)
        except pygame.error as e:
            print(f"Error loading score icon: {e}")
            self.score_icon = None






    def create_aliens(self):
        # Initial spawn of a few aliens
        for _ in range(3):  # Start with 3 aliens
            self.spawn_alien()





    def spawn_alien(self):
        # Randomly position alien at the top of the screen
        x = random.randint(50, WIDTH - 50)  # Random x position
        alien = Alien(x, -50)  # Start above the screen
        alien.speed = random.uniform(0.2, 1)  
        self.all_sprites.add(alien)
        self.aliens.add(alien)




    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            running = self.handle_events()
            if self.state == GameState.PLAYING:
                self.update()
            self.draw()
        
        pygame.quit()
        sys.exit()




    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:

                # ===== MENU =====
                if self.state == GameState.MENU:
                    if event.key == pygame.K_RETURN:
                        self.start_game()

                # ===== PLAYING =====
                elif self.state == GameState.PLAYING:
                    if event.key == self.control_keys.get('pause'):
                        self.state = GameState.PAUSED
                        pygame.mixer.music.pause()

                    elif event.key == self.control_keys.get('shoot'):
                        self.player.shoot(self.all_sprites, self.bullets)

                # ===== PAUSED =====
                elif self.state == GameState.PAUSED:
                    if event.key == self.control_keys.get('pause'):
                        self.state = GameState.PLAYING
                        pygame.mixer.music.unpause()

                # ===== GAME OVER =====
                elif self.state == GameState.GAME_OVER:
                    if event.key == self.control_keys.get('restart'):
                        self.reset_game()
        return True




    def update(self):
        self.all_sprites.update()
        self.handle_alien_movement()
        self.handle_alien_shooting()
        self.check_collisions()
        self.explosions.update()




    def handle_alien_movement(self):
        # Spawn new aliens periodically
        if random.random() < 0.02:  # 2% chance each frame to spawn a new alien
            self.spawn_alien()
        
        # Check if any alien reached the bottom
        for alien in self.aliens:
            if alien.rect.top >= HEIGHT:
                alien.kill()
                self.player.take_damage()
                if self.player.health <= 0:
                    self.state = GameState.GAME_OVER

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
                alien.speed_x = self.alien_direction * 2  # Update horizontal speed with new direction

        # Check if aliens reached player level
        for alien in self.aliens:
            if alien.rect.bottom >= self.player.rect.top:
                self.state = GameState.GAME_OVER





    def handle_alien_shooting(self):
        self.shoot_timer += 0.2
        if self.shoot_timer > 10 and len(self.aliens) > 0:
            self.shoot_timer = 0
            
            # Create a dictionary to track the frontmost alien in each column
            frontline_aliens = {}
            
            # Find the frontmost alien in each column that is visible on screen
            for alien in self.aliens:
                # Only consider aliens that have entered the screen
                if alien.rect.top > 0:
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
            hits = pygame.sprite.spritecollide(bullet, self.aliens, True)
            for alien in hits:
                explosion = Explosion(alien.rect.centerx, alien.rect.centery)
                self.all_sprites.add(explosion)
                self.explosions.add(explosion)
                bullet.kill()
                self.score += 10

        # Check alien bullet-player collision
        if pygame.sprite.spritecollide(self.player, self.alien_bullets, True):
            if self.player.take_damage():  # Will return True if health reaches 0
                self.state = GameState.GAME_OVER
            # Flash the player or show hit animation here if desired

        # Check if all aliens destroyed
        if len(self.aliens) == 0:
            self.create_aliens()
            self.alien_direction = 1
            self.player.heal()  # Heal player after clearing a wave

        # End game when alien hit player
        for alien in self.aliens:
            if pygame.sprite.collide_rect(alien, self.player):
                self.state = GameState.GAME_OVER

        # Use explosion on player hit
        if self.state == GameState.GAME_OVER:
            explosion = Explosion(self.player.rect.centerx, self.player.rect.centery)
            self.all_sprites.add(explosion)
            self.explosions.add(explosion)
            self.player.kill()





    def draw(self):

        if self.state == GameState.MENU:
            self.draw_menu()

        elif self.state == GameState.PLAYING:
            self.draw_game()

        elif self.state == GameState.PAUSED:
            self.draw_game()
            self.draw_pause_overlay()

        elif self.state == GameState.GAME_OVER:
            self.draw_game()
            self.draw_game_over()

        pygame.display.flip()



    def start_game(self):
        self.reset_game()
        self.state = GameState.PLAYING

    def draw_menu(self):
        self.screen.fill((0, 0, 0))

        title = self.font.render("SPACE INVADERS", True, (255, 255, 255))
        start = self.font.render("Press ENTER to Start", True, (255, 255, 255))

        self.screen.blit(title, title.get_rect(center=(WIDTH//2, HEIGHT//2 - 50)))
        self.screen.blit(start, start.get_rect(center=(WIDTH//2, HEIGHT//2 + 20)))

    def draw_pause_overlay(self):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))

        text = self.font.render("PAUSED", True, (255, 255, 255))
        self.screen.blit(overlay, (0, 0))
        self.screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))


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
        # Pause music when game over screen appears
        pygame.mixer.music.pause()
        
        game_over_text = self.font.render("GAME OVER", True, WHITE)
        restart_text = self.font.render("Press R to Restart", True, WHITE)
        score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
        
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 10))
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(restart_text, restart_rect)
        self.screen.blit(score_text, score_rect)




    def draw_game(self):
        # Draw background
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(BLACK)
        
        # Draw all sprites
        self.all_sprites.draw(self.screen)
        
        # Draw score and health
        self.draw_score()




    def reset_game(self):
        self.state = GameState.MENU
        self.score = 0
        self.all_sprites.empty()
        self.aliens.empty()
        self.bullets.empty()
        self.alien_bullets.empty()
        self.player = Player()
        self.player.control_keys = self.control_keys
        self.all_sprites.add(self.player)
        self.create_aliens()
        self.alien_direction = 1
        # Resume music when game restarts
        pygame.mixer.music.play(-1)