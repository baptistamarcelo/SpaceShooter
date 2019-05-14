import pygame


# screen configs
W = 800
H = 600
HW = W / 2
HH = H / 2
screen = pygame.display.set_mode((W, H))

# assets
image_dir = 'assets/PNG/'
ship_blue = pygame.image.load(image_dir + 'playerShip1_blue.png').convert_alpha()
ship_orange = pygame.image.load(image_dir + 'playerShip1_orange.png').convert_alpha()
bg_black = pygame.image.load('assets/Backgrounds/black.png').convert_alpha()
bg_blue = pygame.image.load('assets/Backgrounds/blue.png').convert_alpha()
bg_purple = pygame.image.load('assets/Backgrounds/purple.png').convert_alpha()
meteor_brown_big = pygame.image.load(image_dir + 'Meteors/meteorBrown_big1.png').convert_alpha()
meteor_tiny_1 = pygame.image.load(image_dir + 'Meteors/meteorGrey_small1.png').convert_alpha()
meteor_tiny_2 = pygame.image.load(image_dir + 'Meteors/meteorGrey_small2.png').convert_alpha()
meteor_tiny_3 = pygame.image.load(image_dir + 'Meteors/meteorGrey_tiny1.png').convert_alpha()
tiny_meteors = [meteor_tiny_1, meteor_tiny_2, meteor_tiny_3]
laser_blue = pygame.image.load(image_dir + 'Lasers/laserBlue07.png').convert_alpha()
laser_blue_impact = pygame.image.load(image_dir + 'Lasers/laserBlue08.png').convert_alpha()

# game variables
bg_pos_y_1 = 0
bg_speed = 4
clock = pygame.time.Clock()
color_black = (0, 0, 0)
color_white = (255, 255, 255)
default_move_speed = 5
meteors = []
lasers = []
laser_cooldown_max = 30
laser_cooldown_count = 0
laser_cooldown = False
player_invulnerability_cooldown_max = 80
FPS = 120
meteor_spawn_chance = 80  # the lower the number, the higher the chance, 1 = 100%
