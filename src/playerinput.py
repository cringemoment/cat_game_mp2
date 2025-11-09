import pygame

CONTROLLER_DEADZONE = 0.2 #avoid controller drift, just in case

class Keyboard():
    def __init__(self):
        self.lmb = lambda: pygame.mouse.get_pressed()[0]
        self.mmb = lambda: pygame.mouse.get_pressed()[1]
        self.rmb = lambda: pygame.mouse.get_pressed()[2]

    def get_key(self, key): #i hate how pygame handles keys
        return lambda: pygame.key.get_pressed()[key]

class Controller():
    def __init__(self, joystick):
        self.joystick = joystick

        #joystick stuff
        self.J1_x = lambda: self.joystick.get_axis(0)
        self.J1_y = lambda: self.joystick.get_axis(1)
        self.J2_x = lambda: self.joystick.get_axis(2)
        self.J2_y = lambda: self.joystick.get_axis(3)

        #for convenience
        self.J1_left = lambda: self.joystick.get_axis(0) if self.joystick.get_axis(0) + CONTROLLER_DEADZONE < 0 else 0
        self.J1_right = lambda: self.joystick.get_axis(0) if self.joystick.get_axis(0) - CONTROLLER_DEADZONE > 0 else 0

        self.J1_up = lambda: self.joystick.get_axis(1) if self.joystick.get_axis(1) + CONTROLLER_DEADZONE < 0 else 0
        self.J1_down = lambda: self.joystick.get_axis(1) if self.joystick.get_axis(1) - CONTROLLER_DEADZONE > 0 else 0

        #buttons
        self.B_down = lambda: self.joystick.get_button(0)
        self.B_right = lambda: self.joystick.get_button(1)
        self.B_left = lambda: self.joystick.get_button(2)
        self.B_up = lambda: self.joystick.get_button(3)

        #bumpers and triggers
        self.LB = lambda: self.joystick.get_button(5)
        self.RB = lambda: self.joystick.get_button(5)

        self.LT = lambda: self.joystick.get_axis(4) if self.joystick.get_axis(4) > 0 else 0 #idk why theyre axises
        self.RT = lambda: self.joystick.get_axis(5) if self.joystick.get_axis(5) > 0 else 0

class InputHandler:
    def __init__(self, player, controls, joystick = None):
        self.player = player
        self.controls = controls
        self.joystick = joystick

        self.keys_pressed = []

    def handle_inputs(self):
        held_events = {
            "left": lambda: self.player.go_horizontal(-1),
            "right": lambda: self.player.go_horizontal(1),
        }

        keydown_events = {
            "left": lambda: self.player.set_facing(-1),
            "right": lambda: self.player.set_facing(1),
            "crouch": lambda: self.player.crouch(),
            "shoot": lambda: self.player.shoot(),
            "jump": lambda: self.player.jump()
        }

        keyup_events = {
            "crouch": lambda: self.player.uncrouch()
        }

        keys = pygame.key.get_pressed()

        for control in held_events:
            if self.controls[control]():
                held_events[control]()
                self.player.bullet_physics = False

        for control in keydown_events:
            if self.controls[control]():
                if control not in self.keys_pressed:
                    keydown_events[control]()
                    self.keys_pressed.append(control)
            else:
                if control in self.keys_pressed:
                    self.keys_pressed.remove(control)
                    if control in keyup_events:
                        keyup_events[control]()
