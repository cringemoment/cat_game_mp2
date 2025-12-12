import pygame
import random
import math

from src.physics.physicsobject import PhysicsObject

MAXPARTX_VELO = 3
MAXPARTY_VELO = 3
PART_LIFETIME = 0.1
MIN_LIFETIME = 0.05

class OneParticle(PhysicsObject):
    def __init__(self, level, image, x, y, xdir = None, ydir = None):
        super().__init__(level)

        self.collision = False
        self.x = x
        self.y = y

        if xdir:
            self.xdir = math.copysign(1, xdir)
        else:
            self.xdir = random.choice([-1, 1])

        if ydir:
            self.ydir = math.copysign(1, ydir)
        else:
            self.ydir = random.choice([-1, 1])

        self.velx = random.randint(1, MAXPARTX_VELO) * self.xdir
        self.vely = random.randint(1, MAXPARTY_VELO) * self.ydir


        self.gravity = 0
        self.air_resistance = 0
        self.time = PART_LIFETIME

        self.set_loaded_sprites({"default": image})
        self.change_image("default")

    def update_timers(self, dt):
        self.time -= dt
        if self.time <= 0:
            self.kill()

    def tile_collision(self, sprite):
        if PART_LIFETIME - self.time > MIN_LIFETIME:
            self.kill()

    def sprite_collision(self, sprite):
        if not type(sprite).__name__ == "OneParticle" and PART_LIFETIME - self.time > MIN_LIFETIME:
            self.kill()

class ParticleEffect(pygame.sprite.Group):
    def __init__(self, images, count):
        super().__init__()

        self.particle_count = count
        self.images = images

    def spawn_effect(self, level, x, y, xdir = None, ydir = None):
        for _ in range(self.particle_count):
            level.tiles.physics_objects.add(OneParticle(level, random.choice(self.images), x, y, xdir, ydir))

def break_tile(image, tile_size = 4):
    width, height = image.get_size()

    tiles = []

    for y in range(0, height, tile_size):
        for x in range(0, width, tile_size):
            rect = pygame.Rect(x, y, tile_size, tile_size)
            tile = image.subsurface(rect).copy()
            tiles.append(tile)

    return tiles

test = pygame.image.load("assets/objects/box.png")
testpart = ParticleEffect(break_tile(test), 20)
