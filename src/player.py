import pygame
import math

from src.spriteobject import Sprite
from src.gun import Gun

#each tile is 32 pixels
#time is measured in seconds
#acceleration is measured in pixels per frame
GRAVITY = 0.5
FRICTION = 0.8
MAXX_VELO = 10
JUMP_POWER = 12
COYOTE_TIME = 0.1
X_ACEL = 1.4

CONTROLLER_DEADZONE = 0.08 #avoid controller drift, just in case

class Player(Sprite):
    def __init__(self, coords, controls, sprites, joystick = None):
        super().__init__(sprites)

        #handling controls
        self.controls = controls
        self.joystick = joystick
        self.leftclick_down = False

        #temp image
        # self.image = pygame.Surface((32, 32))
        # self.image.fill((255, 0, 0))
        # self.rect = self.image.get_rect(topleft = coords)

        self.change_image("idle")
        self.rect = self.image.get_rect(topleft = coords)

        #movement stuff
        self.x, self.y = coords
        self.velx = 0
        self.vely = 0
        self.accel = X_ACEL

        #Coyote time implementation
        self.on_ground = False
        self.coyote_time = 0

        self.gun = Gun(self)
        self.aim_angle = 0

    def shoot(self):
        self.gun.shoot()

    def handle_input(self):
        if not self.joystick: #handling kb first
            keys = pygame.key.get_pressed()

            # Horizontal movement
            if keys[self.controls["left"]]:
                self.velx -= self.accel
            if keys[self.controls["right"]]:
                self.velx += self.accel

            # Jumping
            if keys[self.controls["jump"]] and (self.on_ground or self.coyote_time > 0):
                self.vely = -JUMP_POWER
                self.on_ground = False
                self.coyote_time = 0

            mouse_pressed = pygame.mouse.get_pressed()
            if mouse_pressed[0]:  # left click
                if not self.leftclick_down:
                    self.shoot()
                self.leftclick_down = True
            else:
                self.leftclick_down = False

        else:
            axis_x = self.joystick.get_axis(0) #the left-right motion of the first (left) joystick
            if abs(axis_x) > CONTROLLER_DEADZONE:
                self.velx += self.accel * axis_x

            if self.joystick.get_button(0) and (self.on_ground or self.coyote_time > 0):
                self.vely = -JUMP_POWER
                self.on_ground = False
                self.coyote_time = 0

            if self.joystick.get_button(5):
                self.shoot()

        # Clamp horizontal velocity
        if self.velx > MAXX_VELO:
            self.velx = MAXX_VELO
        elif self.velx < -MAXX_VELO:
            self.velx = -MAXX_VELO

        # Friction
        if self.velx > 0:
            self.velx -= FRICTION
            if self.velx < 0:
                self.velx = 0
        elif self.velx < 0:
            self.velx += FRICTION
            if self.velx > 0:
                self.velx = 0

    def update_pos(self, tiles, dt, *args):
        #dealing with horizontal movement first
        self.x += self.velx
        self.rect.x = int(self.x)

        for tile in tiles:
            if self.rect.colliderect(tile.rect):
                if self.velx > 0:  # moving right
                    self.rect.right = tile.rect.left
                elif self.velx < 0:  # moving left
                    self.rect.left = tile.rect.right
                self.velx = 0
                self.x = self.rect.x

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

        #dealing with coyote time
        if self.on_ground:
            self.coyote_time = COYOTE_TIME
        elif self.coyote_time > 0:
            self.coyote_time -= dt

    def update_aim(self):
        if self.joystick:
            axis_x = self.joystick.get_axis(2)
            axis_y = self.joystick.get_axis(3)

            if abs(axis_x) > CONTROLLER_DEADZONE or abs(axis_y) > CONTROLLER_DEADZONE:
                self.aim_angle = math.degrees(math.atan2(-axis_y, axis_x))
        else:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - self.rect.centerx
            dy = mouse_y - self.rect.centery
            self.aim_angle = math.degrees(math.atan2(-dy, dx))

    def update(self, tiles, dt):
        self.handle_input()
        self.update_pos(tiles, dt)
        self.update_aim()
        self.gun.update()
