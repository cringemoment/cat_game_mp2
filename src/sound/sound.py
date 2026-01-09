import pygame
pygame.mixer.init()
pygame.mixer.set_num_channels(32)

class Sound():
    def __init__(self, game):
        self.game = game
        self.bg_music = None
        self.sounds = {}
        self.bg_music = {}
        self.bg_music_channel = pygame.mixer.Channel(0)

        self.load_sound("cannon_fire", "assets/sounds/cannon_fire.ogg")
        self.load_bg_music("level0_bg", "assets/sounds/level0_bg.ogg")

    def load_sound(self, file, file_path):
        self.sounds[file] = pygame.mixer.Sound(file_path)

    def load_bg_music(self, file, file_path):
        self.bg_music[file] = pygame.mixer.Sound(file_path)

    def play_sound(self, sound_name):
        self.sounds[sound_name].play()

    def play_bg_music(self, sound_name):
        self.bg_music_channel.stop()
        if sound_name:
            self.bg_music_channel.play(self.bg_music[sound_name], loops = -1)