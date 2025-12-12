import pygame

class DialogueBox:
    def __init__(self, image, text, speed):
        pass

    def draw(self, surface):
        pass

    def update(self, surface, dt):
        self.draw(surface)

class DialogueInputHandler():
    def __init__(self, dialoguehandler, input1, input2, controls1, controls2):
        self.dialoguehandler = dialoguehandler
        self.inputs = [input1, input2]
        self.controllayouts = [controls1, controls2]

        self.controls = {
            "select": lambda: self.dialoguehandler.current_dialogue.next(),
        }

        self.keys = {}

        for input, control in zip(self.inputs, self.controllayouts):
            for keys in self.menucontrols:
                for key in control.controls[keys]:
                    self.keys[input.get_key(key)] = keys

        self.pressed = []

    def check(self):
        for key in self.keys:
            if key():
                if key in self.pressed: continue

                self.pressed.append(key)
                self.controls[self.keys[key]]()

            else:
                if key in self.pressed:
                    self.pressed.remove(key)

class Dialogue:
    def __init__(self):
        self.dialogues = []
        self.current_dialogue_box_index = 0
        self.current_dialogue_box = self.dialogues[0]

    def next(self):
        self.current_dialogue_box_index += 1
        self.current_dialogue_box = self.dialogues[self.current_dialogue_box_index]

    def update(self):
        self.current_dialogue_box.update()
        self.current_dialogue_box.draw()
