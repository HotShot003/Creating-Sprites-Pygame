import pygame
import sys
import random 

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()
        self.gunshot = pygame.mixer.Sound('shot-and-reload-6158.mp3')
        self.hit_sound = pygame.mixer.Sound('duck-quack-112941.mp3')
    
    def shoot(self):
        self.gunshot.play()
        hits = pygame.sprite.spritecollide(self, target_group, True)
        for hit in hits:
            if isinstance(hit, Target) and hit.picture_path == "icon_duck.png":
                self.hit_sound.play()
    
    def update(self):
        # Get mouse position
        self.rect.center = pygame.mouse.get_pos()

class Target(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()    
        self.rect.center = [pos_x, pos_y]
        self.picture_path = picture_path  # Store the picture path of the target

pygame.init()
clock = pygame.time.Clock()

# Set screen dimensions to match the monitor's resolution
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h

# Create a fullscreen display
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

# Load and scale background image to match screen size
background = pygame.image.load("bg_blue.png")
background = pygame.transform.scale(background, (screen_width, screen_height))
pygame.mouse.set_visible(0)

# Create crosshair sprite
crosshair = Crosshair("crosshair_white_small.png")

# Sprite groups
crosshair_group = pygame.sprite.Group()
crosshair_group.add(crosshair)

target_group = pygame.sprite.Group()
for _ in range(10):
    # Randomly select between "icon_target.png" and "icon_duck.png" for targets
    target_image = random.choice(["icon_target.png", "icon_duck.png"])
    new_target = Target(target_image, random.randrange(0, screen_width - 10), random.randrange(0, screen_height))
    target_group.add(new_target)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            crosshair.shoot()
    
    # Draw the background image
    screen.blit(background, (0, 0))
    
    # Draw and update sprites
    target_group.draw(screen)
    crosshair_group.draw(screen)
    crosshair_group.update()
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()


