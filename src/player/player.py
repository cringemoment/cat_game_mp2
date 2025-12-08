import pygame
import math

from src.player.playerinput import InputHandler, CONTROLLER_DEADZONE

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
    def __init__(self, index = 0, level = None, controls = None, input_device = None, sprites = None):
        super().__init__(level)
        self.set_sprites(sprites)

        self.index = index

        #handling controls
        self.input_handler = InputHandler(self, controls, input_device)
        self.controls = controls
        self.input_device = input_device
        self.leftclick_down = False
        self.keys_pressed = []

        self.rect = self.image.get_rect(topleft = (0, 0))

        #movement stuff
        self.x, self.y = 0, 0
        self.maxx_velo = MAXX_VELO
        self.accel = X_ACCEL
        self.collision = True
        self.bullet_physics = False #lower friction after being hit by a bullet
        self.pushback_factor = 0.01

        self.uncrouch_queued = False

        #Coyote time implementation
        self.on_ground = False
        self.coyote_time = 0

        #anti spam stuff
        self.jump_timer = 0
        self.shoot_timer = 0

        self.gun = Gun(level, self)
        self.aim_angle = 0

    def shoot(self):
        self.gun.shoot()

    def go_horizontal(self, dir):
        if self.current_sprite == "default":
            self.change_image("running")

        if type(self.input_device).__name__ == "Controller":
            self.velx += self.accel * self.input_device.get_axis(0)
        else:
            self.velx += self.accel * dir

    def reset_run(self):
        if self.current_sprite == "running":
            self.change_image("default")

    def jump(self):
        if self.on_ground or self.coyote_time > 0:
            self.vely = -JUMP_POWER
            self.on_ground = False
            self.coyote_time = 0

    def crouch(self):
        # self.play_anim("crouchanim", play_once = True)
        self.change_image("crouch")
        self.accel = CROUCHING_ACCEL
        self.maxx_velo = CROUCHING_MAXX_VELO

    def uncrouch(self):
        self.uncrouch_queued = True

    def check_uncrouch(self):
        colliders = [i for i in self.level.tiles.physics_objects if i is not self and getattr(i, "collision", False)]
        colliders.extend(self.level.tiles.collision_tiles)

        self.change_image("default")
        self.update_bounds()

        for obj in colliders:
            if self.colliding(obj):
                if getattr(obj, "pushback_factor", 1) != 1:
                    obj.y -= (obj.y + obj.rect.height) - self.y
                    obj.update_bounds()
                else:
                    self.change_image("crouch")
                    self.uncrouch_queued = True

                break

        else:
            self.change_image("default")
            self.update_bounds()
            self.accel = X_ACCEL
            self.uncrouch_queued = False

    def update_timers(self, dt):
        if self.on_ground:
            self.coyote_time = COYOTE_TIME
        elif self.coyote_time > 0:
            self.coyote_time -= dt

    def update_aim(self):
        if type(self.input_device).__name__ == "Joystick":
            axis_x = self.input_device.get_axis(2)
            axis_y = self.input_device.get_axis(3)

            if abs(axis_x) > CONTROLLER_DEADZONE or abs(axis_y) > CONTROLLER_DEADZONE:
                self.aim_angle = math.degrees(math.atan2(-axis_y, axis_x))
        else:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - self.rect.centerx
            dy = mouse_y - self.rect.centery
            self.aim_angle = math.degrees(math.atan2(-dy, dx))

    def update(self, level, dt):
        self.tiles = level.tiles
        self.input_handler.handle_inputs()

        if self.bullet_physics:
            self.maxx_velo = BULLET_HIT_MAXVELO
            self.air_resistance = BULLET_HIT_AR
        else:
            self.maxx_velo = MAXX_VELO
            self.air_resistance = AIR_RESISTANCE

        self.update_pos(self.tiles, dt)
        self.update_aim()
        self.gun.update()
        self.update_sprites(dt)

        if self.uncrouch_queued:
            self.check_uncrouch()
