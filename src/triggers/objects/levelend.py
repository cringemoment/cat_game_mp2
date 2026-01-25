from src.triggers.triggerobject import Trigger

class LevelEnd(Trigger):
    def on_trigger(self):
        if "enddialogue" in self.level.dialogues:
            self.level.dialogues["enddialogue"].on_finish = self.go_next
            self.level.game.dialogue_handler.set_dialogue(self.level.dialogues["enddialogue"])

    def go_next(self):
        self.level.game.paused = False
        self.level.game.transition_load_level("level_end")
