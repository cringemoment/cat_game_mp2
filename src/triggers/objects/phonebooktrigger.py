from src.triggers.triggerobject import Trigger

class PhoneBook(Trigger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    #wildly jank but itll work
    def select(self, player):
        if self.players_inside[player.index]:
            # self.level.game.sound_handler.play_sound("ringtone")
            self.level.game.phone_book.play()

        self.level.game.phone_book.loading = False
