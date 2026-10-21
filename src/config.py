import pygame
import os
import random

from src.exception import InvalidGameStateMatchException

pygame.init()

# Asset directories
png_dir = os.path.join('assets', 'PNG')
bg_dir = os.path.join('assets', 'Backgrounds')
snd_dir = os.path.join('assets', 'Sound')

# Screen configs
display_info = pygame.display.Info()
screen_width = int(display_info.current_w * 0.75)
usable_screen_width = screen_width
screen_height = int(display_info.current_h * 0.75)
usable_screen_height = int(screen_height * 0.9)
screen = pygame.display.set_mode((screen_width, screen_height))

def play_music(file_path: str) -> None:
    pygame.mixer.music.load(os.path.join(snd_dir, 'music', file_path))
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)

def load_image(file_name: str) -> pygame.Surface:
    return pygame.image.load(file_name).convert_alpha()

def load_enemies(color: str):
    enemy_list = []
    for number in range(1, 6):
        value = f"Enemies/enemy{color}{number}.png"
        surface = load_image(os.path.join(png_dir, value))
        enemy_list.append(surface)
    return enemy_list

def load_numbers():
    _numbers = {}
    for number in range(10):
        _numbers[str(number)] = load_image(os.path.join(png_dir, f'UI/numeral{number}.png'))
    return _numbers

# Boss assets
boss_assets = {
    "easy": {
        "ship": load_image(os.path.join(png_dir, "ufoGreen.png")),
        "music": "Epic End.ogg",
    },
    "normal": {
        "ship": load_image(os.path.join(png_dir, "ufoRed.png")),
        "music": "SkyFire (Title Screen).ogg",
    },
    "hard": {
        "ship": load_image(os.path.join(png_dir, "ufoBlack.png")),
        "music": "DeathMatch (Boss Theme).ogg",
    },
}

boss_damaged = load_image(os.path.join(png_dir, "ufoYellow.png"))

def load_boss():
    try:
        game_state.boss_difficulty = next(game_state.bosses)
    except StopIteration:
        game_state.bosses = iter(boss_assets.keys())
        load_boss()

# Game state class
class GameState:
    def __init__(self):
        self.default_speed = 10
        self.match = "new"
        self.meteors = []
        self.lasers = []
        self.enemies = []
        self.bosses = iter(boss_assets.keys())
        # Items that spawn from meteors or enemies
        self.items = []
        self.boss_difficulty = None
        self.score_to_spawn_boss = 5000
        self.boss_counter_score = 0
        self.meteor_spawn_chance = 200
        self.enemy_spawn_chance = 50
        self.difficulty_level = 0
        self.particles = []
        self.item_spawn_multiplier = 1.0
        self.max_enemies_on_screen = 25

    def restart(self):
        self.__init__()

    def set_match_state(self, new_match_state: str) -> None:
        self.match = new_match_state
        if self.match in ["new", "restart"]:
            play_music("Space Heroes.ogg")
        elif self.match == "boss":
            load_boss()
            play_music(boss_assets[self.boss_difficulty]["music"])
        elif self.match == "running":
            play_music("Alone Against Enemy.ogg")
            self.boss_counter_score = 0
            self.enemy_spawn_chance = 25
            self.meteor_spawn_chance = 200
            self.adjust_difficulty()
        elif self.match == "end":
            play_music("Victory Tune.ogg")
        elif self.match == "quit":
            pass
        else:
            raise InvalidGameStateMatchException(new_match_state)

    def adjust_difficulty(self):
        thresholds = [2000, 5000, 8000, 12000]
        # Determine level based on boss counter score thresholds
        level = 0
        for th in thresholds:
            if self.boss_counter_score >= th:
                level += 1
            else:
                break
        if level != self.difficulty_level:
            self.difficulty_level = level
            # Decrease spawn chance (i.e., increase frequency)
            self.enemy_spawn_chance = max(5, 25 - level * 5)
            self.max_enemies_on_screen = 25 + level * 5
            self.item_spawn_multiplier = 1.0 + level * 0.5

