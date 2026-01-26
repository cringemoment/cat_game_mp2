from src.triggers.triggerobject import Trigger
import json

class LevelEnd(Trigger):
    def on_trigger(self):
        f = json.load(open("src/levels/unlocked_levels.json"))
        f[f"level_{self.properties["next_level"]}"] = 1
        json.dump(f, open("src/levels/unlocked_levels.json", "w"))
        self.level.game.phone_book.current_popup = self.level.game.phone_book.dialogues[f"level_{self.properties["next_level"]}"]

        if "enddialogue" in self.level.dialogues and not self.level.dialogues["enddialogue"].finished:
            self.level.dialogues["enddialogue"].on_finish = self.go_next
            self.level.game.dialogue_handler.set_dialogue(self.level.dialogues["enddialogue"])
        else:
            self.go_next()

    def go_next(self):
        self.level.game.paused = False
        self.level.game.transition_load_level("level_end")
