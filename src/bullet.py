import pygame
import math

from src.physicsobject import PhysicsObject, GRAVITY, FRICTION

BULLET_SPEED = 2000
PLAYER_HIT_STRENGTH = 25
BULLET_LIFETIME = 1

class Bullet(PhysicsObject):
    def __init__(self, pos, angle):
        super().__init__({})
        self.angle = angle
        self.image = pygame.Surface((3, 3))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=pos)
        self.lifetime = BULLET_LIFETIME

        self.x, self.y = pos

    def update(self, tiles, dt):
        rad = math.radians(self.angle)
        self.velx = math.cos(rad) * BULLET_SPEED * dt
        self.vely = -math.sin(rad) * BULLET_SPEED * dt

        self.update_pos(tiles, dt)

    def tile_collision(self, tiles):
        self.kill()

    def update_timers(self, dt):
        self.lifetime -= dt
        if self.lifetime < 0:
            self.kill()

    def sprite_collision(self, sprite):
        if type(sprite).__name__ == "Player": #checking if it hit a player
            rad = math.radians(self.angle)
            sprite.velx += math.cos(rad) * PLAYER_HIT_STRENGTH
            sprite.vely -= math.sin(rad) * PLAYER_HIT_STRENGTH / 1.5 + 2

            sprite.on_ground = False

        self.kill()
