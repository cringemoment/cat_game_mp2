import pygame
import math

from src.playerinput import InputHandler, CONTROLLER_DEADZONE

from src.physics.physicsobject import PhysicsObject, AIR_RESISTANCE
from src.physics.gun import Gun

#each tile is 32 pixels
#time is measured in seconds
#acceleration is measured in pixels per frame
JUMP_POWER = 12
COYOTE_TIME = 0.15

MAXX_VELO = 5
X_ACCEL = 2
CROUCHING_ACCEL = 1.4
CROUCHING_MAXX_VELO = 3

BULLET_HIT_MAXVELO = 10
BULLET_HIT_AR = 0.1

class Player(PhysicsObject):
    def __init__(self, coords, controls, sprites, joystick = None):
        super().__init__()
        self.set_sprites(sprites)

        #handling controls
        self.input_handler = InputHandler(self, controls, joystick)
        self.controls = controls
        self.joystick = joystick
        self.leftclick_down = False
        self.keys_pressed = []

        self.rect = self.image.get_rect(topleft = coords)

        #movement stuff
        self.x, self.y = coords
        self.maxx_velo = MAXX_VELO
        self.accel = X_ACCEL
        self.collision = True
        self.bullet_physics = False #lower friction after being hit by a bullet
        self.pushable = True
        self.pushback_factor = 0

        self.uncrouch_queued = False

        #Coyote time implementation
        self.on_ground = False
        self.coyote_time = 0

        #anti spam stuff
        self.jump_timer = 0
        self.shoot_timer = 0

        self.gun = Gun(self)
        self.aim_angle = 0

    def shoot(self):
        self.gun.shoot()

    def go_horizontal(self, dir):
        if self.joystick:
            self.velx += self.accel * self.joystick.get_axis(0)
        else:
            self.velx += self.accel * dir

    def jump(self):
        if self.on_ground or self.coyote_time > 0:
            self.vely = -JUMP_POWER
            self.on_ground = False
            self.coyote_time = 0

    def crouch(self):
        self.change_image("crouch")
        self.accel = CROUCHING_ACCEL
        self.maxx_velo = CROUCHING_MAXX_VELO

    def uncrouch(self):
        self.change_image("default")
        self.accel = X_ACCEL
        self.maxx_velo = MAXX_VELO

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
        self.tiles = tiles
        self.input_handler.handle_inputs()

        if self.bullet_physics:
            self.maxx_velo = BULLET_HIT_MAXVELO
            self.air_resistance = BULLET_HIT_AR
        else:
            self.maxx_velo = MAXX_VELO
            self.air_resistance = AIR_RESISTANCE

        self.update_pos(tiles, dt)
        self.update_aim()
        self.gun.update()
