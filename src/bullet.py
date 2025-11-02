import pygame
import math

BULLET_SPEED = 400  # pixels per second

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        self.image = pygame.Surface((3, 3))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=pos)

        rad = math.radians(angle)
        self.velx = math.cos(rad) * BULLET_SPEED
        self.vely = -math.sin(rad) * BULLET_SPEED

        self.x, self.y = pos

    def update(self, tiles, dt, *args):
        self.x += self.velx * dt
        self.y += self.vely * dt
        self.rect.center = (int(self.x), int(self.y))