game_state = GameState()

# Assets
ship_blue = load_image(os.path.join(png_dir, 'playerShip1_blue.png'))
ship_orange = load_image(os.path.join(png_dir, 'playerShip1_orange.png'))
life_blue = load_image(os.path.join(png_dir, 'UI/playerLife1_blue.png'))
shield_1 = load_image(os.path.join(png_dir, 'Effects/shield1.png'))

bg_space = pygame.image.load(os.path.join(bg_dir, 'space.png')).convert()

meteor_brown_big_1 = load_image(os.path.join(png_dir, 'Meteors/meteorBrown_big1.png'))
meteor_brown_big_2 = load_image(os.path.join(png_dir, 'Meteors/meteorBrown_big2.png'))
meteor_brown_big_3 = load_image(os.path.join(png_dir, 'Meteors/meteorBrown_big3.png'))
meteor_brown_big_4 = load_image(os.path.join(png_dir, 'Meteors/meteorBrown_big4.png'))
meteor_brown_med_1 = load_image(os.path.join(png_dir, 'Meteors/meteorBrown_med1.png'))
meteor_brown_med_3 = load_image(os.path.join(png_dir, 'Meteors/meteorBrown_med3.png'))
# meteor_brown_small_1 = load_image(os.path.join(png_dir, 'Meteors/meteorBrown_small1.png'))
# meteor_brown_small_2 = load_image(os.path.join(png_dir, 'Meteors/meteorBrown_small2.png'))
# meteor_tiny_1 = load_image(os.path.join(png_dir, 'Meteors/meteorGrey_small1.png'))
# meteor_tiny_2 = load_image(os.path.join(png_dir, 'Meteors/meteorGrey_small2.png'))
# meteor_tiny_3 = load_image(os.path.join(png_dir, 'Meteors/meteorGrey_tiny1.png'))
laser_blue = load_image(os.path.join(png_dir, 'Lasers/laserBlue07.png'))
laser_blue_impact = load_image(os.path.join(png_dir, 'Lasers/laserBlue08.png'))
laser_red = load_image(os.path.join(png_dir, 'Lasers/laserRed07.png'))
laser_red_impact = load_image(os.path.join(png_dir, 'Lasers/laserRed08.png'))

item_power_up = load_image(os.path.join(png_dir, 'Power-ups/powerupBlue_bolt.png'))
item_shield = load_image(os.path.join(png_dir, 'Power-ups/powerupGreen_shield.png'))
# item_invulnerable = load_image(os.path.join(png_dir, 'Power-ups/powerupYellow_star.png'))

brown_meteors = [
    meteor_brown_big_1,
    meteor_brown_big_2,
    meteor_brown_big_3,
    meteor_brown_big_4,
    meteor_brown_med_1,
    meteor_brown_med_3,
]
enemy_assets = {
    "easy": load_enemies("Green"),
    "normal": load_enemies("Red"),
    "hard": load_enemies("Black"),
}
available_items = [{"power_up": item_power_up}, {"shield": item_shield}]

number_sprites = load_numbers()

# Sounds
player_laser_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'sfx_laser2.ogg'))
enemy_laser_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'sfx_laser1.ogg'))
impact_1 = pygame.mixer.Sound(os.path.join(snd_dir, 'impact_1.ogg'))
impact_2 = pygame.mixer.Sound(os.path.join(snd_dir, 'impact_2.ogg'))
power_up_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'sfx_twoTone.ogg'))
shield_up_sound = pygame.mixer.Sound(os.path.join(snd_dir, 'sfx_shieldUp.ogg'))

bg_pos_y_1 = 0
clock = pygame.time.Clock()
color_black = (0, 0, 0)
color_white = (255, 255, 255)
FPS = 60
font = pygame.font.SysFont(None, 30)
