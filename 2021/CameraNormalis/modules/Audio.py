#!/usr/bin/env python3
# coding=utf-8

from glob import glob
import pygame
from random import randrange
import time


class Player(object):

    Category = {
        'ambient': dict(),
        'intro': dict(),
        'scene': dict()
    }

    def __init__(self, audio_path=None, audio_format='wav'):

        # Start the Mixer
        # pygame.mixer.pre_init(48000, -16, 1, 1024)  # frequency, size, channels, buffersize
        # pygame.init()  # turn all of pygame on.
        pygame.mixer.init(48000, -16, 1, 1024)

        self.count = 0
        self.audio_path = audio_path

        # Crerate the library of available sounds
        audio_files = glob('{}/*{}'.format(str(audio_path), str(audio_format)))
        for audio_file in audio_files:
            # a = pygame.mixer.Sound(audio_file)
            # audio_length = pygame.mixer.Sound.get_length(a)
            audio_name = audio_file.split('/')[-1].split('.')[0]
            for category in self.Category:
                if category in audio_name:
                    self.Category[category][audio_name] = 1
                    self.count += 1

    def get_random(self, category):
        r = randrange(0, len(self.Category[category]), 1)
        return self.Category[category][r]

    def showtime(self):

        while True:

            current_file = self.get_random('ambient')
            pygame.mixer.music.load('{}/{}'.format(self.audio_path, current_file))
            pygame.mixer.music.play()
            timer = 0
            current_volume = 0.5

            while pygame.mixer.music.get_busy():

                if timer == 0:
                    timer = time.time()

                if time.time() - timer > 5:
                    # After 5 seconds
                    current_volume = self.random_change(current_volume)
                    self.volume(current_volume)
                    timer = 0

    def self_test(self):
        # pygame.mixer.music.load('{}/self_test.mp3'.format(self.audio_path))
        pygame.mixer.music.load('{}/ambient-full-MP3.mp3'.format(self.audio_path))
        pygame.mixer.music.play()
        timer = 0
        current_volume = 0.5

        while pygame.mixer.music.get_busy():

            if timer == 0:
                timer = time.time()

            if time.time() - timer > 5:
                # After 5 seconds
                current_volume = self.random_change(current_volume)
                self.volume(current_volume)
                timer = 0
        exit()
        # filename: self_test.mp3

    @staticmethod
    def random_change(from_volume):

            next_volume = 0

            if from_volume < 0.3:
                next_volume = randrange(0, 2, 1) / 10
            elif from_volume > 0.7:
                next_volume = randrange(-2, 0, 1) / 10
            else:
                next_volume = randrange(-2, 2, 1) / 10

            return from_volume + next_volume

    def playlist(self, category):
        """ Create random loop """
        pass

    def list(self):
        for category in self.Category:
            print(category)
            print('---')
            for aname in sorted(self.Category[category]):
                print(' - {}'.format(aname))

    def volume(self, value):
         pygame.mixer.music.set_volume(value)

    def ambient(self):
         pygame.mixer.music.load(p)
         pygame.mixer.music.play()

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