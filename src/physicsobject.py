import pygame

from src.spriteobject import Sprite

GRAVITY = 0.5
FRICTION = 1.2
AIR_RESISTANCE = 0.8

MAXX_VELO = 20
MAXY_VELO = 20


class PhysicsObject(Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x, self.y = (0, 0) #should be set elsewhere
        self.velx = 0
        self.vely = 0

        self.on_ground = False

        self.maxx_velo = MAXX_VELO
        self.maxy_velo = MAXY_VELO

    def touching_ground(self, rect2): #when on the ground, technically the rectangles are not colliding (they're touching)
        #a custom function is needed
        rect1 = self.rect
        return rect1.right > rect2.left and rect1.left < rect2.right and rect1.bottom >= rect2.top and rect1.top < rect2.bottom

    def tile_collision(self, tile): #exists to be overwrriten
        pass

    def sprite_collision(self, tile): #same here
        pass

    def update_timers(self, dt):
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

                self.tile_collision(tile)

        #then vertical acceleration
        self.vely += GRAVITY

        self.y += int(self.vely)
        self.rect.y = self.y

        self.on_ground = False

        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.vely <= 0:  # jumping
                    self.rect.top = tile.rect.bottom
                    self.vely = 0

                self.tile_collision(tile)

            if self.touching_ground(tile.rect):
                if self.vely >= 0:  # falling
                    self.rect.bottom = tile.rect.top + 0.1
                    self.vely = 0
                    self.on_ground = True

                self.tile_collision(tile)

            self.y = self.rect.y

        if self.on_ground:
            dv = FRICTION
        else:
            dv = AIR_RESISTANCE

        if self.velx > 0:
            self.velx -= dv
            if self.velx < 0:
                self.velx = 0
        elif self.velx < 0:
            self.velx += dv
            if self.velx > 0:
                self.velx = 0

        # Clamp horizontal velocity
        if self.velx > self.maxx_velo:
            self.velx = self.maxx_velo
        elif self.velx < -self.maxx_velo:
            self.velx = -self.maxx_velo

        if self.groups(): #checking for if the sprite is in any groups because apparently itll still update after its killed :(((
            for sprite in self.groups()[0]:
                if sprite != self and self.rect.colliderect(sprite.rect):
                    self.sprite_collision(sprite)

        self.update_timers(dt)
