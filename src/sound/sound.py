import pygame

pygame.mixer.init()
pygame.mixer.set_num_channels(64)
pygame.mixer.set_reserved(1)

#ffmpeg -i door_open.m4a -c:a libvorbis -q:a 4 door_open.ogg

class Sound():
    def __init__(self, game):
        self.game = game
        self.bg_music = None
        self.sounds = {}
        self.bg_music = {}
        self.bg_music_channel = pygame.mixer.Channel(0)

        self.load_sound("cannon_fire", "assets/sounds/cannon_fire.ogg")
        self.load_sound("jump", "assets/sounds/jump.ogg")
        self.load_sound("button", "assets/sounds/button.ogg")
        self.load_sound("door_open", "assets/sounds/door_open.ogg")
        self.load_sound("door_close", "assets/sounds/door_close.ogg")
        self.load_sound("ringtone", "assets/sounds/ringtone.ogg")
        self.load_sound("dialogue", "assets/sounds/dialogue.ogg")
        self.load_bg_music("level0_bg", "assets/sounds/level0_bg.ogg")

    def load_sound(self, file, file_path):
        self.sounds[file] = pygame.mixer.Sound(file_path)

    def load_bg_music(self, file, file_path):
        self.bg_music[file] = pygame.mixer.Sound(file_path)

    def play_sound(self, sound_name):
        for i in range(1, 64):
            channel = pygame.mixer.Channel(i)
            if not channel.get_busy():
                channel.play(self.sounds[sound_name])
                return

    def play_sound_blocking(self, sound_name):
        sound = self.sounds[sound_name]
        channel = sound.play()
        if channel is None:
            return

        while channel.get_busy():
            pygame.time.wait(10)

    def play_bg_music(self, sound_name):
        self.bg_music_channel.stop()
        if sound_name:
            self.bg_music_channel.play(self.bg_music[sound_name], loops = -1)
