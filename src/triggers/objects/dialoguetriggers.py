from src.triggers.triggerobject import Trigger

class DialogueSelectTrigger(Trigger):
    def on_select(self, player):
        self.level.game.dialogue_handler.set_dialogue(self.level.dialogues[self.name])

class DialogueAreaTrigger(Trigger):
    def on_trigger(self):
        self.level.game.dialogue_handler.set_dialogue(self.level.dialogues[self.name])
