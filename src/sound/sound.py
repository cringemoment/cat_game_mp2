import pygame
import json

CHANNELS = 64
pygame.mixer.init()
pygame.mixer.set_num_channels(CHANNELS)
pygame.mixer.set_reserved(1)

#ffmpeg -i door_open.m4a -c:a libvorbis -q:a 4 door_open.ogg

class Sound():
    def __init__(self, game):
        self.game = game
        self.bg_music = None
        self.sounds = {}
        self.bg_music = {}
        self.bg_music_channel = pygame.mixer.Channel(0)
        self.settings_file = "settings.json"

        self.load_sound("cannon_fire", "assets/sounds/cannon_fire.ogg")
        self.load_sound("jump", "assets/sounds/jump.ogg")
        self.load_sound("button", "assets/sounds/button.ogg")
        self.load_sound("door_open", "assets/sounds/door_open.ogg")
        self.load_sound("door_close", "assets/sounds/door_close.ogg")
        self.load_sound("ringtone", "assets/sounds/ringtone.ogg")
        self.load_sound("dialogue", "assets/sounds/dialogue.ogg")
        self.load_sound("loading_in", "assets/sounds/loading_in.ogg")

        self.load_bg_music("level0_bg", "assets/sounds/level0_bg.ogg")

    def load_sound(self, file, file_path):
        self.sounds[file] = pygame.mixer.Sound(file_path)

    def load_bg_music(self, file, file_path):
        self.bg_music[file] = pygame.mixer.Sound(file_path)

    def load_volume(self):
        self.volume = json.load(open(self.settings_file))["Volume"]/10
        pygame.mixer.music.set_volume(self.volume)
        for i in range(1, CHANNELS):
            pygame.mixer.Channel(i).set_volume(self.volume)

    def play_sound(self, sound_name):
        self.load_volume()
        for i in range(1, 64):
            channel = pygame.mixer.Channel(i)
            if not channel.get_busy():
                channel.play(self.sounds[sound_name])
                return

    def play_sound_blocking(self, sound_name):
        self.load_volume()
        sound = self.sounds[sound_name]
        channel = sound.play()
        if channel is None:
            return

        while channel.get_busy():
            pygame.time.wait(10)

    def play_bg_music(self, sound_name):
        self.load_volume()
        self.bg_music_channel.stop()
        if sound_name:
            self.bg_music_channel.play(self.bg_music[sound_name], loops = -1)
