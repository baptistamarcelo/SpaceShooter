import pygame

from src.exception import InvalidGameStateMatchException
from src.exception.InvalidGameStateMatchException import InvalidGameStateMatchException

pygame.init()

png_dir = 'assets/PNG/'
bg_dir = 'assets/Backgrounds/'
snd_dir = 'assets/Sound/'

# screen configs
display_info = pygame.display.Info()
screen_width = int(display_info.current_w * 0.75)
usable_screen_width = screen_width  # at the moment there is no use case to separate a portion of width
screen_height = int(display_info.current_h * 0.75)
usable_screen_height = int(screen_height * 0.9)  # separates portion of screen for the ui
screen = pygame.display.set_mode((screen_width, screen_height))


def play_music(file_path):
    pygame.mixer.music.load(f"{snd_dir}music/{file_path}")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)


def load_image(file_name):
    return pygame.image.load(file_name).convert_alpha()


def load_enemies(color):
    enemy_list = []
    for number in range(1, 6):
        value = "Enemies/enemy{}{}.png".format(color, number)
        surface = load_image(png_dir + value)
        enemy_list.append(surface)
    return enemy_list


def load_numbers():
    _numbers = {}
    for number in range(10):
        _numbers[str(number)] = load_image(png_dir + 'UI/numeral{}.png'.format(number))

    return _numbers


boss_assets = {
    "easy": {
        "ship": load_image(png_dir + "ufoGreen.png"),
        "music": "Epic End.ogg"
    },
    "normal": {
        "ship": load_image(png_dir + "ufoRed.png"),
        "music": "SkyFire (Title Screen).ogg"
    },
    "hard": {
        "ship": load_image(png_dir + "ufoBlack.png"),
        "music": "DeathMatch (Boss Theme).ogg"
    }
}

boss_damaged = load_image(png_dir + "ufoYellow.png")


def load_boss():
    try:
        game_state.boss_difficulty = next(game_state.bosses)
    except StopIteration:
        game_state.bosses = iter(boss_assets.keys())
        load_boss()


class GameState:
    def __init__(self):
        self.default_speed = 10  # the lower the number, the slowest the game will be
        self.match = "new"
        self.meteors = []
        self.lasers = []
        self.enemies = []
        self.items = []
        self.bosses = iter(boss_assets.keys())
        self.boss_difficulty = None
        self.score_to_spawn_boss = 5000
        self.boss_counter_score = 0
        self.meteor_spawn_chance = 200
        self.enemy_spawn_chance = 50
        self.item_spawn_chance = 1
        self.max_enemies_on_screen = 25

    def restart(self):
        self = self.__init__()

    def set_match_state(self, new_match_state):
        self.match = new_match_state
        if self.match in ["new", "restart"]:
            play_music('Space Heroes.ogg')
        elif self.match == "boss":
            load_boss()
            play_music(boss_assets[self.boss_difficulty]["music"])
            game_state.boss_counter_score = 0
        elif self.match == "running":  # apply original settings to the match
            play_music('Alone Against Enemy.ogg')
            self.boss_counter_score = 0
            self.enemy_spawn_chance = 25
            self.meteor_spawn_chance = 200
        elif self.match == "end":
            play_music('Victory Tune.ogg')
        elif self.match == "quit":
            pass
        else:
            raise InvalidGameStateMatchException(new_match_state)

    def clear(self):
        self.enemies.clear()
        self.lasers.clear()


game_state = GameState()

# assets
ship_blue = load_image(png_dir + 'playerShip1_blue.png')
ship_orange = load_image(png_dir + 'playerShip1_orange.png')
life_blue = load_image(png_dir + 'UI/playerLife1_blue.png')
shield_1 = load_image(png_dir + 'Effects/shield1.png')

bg_space = pygame.image.load('assets/Backgrounds/space.png').convert()

meteor_brown_big_1 = load_image(png_dir + 'Meteors/meteorBrown_big1.png')
meteor_brown_big_2 = load_image(png_dir + 'Meteors/meteorBrown_big2.png')
meteor_brown_big_3 = load_image(png_dir + 'Meteors/meteorBrown_big3.png')
meteor_brown_big_4 = load_image(png_dir + 'Meteors/meteorBrown_big4.png')
meteor_brown_med_1 = load_image(png_dir + 'Meteors/meteorBrown_med1.png')
meteor_brown_med_3 = load_image(png_dir + 'Meteors/meteorBrown_med3.png')
# meteor_brown_small_1 = load_image(png_dir + 'Meteors/meteorBrown_small1.png')
# meteor_brown_small_2 = load_image(png_dir + 'Meteors/meteorBrown_small2.png')

# meteor_tiny_1 = load_image(png_dir + 'Meteors/meteorGrey_small1.png')
# meteor_tiny_2 = load_image(png_dir + 'Meteors/meteorGrey_small2.png')
# meteor_tiny_3 = load_image(png_dir + 'Meteors/meteorGrey_tiny1.png')
laser_blue = load_image(png_dir + 'Lasers/laserBlue07.png')
laser_blue_impact = load_image(png_dir + 'Lasers/laserBlue08.png')
laser_red = load_image(png_dir + 'Lasers/laserRed07.png')
laser_red_impact = load_image(png_dir + 'Lasers/laserRed08.png')

item_power_up = load_image(png_dir + 'Power-ups/powerupBlue_bolt.png')
item_shield = load_image(png_dir + 'Power-ups/powerupGreen_shield.png')
# item_invulnerable = load_image(png_dir + 'Power-ups/powerupYellow_star.png') - maybe implement later, not sure yet

# tiny_grey_meteors = [meteor_tiny_1, meteor_tiny_2, meteor_tiny_3]
brown_meteors = [meteor_brown_big_1, meteor_brown_big_2, meteor_brown_big_3, meteor_brown_big_4, meteor_brown_med_1,
                 meteor_brown_med_3]
enemy_assets = {"easy": load_enemies("Green"), "normal": load_enemies("Red"), "hard": load_enemies("Black")}
available_items = [{"power_up": item_power_up}, {"shield": item_shield}]

number_sprites = load_numbers()

# sounds
player_laser_sound = pygame.mixer.Sound(snd_dir + 'sfx_laser2.ogg')
enemy_laser_sound = pygame.mixer.Sound(snd_dir + 'sfx_laser1.ogg')
impact_1 = pygame.mixer.Sound(snd_dir + 'impact_1.ogg')
impact_2 = pygame.mixer.Sound(snd_dir + 'impact_2.ogg')

power_up_sound = pygame.mixer.Sound(snd_dir + 'sfx_twoTone.ogg')
shield_up_sound = pygame.mixer.Sound(snd_dir + 'sfx_shieldUp.ogg')

# game variables
bg_pos_y_1 = 0
clock = pygame.time.Clock()
color_black = (0, 0, 0)
color_white = (255, 255, 255)
FPS = 60
font = pygame.font.SysFont(None, 30)
