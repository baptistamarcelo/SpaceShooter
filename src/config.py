import pygame

pygame.init()

png_dir = 'assets/PNG/'
bg_dir = 'assets/Backgrounds/'
snd_dir = 'assets/Sound/'


def load_image(file_name):
    return pygame.image.load(file_name).convert_alpha()


def load_enemies(color):
    enemy_list = []
    for number in range(1, 6):
        value = "Enemies/enemy{}{}.png".format(color, number)
        surface = load_image(png_dir + value)
        enemy_list.append(surface)
    return enemy_list


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

bg_space = pygame.image.load('assets/Backgrounds/space.png').convert()

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
laser_red = load_image(png_dir + 'Lasers/laserRed07.png')
laser_red_impact = load_image(png_dir + 'Lasers/laserRed08.png')

tiny_grey_meteors = [meteor_tiny_1, meteor_tiny_2, meteor_tiny_3]
brown_meteors = [meteor_brown_big_1, meteor_brown_big_2, meteor_brown_big_3, meteor_brown_big_4, meteor_brown_med_1,
                 meteor_brown_med_3, meteor_brown_small_1, meteor_brown_small_2]
enemy_ships = {"easy": load_enemies("Green"), "normal": load_enemies("Red"), "hard": load_enemies("Black")}

# sounds

music_1 = pygame.mixer.music.load(snd_dir + 'music/Battle in the Stars.ogg')
music_2 = pygame.mixer.music.load(snd_dir + 'music/Alone Against Enemy.ogg')

player_laser_sound = pygame.mixer.Sound(snd_dir + 'sfx_laser2.ogg')
enemy_laser_sound = pygame.mixer.Sound(snd_dir + 'sfx_laser1.ogg')
impact_1 = pygame.mixer.Sound(snd_dir + 'impact_1.ogg')
impact_2 = pygame.mixer.Sound(snd_dir + 'impact_2.ogg')

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
max_enemies_on_screen = 8
FPS = 60
meteor_spawn_chance = 30  # the lower the number, the higher the chance, 1 = 100%
enemy_spawn_chance = 100  # the lower the number, the higher the chance, 1 = 100%
