import pygame
import random

pygame.init()

W = 800
H = 600

HW = W / 2
HH = H / 2

screen = pygame.display.set_mode((W, H))

image_dir = 'assets/PNG/'

ship_blue = pygame.image.load(image_dir + 'playerShip1_blue.png').convert_alpha()

bg_black = pygame.image.load('assets/Backgrounds/black.png').convert_alpha()
bg_blue = pygame.image.load('assets/Backgrounds/blue.png').convert_alpha()
bg_purple = pygame.image.load('assets/Backgrounds/purple.png').convert_alpha()

meteor_brown_big = pygame.image.load(image_dir + 'Meteors/meteorBrown_big1.png').convert_alpha()
meteor_grey_big = pygame.image.load(image_dir + 'Meteors/meteorGrey_big1.png').convert_alpha()
laser_blue = pygame.image.load(image_dir + 'Lasers/laserBlue07.png').convert_alpha()
laser_blue_impact = pygame.image.load(image_dir + 'Lasers/laserBlue08.png').convert_alpha()

pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

black = (0, 0, 0)

vel = 5

FPS = 120

game_exit = False

meteors = []
lasers = []

laser_cooldown_max = 30
laser_cooldown_count = 0
laser_cooldown = False

laser_hit = False

meteor_spawn_chance = 80


class Laser:
    def __init__(self, surface=laser_blue, pos_x=0.0, pos_y=0.0, speed=vel*2):
        self.surface = surface
        self.mask = pygame.mask.from_surface(self.surface)

        self.width, self.height = self.surface.get_size()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed

    def __new__(cls, *args, **kwargs):
        return super(Laser, cls).__new__(cls)


class Ship:
    def __init__(self, surface=ship_blue, pos_x=W/2, pos_y=H/1.5, speed=vel):
        self.surface = surface
        self.mask = pygame.mask.from_surface(self.surface)

        self.width, self.height = self.surface.get_size()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed

    def __new__(cls, *args, **kwargs):
        return super(Ship, cls).__new__(cls)


class Meteor:
    def __init__(self, surface=meteor_brown_big, pos_x=W/2, pos_y=-50, speed=vel/2):
        self.surface = surface
        self.mask = pygame.mask.from_surface(self.surface)

        self.width, self.height = self.surface.get_size()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.speed = speed

    def __new__(cls, *args, **kwargs):
        return super(Meteor, cls).__new__(cls)

    def display(self):
        self.pos_y += self.speed
        screen.blit(self.surface, (self.pos_x, self.pos_y))

        if self.pos_y > H + self.height:
            meteors.remove(meteor)


class Background:
    def __init__(self, pos_y_1, pos_y_2, speed, pos_x=0, surface=bg_black):
        self.pos_x = pos_x
        self.pos_y_1 = pos_y_1
        self.pos_y_2 = pos_y_2
        self.speed = speed
        self.surface = pygame.transform.scale(surface, (W, H))

    def display(self):
        self.pos_y_1 += self.speed
        self.pos_y_2 += self.speed

        screen.blit(self.surface, (0, self.pos_y_1))
        screen.blit(self.surface, (0, self.pos_y_2))

        if self.pos_y_1 > H:
            self.pos_y_1 = -H
        if self.pos_y_2 > H:
            self.pos_y_2 = -H


def check_collision(obj_1, obj_2):
    offset = (int(obj_1.pos_x - obj_2.pos_x), int(obj_1.pos_y - obj_2.pos_y))
    collision_result = obj_2.mask.overlap(obj_1.mask, offset)

    return collision_result


background = Background(0, -H, 4)

ship = Ship()

while not game_exit:
    pygame.time.delay(10)

    background.display()

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
    if keys[pygame.K_SPACE] and not laser_cooldown:
        laser = Laser(pos_x=ship.pos_x + (ship.width / 2), pos_y=ship.pos_y)
        laser.pos_x -= (laser.width / 2)
        lasers.append(laser)
        laser_cooldown = True

    if laser_cooldown:
        if laser_cooldown_count == laser_cooldown_max:
            laser_cooldown = False
            laser_cooldown_count = 0
        else:
            laser_cooldown_count += 1

    if random.randint(1, meteor_spawn_chance) == 1:
        meteor = Meteor(pos_x=random.randint(30, W - 30))
        meteors.append(meteor)

    for meteor in meteors:
        if check_collision(meteor, ship):
            meteor.surface = meteor_grey_big
        meteor.display()

    for laser in lasers:
        if laser.pos_y > 0:
            for meteor in meteors:
                offset = (int(laser.pos_x) - int(meteor.pos_x), int(laser.pos_y) - int(meteor.pos_y))
                collision_result = meteor.mask.overlap(laser.mask, offset)
                if collision_result:
                    old_width = laser.width
                    laser.surface = laser_blue_impact
                    l_width, l_height = laser.surface.get_size()
                    screen.blit(laser.surface, (laser.pos_x - l_width / 2 + old_width / 2, laser.pos_y - l_height / 2))
                    lasers.remove(laser)
                    meteors.remove(meteor)
                    laser_hit = True

        laser.pos_y -= laser.speed
        if laser_hit:
            laser_hit = False
        else:
            screen.blit(laser.surface, (laser.pos_x, laser.pos_y))

        if laser.pos_y < 0:
            lasers.remove(laser)

    screen.blit(ship.surface, (ship.pos_x, ship.pos_y))

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
quit()
