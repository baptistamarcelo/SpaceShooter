import pygame
import random
from pprint import pprint

pygame.init()

W = 800
H = 600

HW = W / 2
HH = H / 2

screen = pygame.display.set_mode((W, H))

image_dir = 'assets/PNG/'

ship_blue = pygame.image.load(image_dir + 'playerShip1_blue.png').convert_alpha()

meteor_brown_big = pygame.image.load(image_dir + 'Meteors/meteorBrown_big1.png').convert_alpha()
meteor_grey_big = pygame.image.load(image_dir + 'Meteors/meteorGrey_big1.png').convert_alpha()

meteor_color = meteor_brown_big

pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

black = (0, 0, 0)

vel = 5


class Ship:
    def __init__(self, surface=ship_blue, pos_x=W/2, pos_y=H/1.5, speed=vel):
        self.surface = surface
        self.ship_mask = pygame.mask.from_surface(self.surface)

        self.width, self.height = self.surface.get_size()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed

    def __new__(cls, *args, **kwargs):
        return super(Ship, cls).__new__(cls)


class Meteor:
    def __init__(self, surface=meteor_brown_big, pos_x=W/2, pos_y=-50, speed=vel/2):
        self.surface = surface
        self.meteor_mask = pygame.mask.from_surface(self.surface)

        self.width, self.height = self.surface.get_size()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed

    def __new__(cls, *args, **kwargs):
        return super(Meteor, cls).__new__(cls)


FPS = 120

game_exit = False

ship = Ship()

meteors = []

meteor_spawn_chance = 80

while not game_exit:
    pygame.time.delay(15)

    screen.fill(black)

    for event in pygame.event.get():
        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
            game_exit = True

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and ship.pos_x > ship.speed:
        ship.pos_x -= ship.speed
    if keys[pygame.K_RIGHT] and ship.pos_x < W - ship.width - ship.speed:
        ship.pos_x += ship.speed
    if keys[pygame.K_UP] and ship.pos_y > ship.speed:
        ship.pos_y -= ship.speed
    if keys[pygame.K_DOWN] and ship.pos_y < H - ship.height - ship.speed:
        ship.pos_y += ship.speed

    if random.randint(1, meteor_spawn_chance) == 1:
        meteor = Meteor(pos_x=random.randint(30, W - 30))
        meteors.append(meteor)
        # pprint(vars(meteor))

    for meteor in meteors:
        offset = (int(meteor.pos_x) - int(ship.pos_x), int(meteor.pos_y) - int(ship.pos_y))
        collision_result = meteor.meteor_mask.overlap(ship.ship_mask, offset)
        if collision_result:
            meteor.surface = meteor_grey_big

        meteor.pos_y += meteor.speed
        screen.blit(meteor.surface, (meteor.pos_x, meteor.pos_y))
        if meteor.pos_y > H + meteor.height:
            meteors.remove(meteor)

    screen.blit(ship.surface, (ship.pos_x, ship.pos_y))
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
quit()
