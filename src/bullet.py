import pygame
import math

from src.physicsobject import PhysicsObject

BULLET_SPEED = 800  # pixels per second

class Bullet(PhysicsObject):
    def __init__(self, pos, angle):
        super().__init__({})
        self.angle = angle
        self.image = pygame.Surface((3, 3))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=pos)

        self.x, self.y = pos

    def update(self, tiles, dt):
        rad = math.radians(self.angle)
        self.velx = math.cos(rad) * BULLET_SPEED * dt
        self.vely = -math.sin(rad) * BULLET_SPEED * dt

        self.update_pos(tiles, dt)

    def on_collision(self, tiles):
        self.kill()
