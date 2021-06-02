#!/usr/bin/env python3
# coding=utf-8

from glob import glob
import pygame


class Player(object):

    Category = {
        'ambient': dict(),
        'intro': dict(),
        'scene': dict()
    }

    def __init__(self, audio_path=None, audio_format='wav'):

        # Start the Mixer
        pygame.mixer.pre_init(44100, 16, 2, 4096)  # frequency, size, channels, buffersize
        pygame.init()  # turn all of pygame on.
        pygame.mixer.init()

        self.count = 0

        # Crerate the library of available sounds
        audio_files = glob('{}/*{}'.format(str(audio_path), str(audio_format)))
        for audio_file in audio_files:
            a = pygame.mixer.Sound(audio_file)
            audio_length = pygame.mixer.Sound.get_length(a)
            audio_name = audio_file.split('/')[-1].split('.')[0]
            for category in self.Category:
                if category in audio_name:
                    self.Category[category][audio_length] = audio_name
                    self.count += 1

    def playlist(self, category):
        """ Get one random """
        pass

    def list(self):
        for category in self.Category:
            print(category)
            print('---')
            for timelenght in sorted(self.Category[category]):
                print('{}: {}'.format(str(int(timelenght)), str(self.Category[category][timelenght])))

#
# class Player(object):
#
#     def __init__(self):
#         pygame.mixer.init(48000, -16, 1, 1024)
#
#     def volume(self, value):
#         pygame.mixer.music.set_volume(value)
#
#     def ambient(self):
#         pygame.mixer.music.load(p)
#         pygame.mixer.music.play()
#         while pygame.mixer.music.get_busy() == True:
#             continue
#
#         pass
#
#     def speech(self):
#         pass