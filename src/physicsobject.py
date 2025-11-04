import pygame

from src.spriteobject import Sprite

GRAVITY = 0.5
FRICTION = 0.8

class PhysicsObject(Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x, self.y = (0, 0) #should be set elsewhere
        self.velx = 0
        self.vely = 0

    def on_collision(self, tile): #exists to be overwrriten
        pass

    def update_pos(self, tiles, dt):
        #dealing with horizontal movement first
        self.x += self.velx
        self.rect.x = int(self.x)

        #checking for tile collision
        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.velx > 0:  # moving right
                    self.rect.right = tile.rect.left
                elif self.velx < 0:  # moving left
                    self.rect.left = tile.rect.right
                self.velx = 0
                self.x = self.rect.x

                self.on_collision(tile)

        #then vertical acceleration
        self.vely += GRAVITY
        self.y += self.vely
        self.rect.y = int(self.y)
        self.on_ground = False

        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.vely > 0:  # falling
                    self.rect.bottom = tile.rect.top
                    self.vely = 0
                    self.on_ground = True
                elif self.vely < 0:  # jumping
                    self.rect.top = tile.rect.bottom
                    self.vely = 0
                self.y = self.rect.y

                self.on_collision(tile)

        for sprite in self.groups()[0]:
            pass
