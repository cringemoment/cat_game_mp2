import pygame
import math

from src.player.playerinput import InputHandler, CONTROLLER_DEADZONE

from src.physics.physicsobject import PhysicsObject, AIR_RESISTANCE
from src.physics.gun import Gun

#each tile is 32 pixels
#time is measured in seconds
#acceleration is measured in pixels per frame
JUMP_POWER = 13
CROUCHING_JUMP_POWER = 11
COYOTE_TIME = 0.15

MAXX_VELO = 5
X_ACCEL = 2
CROUCHING_ACCEL = 1
CROUCHING_MAXX_VELO = 3

BULLET_HIT_MAXVELO = 10
BULLET_HIT_AR = 0.1

class Player(PhysicsObject):
    def __init__(self, index = 0, sprites = None):
        super().__init__("beh")
        self.set_sprites(sprites)
        level = None

        self.index = index

        #handling controls
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
        self.trigger_interactible = True

        self.current_velo = MAXX_VELO
        self.jump_power = JUMP_POWER

        self.uncrouch_queued = False

        #Coyote time implementation
        self.on_ground = False
        self.coyote_time = 0

        #anti spam stuff
        self.jump_timer = 0
        self.shoot_timer = 0

        self.gun = Gun(level, self)
        self.aim_angle = 0

        self.current_trigger_inside = None

    def load_inputs(self, input_device, controls):
        self.input_device = input_device
        self.input_handler = InputHandler(self, input_device, controls)

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
            self.vely = -self.jump_power
            self.on_ground = False
            self.coyote_time = 0
            self.level.game.sound_handler.play_sound("jump")

    def crouch(self):
        # self.play_anim("crouchanim", play_once = True)
        # self.level.game.sound_handler.play_sound("cannon_fire")
        self.change_image("crouch")
        self.accel = CROUCHING_ACCEL
        self.current_velo = CROUCHING_MAXX_VELO
        self.jump_power = CROUCHING_JUMP_POWER

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
            self.current_velo = MAXX_VELO
            self.uncrouch_queued = False
            self.jump_power = JUMP_POWER

    def select(self):
        good = False
        for trigger in self.level.tiles.area_triggers:
            if self.rect.colliderect(trigger.rect):
                self.current_trigger_inside = trigger.name
                good = True
            trigger.select(self)
        if not good:
            self.current_trigger_inside = None

    def update_timers(self, dt):
        if self.on_ground:
            self.coyote_time = COYOTE_TIME
        elif self.coyote_time > 0:
            self.coyote_time -= dt

    def update_aim(self):
        camera = self.level.camera
        screen = pygame.display.get_surface()
        screen_width, screen_height = screen.get_size()

        tile_size = screen_width / camera.width
        scale_factor = tile_size / 32

        player_world = pygame.Vector2(self.rect.center)
        player_screen = pygame.Vector2((player_world.x - camera.x) * scale_factor, (player_world.y - camera.y) * scale_factor)

        if type(self.input_device).__name__ == "Controller":
            axis_x = self.input_device.get_axis(2)
            axis_y = self.input_device.get_axis(3)

            if abs(axis_x) > CONTROLLER_DEADZONE or abs(axis_y) > CONTROLLER_DEADZONE:
                self.aim_angle = math.degrees(math.atan2(-axis_y, axis_x))
        else:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - player_screen.x
            dy = mouse_y - player_screen.y
            self.aim_angle = math.degrees(math.atan2(-dy, dx))

    def update(self, level, dt):
        self.tiles = level.tiles
        self.input_handler.handle_inputs()

        if self.bullet_physics:
            self.maxx_velo = BULLET_HIT_MAXVELO
            self.air_resistance = BULLET_HIT_AR
        else:
            self.maxx_velo = self.current_velo
            self.air_resistance = AIR_RESISTANCE

        self.update_pos(self.tiles, dt)
        self.update_aim()
        self.gun.update()
        self.update_sprites(dt)

        if self.uncrouch_queued:
            self.check_uncrouch()
