import pygame

from src.renderer.spriteobject import Sprite

GRAVITY = 0.7
FRICTION = 1.2
AIR_RESISTANCE = 0.8

MAXX_VELO = 20
MAXY_VELO = 12

MAX_PHYSICS_CHECKS = 4
MYSTERY_PHYSICS_CONSTANT = 0.1 #no comment needed
SEARCH_RADIUS = 2 * 32 #32 is tile size, 8 is how many tiles is checked on the left/right sid

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
        self.trigger_interactible = False
        self.player_only = False

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
        if self.collision == False or getattr(obj, "collision", True) == False:
            return

        if not obj.alive() or not self.alive():
            return

        if self.player_only and type(obj).__name__ != "Player":
            return

        if not self.colliding(obj):
            return

        if getattr(obj, "sprite_collision", None):
            self.sprite_collision(obj)
            obj.sprite_collision(self)
        else:
            self.tile_collision(obj)

        pushback_factor = getattr(obj, "pushback_factor", 1)

        if self.right > obj.left and self.left < obj.left: #going right
            dx = self.right - obj.left

        elif self.left < obj.right and self.right > obj.right: #going left
            dx = self.left - obj.right

        else:
            return

        if self.pushback_factor != 1:
            self.x -= minimum_push(MYSTERY_PHYSICS_CONSTANT, dx * pushback_factor)
        obj.x += minimum_push(MYSTERY_PHYSICS_CONSTANT, dx * (1 - pushback_factor))

        self.update_bounds()
        if getattr(obj, "update_bounds", None):
            obj.update_bounds()

    def collide_y(self, obj, iteration):
        if self.collision == False or getattr(obj, "collision", True) == False:
            return

        if not self.touching_ground(obj) or not self.colliding(obj):
            return

        if not obj.alive() or not self.alive():
            return

        if self.player_only and type(obj).__name__ != "Player":
            return

        if getattr(obj, "sprite_collision", None):
            self.sprite_collision(obj)
            obj.sprite_collision(self)
        else:
            self.tile_collision(obj)

        pushback_factor = getattr(obj, "pushback_factor", 1)

        if self.bottom > obj.top and self.top < obj.top: #going down
            dy = self.bottom - obj.top
            self.y -= dy
            self.on_ground = True
            self.vely = 0

        elif self.top < obj.bottom and self.bottom > obj.bottom: #going up
            dy = obj.bottom - self.top
            self.y += dy
            # obj.y -= dy * (1 - pushback_factor)
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

        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

    def update_pos(self, level, dt):
        search_rect = pygame.Rect(
            self.rect.centerx - SEARCH_RADIUS,
            self.rect.centery - SEARCH_RADIUS,
            SEARCH_RADIUS * 2,
            SEARCH_RADIUS * 2
        )

        colliders = []

        for group in self.groups():
            for s in group:
                if s is self or not getattr(s, "collision", False):
                    continue
                if search_rect.colliderect(s.rect):
                    colliders.append(s)

        for tile in level.collision_tiles:
            if search_rect.colliderect(tile.rect):
                colliders.append(tile)


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
