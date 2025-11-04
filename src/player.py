import pygame
import math

from src.physicsobject import PhysicsObject
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

CONTROLLER_DEADZONE = 0.05 #avoid controller drift, just in case

class Player(PhysicsObject):
    def __init__(self, coords, controls, sprites, joystick = None):
        super().__init__(sprites)

        #handling controls
        self.controls = controls
        self.joystick = joystick
        self.leftclick_down = False
        self.keys_pressed = []

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

    def go_horizontal(self, dir = None):
        if dir:
            self.velx += self.accel * dir
        else:
            self.velx += self.accel * self.joystick.get_axis(0)

    def jump(self):
        self.vely = -JUMP_POWER
        self.on_ground = False
        self.coyote_time = 0

    def crouch(self):
        bottom = self.rect.bottom
        self.change_image("crouch")
        self.rect.bottom = bottom

    def uncrouch(self):
        self.change_image("idle")

    def handle_input(self):
        held_controls = {
            "left": lambda: self.go_horizontal(-1),
            "right": lambda: self.go_horizontal(1)
        }

        keydown_events = {
            "left": lambda: self.set_facing(-1),
            "right": lambda: self.set_facing(1),
            "crouch": lambda: self.crouch()
        }

        keyup_events = {
            "crouch": lambda: self.uncrouch()
        }

        if not self.joystick: #handl ing kb first
            keys = pygame.key.get_pressed()

            # Horizontal movement
            # if keys[self.controls["left"]]:
            #     self.go_horizontal(-1)
            # if keys[self.controls["right"]]:
            #     self.go_horizontal(1)

            for control in held_controls:
                if keys[self.controls[control]]:
                    held_controls[control]()

            for control in keydown_events:
                if keys[self.controls[control]]:
                    if control not in self.keys_pressed:
                        keydown_events[control]()
                        self.keys_pressed.append(control)
                else:
                    if control in self.keys_pressed:
                        self.keys_pressed.remove(control)
                        if control in keyup_events:
                            keyup_events[control]()

            # Jumping
            if keys[self.controls["jump"]] and (self.on_ground or self.coyote_time > 0):
                self.jump()

            # Crouching
            # if keys[self.controls["crouch"]]:
            #     self.crouch()
            # else:
            #     self.uncrouch()

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
                self.go_horizontal()

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

    def update_timers(self, dt):
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
        self.update_timers(dt)
        self.update_aim()
        self.gun.update()
