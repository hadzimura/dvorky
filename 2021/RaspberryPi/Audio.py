#!/usr/bin/env python3
# coding=utf-8

from glob import glob
import pygame


class Samples(object):

    def __init__(self, audio_path=None):

        pygame.mixer.init(48000, -16, 1, 1024)

        files = glob(audio_path + '*.mp3')
        for p in files:
            print('{}'.format(p))
            pygame.mixer.music.load(p)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue

    def volume(self, value):
        pygame.mixer.music.set_volume(value)

    def ambient(self):
        pass

    def speech(self):
        pass