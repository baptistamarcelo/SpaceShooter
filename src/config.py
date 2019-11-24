import pygame

pygame.init()

png_dir = 'assets/PNG/'
bg_dir = 'assets/Backgrounds/'


def load_image(file_name):
    return pygame.image.load(file_name).convert_alpha()


# screen configs
display_info = pygame.display.Info()
W = int(display_info.current_w * 0.75)
H = int(display_info.current_h * 0.75)
HW = W / 2
HH = H / 2
screen = pygame.display.set_mode((W, H))

# assets
ship_blue = load_image(png_dir + 'playerShip1_blue.png')
ship_orange = load_image(png_dir + 'playerShip1_orange.png')
enemy_black_1 = load_image(png_dir + 'Enemies/enemyBlack1.png')
enemy_black_2 = load_image(png_dir + 'Enemies/enemyBlack2.png')
enemy_red_1 = load_image(png_dir + 'Enemies/enemyRed1.png')
enemy_red_2 = load_image(png_dir + 'Enemies/enemyRed2.png')
bg_black = load_image('assets/Backgrounds/black.png')
bg_blue = load_image('assets/Backgrounds/blue.png')
bg_purple = load_image('assets/Backgrounds/purple.png')
meteor_brown_big_1 = load_image(png_dir + 'Meteors/meteorBrown_big1.png')
meteor_brown_big_2 = load_image(png_dir + 'Meteors/meteorBrown_big2.png')
meteor_brown_big_3 = load_image(png_dir + 'Meteors/meteorBrown_big3.png')
meteor_brown_big_4 = load_image(png_dir + 'Meteors/meteorBrown_big4.png')
meteor_brown_med_1 = load_image(png_dir + 'Meteors/meteorBrown_med1.png')
meteor_brown_med_3 = load_image(png_dir + 'Meteors/meteorBrown_med3.png')
meteor_brown_small_1 = load_image(png_dir + 'Meteors/meteorBrown_small1.png')
meteor_brown_small_2 = load_image(png_dir + 'Meteors/meteorBrown_small2.png')

meteor_tiny_1 = load_image(png_dir + 'Meteors/meteorGrey_small1.png')
meteor_tiny_2 = load_image(png_dir + 'Meteors/meteorGrey_small2.png')
meteor_tiny_3 = load_image(png_dir + 'Meteors/meteorGrey_tiny1.png')
laser_blue = load_image(png_dir + 'Lasers/laserBlue07.png')
laser_blue_impact = load_image(png_dir + 'Lasers/laserBlue08.png')

tiny_grey_meteors = [meteor_tiny_1, meteor_tiny_2, meteor_tiny_3]
brown_meteors = [meteor_brown_big_1, meteor_brown_big_2, meteor_brown_big_3, meteor_brown_big_4, meteor_brown_med_1,
                 meteor_brown_med_3, meteor_brown_small_1, meteor_brown_small_2]
enemy_ships = [enemy_black_1, enemy_black_2, enemy_red_1, enemy_red_2]

# game variables
bg_pos_y_1 = 0
bg_speed = W * 0.003
clock = pygame.time.Clock()
color_black = (0, 0, 0)
color_white = (255, 255, 255)
default_move_speed = W * 0.006
meteors = []
lasers = []
enemies = []
laser_cooldown = False
player_invulnerability_cooldown_max = 80
max_enemies_on_screen = 5
FPS = 60
meteor_spawn_chance = 50  # the lower the number, the higher the chance, 1 = 100%
enemy_spawn_chance = 100  # the lower the number, the higher the chance, 1 = 100%
