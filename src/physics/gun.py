import pygame
import math

from src.physics.bullet import Bullet
from src.renderer.spriteobject import Sprite

class Gun(Sprite):
    def __init__(self, level, player):
        super().__init__(level)
        self.player = player

        self.original_image = pygame.Surface((60, 12), pygame.SRCALPHA)
        self.original_image.fill((255, 0, 0))
        self.image = self.original_image
        self.rect = self.image.get_rect()

        self.angle = 0

    def update(self, *args):
        angle = self.player.aim_angle

        rotated_image = pygame.transform.rotate(self.original_image, angle)
        rotated_rect = rotated_image.get_rect()

        pivot_offset = pygame.math.Vector2(15, 3)
        pivot_offset.rotate_ip(-angle)

        rotated_rect.centerx = self.player.rect.centerx + pivot_offset.x
        rotated_rect.centery = self.player.rect.centery + pivot_offset.y

        self.image = rotated_image
        self.rect = rotated_rect

    def get_tip_position(self):
        angle = self.player.aim_angle
        rad = math.radians(angle)
        tip_x = self.rect.centerx + math.cos(rad) * (60 / 2)
        tip_y = self.rect.centery - math.sin(rad) * (60 / 2)
        return (tip_x, tip_y)

    def shoot(self):
        start_pos = self.get_tip_position()
        bullet = Bullet(self.level, start_pos, self.player.aim_angle)
        self.player.groups()[0].add(bullet) #adding it to the main sprites list
