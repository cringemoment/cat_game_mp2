from src.triggers.triggerobject import Trigger

class DialogueSelectTrigger(Trigger):
    def on_select(self, player):
        if not self.name in self.level.dialogues: return
        self.level.game.dialogue_handler.set_dialogue(self.level.dialogues[self.name])

class DialogueAreaTrigger(Trigger):
    def on_trigger(self):
        if not self.name in self.level.dialogues: return
        self.level.game.dialogue_handler.set_dialogue(self.level.dialogues[self.name])
