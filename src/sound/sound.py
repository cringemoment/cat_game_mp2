import pygame
pygame.mixer.init()
pygame.mixer.set_num_channels(32)

class Sound():
    def __init__(self, game):
        self.game = game
        self.bg_music = None
        self.sounds = {}
        self.bg_sounds = {}

        self.load_sound("cannon_fire", "assets/sounds/cannon_fire.ogg")
        self.load_sound("background_music", "assets/sounds/bg_music.wav")

    def load_sound(self, file, file_path):
        self.sounds[file] = pygame.mixer.Sound(file_path)

    def load_bg_sounds(self, file, file_path):
        self.bg_sounds[file] = pygame.mixer.Sound(file_path)

    def play_sound(self, sound_name):
        self.sounds[sound_name].play()

    def play_bg_sound(self, sound_name):
        self.bg_sounds[sound_name].play()