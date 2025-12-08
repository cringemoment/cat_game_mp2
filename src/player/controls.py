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

    def load(self, file):
        self.controls = json.load(open(file))

    def write(self):
        out = {
            "input_type": self.input_type,
            "controls": self.controls
        }

        json.dump(out, open(self.name, "w"))

kbcontrols = Controls("p1", "k")
kbcontrols.load("src/player/controls/profile_1.json")

try:
    jycontrols = Controls("p2", "j")
    jycontrols.load("src/player/controls/profile_2.json")
except Exception as e:
    print(e)
