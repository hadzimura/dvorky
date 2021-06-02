#!/usr/bin/env python3
# coding=utf-8

from glob import glob
import pygame


class Samples(object):

    Category = {
        'ambient': list(),
        'speech': list(),
        'scene': list()
    }

    def __init__(self, audio_path=None, audio_format='wav'):

        pygame.mixer.init(48000, -16, 1, 1024)

        # Read and categorize all the available audio files
        audio_files = glob('{}/*{}'.format(str(audio_path), str(audio_format)))
        for audio_file in audio_files:
            for category in self.Category:
                if category in audio_file:
                    self.Category[category].append(audio_file)
        print(self.Category)
        exit()


    def volume(self, value):
        pygame.mixer.music.set_volume(value)

    def ambient(self):
        pygame.mixer.music.load(p)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy() == True:
            continue

        pass

    def speech(self):
        pass