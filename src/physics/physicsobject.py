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

        self.collision = False

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

    def handle_collisions(self, colliders):
        self.x += self.velx
        self.rect.x = int(self.x)

        for obj in colliders:
            if self.rect.colliderect(obj.rect):
                if self.velx > 0:  # moving right
                    self.rect.right = obj.rect.left
                elif self.velx < 0:  # moving left
                    self.rect.left = obj.rect.right
                self.velx = 0
                self.x = self.rect.x

                if isinstance(obj, pygame.sprite.Sprite):
                    self.sprite_collision(obj)
                else:
                    self.tile_collision(obj)

        self.vely += GRAVITY
        self.y += self.vely
        self.rect.y = int(self.y)
        self.on_ground = False

        for obj in colliders:
            if self.rect.colliderect(obj.rect):
                if self.vely <= 0:  # jumping
                    self.rect.top = obj.rect.bottom
                    self.vely = 0
                    if isinstance(obj, pygame.sprite.Sprite):
                        self.sprite_collision(obj)
                    else:
                        self.tile_collision(obj)

                elif self.touching_ground(obj.rect):
                    if self.vely >= 0:  # falling
                        self.rect.bottom = obj.rect.top + 0.1
                        self.vely = 0
                        self.on_ground = True
                        if isinstance(obj, pygame.sprite.Sprite):
                            self.sprite_collision(obj)
                        else:
                            self.tile_collision(obj)

            self.y = self.rect.y

    def update_pos(self, level, dt):
        colliders = []
        for i in self.groups():
            colliders.extend([s for s in i if s is not self and getattr(s, "collision", False)])

        colliders.extend(level.collision_tiles)

        self.handle_collisions(colliders)

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

        self.update_timers(dt)

    def update(self, level, dt):
        self.update_pos(level, dt)
