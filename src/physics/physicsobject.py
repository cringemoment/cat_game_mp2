import pygame

from src.renderer.spriteobject import Sprite

GRAVITY = 0.5
FRICTION = 1.2
AIR_RESISTANCE = 0.8

MAXX_VELO = 20
MAXY_VELO = 12

MAX_PHYSICS_CHECKS = 10
MYSTERY_PHYSICS_CONSTANT = 0.1 #no comment needed

def minimum_push(n, x): #sometimes collision doesn't push out enough
    #easy fix!
    if x == 0:
        return 0
    return n * x/abs(x) if abs(x) < n else x

class PhysicsObject(Sprite):
    """
    object with physics
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x, self.y = (0, 0) #should be set elsewhere
        self.left = 0
        self.right = 0
        self.top = 0
        self.bottom = 0

        self.velx = 0
        self.vely = 0

        self.on_ground = False

        #movement
        self.maxx_velo = MAXX_VELO
        self.maxy_velo = MAXY_VELO
        self.friction = FRICTION
        self.air_resistance = AIR_RESISTANCE
        self.gravity = GRAVITY

        #interactions with other sprites
        self.collision = True
        self.pushback_factor = 1
        self.name = None

    def update_bounds(self):
        self.left = self.x
        self.right = self.x + self.rect.width
        self.top = self.y
        self.bottom = self.y + self.rect.height

    def colliding(self, obj):
        return self.right > obj.left and self.left < obj.right and self.bottom > obj.top and self.top < obj.bottom

    def touching_ground(self, obj): #when on the ground, technically the rectangles are not colliding (they're touching)
        #a custom function is needed
        return self.right > obj.left and self.left < obj.right and self.bottom >= obj.top and self.top < obj.bottom

    def tile_collision(self, tile): #exists to be overwrriten
        pass

    def sprite_collision(self, tile): #same here
        pass

    def update_timers(self, dt):
        pass

    def collide_x(self, obj, iteration):
        if not self.colliding(obj):
            return

        if not obj.alive() or not self.alive():
            return

        if getattr(obj, "sprite_collision", None):
            self.sprite_collision(obj)
            obj.sprite_collision(self)
        else:
            self.tile_collision(obj)

        if self.collision == False or getattr(obj, "collision", True) == False:
            return

        pushback_factor = getattr(obj, "pushback_factor", 1)

        if self.right > obj.left and self.left < obj.left: #going right
            dx = self.right - obj.left

        elif self.left < obj.right and self.right > obj.right: #going left
            dx = self.left - obj.right

        else:
            return

        self.x -= minimum_push(MYSTERY_PHYSICS_CONSTANT, dx * pushback_factor)
        obj.x += minimum_push(MYSTERY_PHYSICS_CONSTANT, dx * (1 - pushback_factor))

        # if type(self).__name__ == "Player" and hasattr(obj, "velx"):
            # obj.velx = dx * (1 - pushback_factor)

        self.update_bounds()
        if getattr(obj, "update_bounds", None):
            obj.update_bounds()

    def collide_y(self, obj, iteration):
        if not self.touching_ground(obj) or not self.colliding(obj):
            return

        if not obj.alive() or not self.alive():
            return

        if getattr(obj, "sprite_collision", None):
            self.sprite_collision(obj)
            obj.sprite_collision(self)
        else:
            self.tile_collision(obj)

        if self.collision == False or getattr(obj, "collision", True) == False:
            return

        pushback_factor = getattr(obj, "pushback_factor", 1)

        if self.bottom >= obj.top and self.top < obj.top: #going down
            dy = self.bottom - obj.top
            self.y -= dy
            self.on_ground = True
            self.vely = 0

        elif self.top < obj.bottom and self.bottom > obj.bottom: #going up
            dy = obj.bottom - self.top
            # if type(self).__name__ == "Player" and type(obj).__name__ == "Player":
            #     print(f"Pushing player up {dy * (1 - pushback_factor)}, to {obj.y - dy * (1 - pushback_factor)}")
            self.y += dy * pushback_factor
            obj.y -= dy * (1 - pushback_factor)
            self.vely = 0

        self.update_bounds()

    def handle_collisions(self, colliders):
        for i in range(MAX_PHYSICS_CHECKS):
            self.x += self.velx / MAX_PHYSICS_CHECKS
            self.update_bounds()

            for obj in colliders:
                self.collide_x(obj, i)

        self.vely += self.gravity
        self.on_ground = False

        for i in range(MAX_PHYSICS_CHECKS):
            self.y += self.vely / MAX_PHYSICS_CHECKS
            self.update_bounds()

            for obj in colliders:
                self.collide_y(obj, i)

        self.rect.x = self.x
        self.rect.y = self.y

    def update_pos(self, level, dt):
        colliders = []
        for i in self.groups():
            colliders.extend([s for s in i if s is not self and getattr(s, "collision", False)])

        colliders.extend(level.collision_tiles)

        colliders.sort(key = lambda x: abs(x.velx) if hasattr(x, "velx") else 0)

        self.handle_collisions(colliders)

        self.rect.x = int(self.x)

        if self.on_ground:
            dv = self.friction
        else:
            dv = self.air_resistance

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

        if self.vely > self.maxy_velo:
            self.vely = self.maxy_velo
        elif self.vely < -self.maxy_velo:
            self.vely = -self.maxy_velo

        self.update_timers(dt)

    def update(self, level, dt):
        self.update_pos(level.tiles, dt)
        self.update_sprites(dt)
