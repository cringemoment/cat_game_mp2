import json

playeroutputs = [
    "left",
    "right",
    "jump",
    "crouch",
    "main_action",
    "off_action",
    "interact"
]

class Controls:
    def __init__(self, name, input_type):
        self.name = name
        self.input_type = type
        self.controls = {}

    def load_controls(self, file):
        f = json.load(file)

    def write_controls(self):
        out = {
            "input_type" = self.input_type,
            "controls": self.controls
        }

        json.dump(out, open(self.name, "w"))

test_controls = {
    "jump": "pygame.K_SPACE",
    "left": "pygame.K_a",
    "right": "pygame.K_d",
    "crouch": "pygame.K_s",
    "shoot": "keyboard.lmb"
}

test_controller_controls = {
    "jump": "B_down",
    "left": "J1_left",
    "right": "J1_right",
    "crouch": "J1_down",
    "shoot": "RB"
}
