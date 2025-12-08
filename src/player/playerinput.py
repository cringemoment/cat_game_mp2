import pygame

CONTROLLER_DEADZONE = 0.2 #avoid controller drift, just in case

MOUSE_BUTTONS = {
    "lmb": lambda: pygame.mouse.get_pressed()[0],
    "mmb": lambda: pygame.mouse.get_pressed()[1],
    "rmb": lambda: pygame.mouse.get_pressed()[2]
}

class Keyboard():
    def __init__(self):
        self.lmb = "lmb"
        self.mmb = "mmb"
        self.rmb = "rmb"

    def get_key(self, key): #i hate how pygame handles keys
        if key in MOUSE_BUTTONS:
            return lambda: MOUSE_BUTTONS[key]()

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
        self.LB = lambda: self.joystick.get_button(4)
        self.RB = lambda: self.joystick.get_button(5)

        self.LT = lambda: self.joystick.get_axis(4) if self.joystick.get_axis(4) > 0 else 0 #idk why theyre axises
        self.RT = lambda: self.joystick.get_axis(5) if self.joystick.get_axis(5) > 0 else 0

        #auxiliary buttons
        self.minus = lambda: self.joystick.get_button(6)
        self.plus = lambda: self.joystick.get_button(7)

    def get_key(self, key):
        return getattr(self, key)

class InputHandler:
    def __init__(self, player, input_device, controls):
        self.player = player
        self.controls = controls.controls
        self.input_device = input_device

        self.keys_pressed = []

    def handle_inputs(self):
        held_events = {
            "left": lambda: self.player.go_horizontal(-1),
            "right": lambda: self.player.go_horizontal(1),
        }

        keydown_events = {
            "left": lambda: self.player.set_facing(-1),
            "right": lambda: self.player.set_facing(1),
            "down": lambda: self.player.crouch(),
            "main_action": lambda: self.player.shoot(),
            "jump": lambda: self.player.jump()
        }

        keyup_events = {
            "down": lambda: self.player.uncrouch(),
            "left": lambda: self.player.reset_run(),
            "right": lambda: self.player.reset_run()
        }

        keys = pygame.key.get_pressed()

        for control in held_events:
            # if self.input_device.get_key(self.controls[control])():
            if any([self.input_device.get_key(i)() for i in self.controls[control]]):
                held_events[control]()
                self.player.bullet_physics = False

        for control in keydown_events:
            if any([self.input_device.get_key(i)() for i in self.controls[control]]):
                if control not in self.keys_pressed:
                    keydown_events[control]()
                    self.keys_pressed.append(control)
            else:
                if control in self.keys_pressed:
                    self.keys_pressed.remove(control)
                    if control in keyup_events:
                        keyup_events[control]()
