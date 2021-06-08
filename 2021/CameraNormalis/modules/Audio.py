#!/usr/bin/env python3
# coding=utf-8

from glob import glob
import pygame
from random import randrange
import time


class Player(object):

    Category = {
        'ambient': list(),
        'intro': list(),
        'scene': list()
    }

    def __init__(self, audio_path=None, audio_format='mp3'):

        self.audio_path = audio_path
        self.default_volume = 0.5
        self.current_volume = 0.5
        self.speech_volume = 1

        # Start the Mixer
        pygame.mixer.init(48000, -16, 1, 1024)

        self.volume(self.default_volume)

        # Create the library of available sounds
        audio_files = glob('{}/*{}'.format(str(audio_path), str(audio_format)))
        for audio_file in audio_files:
            audio_name = audio_file.split('/')[-1]
            for category in self.Category:
                if category in audio_name:
                    self.Category[category].append(audio_name)

    def get_track(self, category):
        random_song = randrange(0, len(self.Category[category]), 1)
        return self.Category[category][random_song]

    def play_track(self, track_name, set_volume=None):

        # Load track
        pygame.mixer.music.load('{}/{}'.format(self.audio_path, track_name))

        # Set the initial volume
        if set_volume is not None:
            self.volume(set_volume)
        else:
            self.volume(self.current_volume)

        # Play track
        pygame.mixer.music.play()

        return None

    def animate_track(self, change_period=5):
        """ While the track is playing, make subtle changes to it's amplitude """
        # Set the timer
        timer = time.time()

        # Set starting volume to default Player value
        current_volume = self.current_volume

        # Loop while the track is playing
        while pygame.mixer.music.get_busy():

            # When the timer expire, roll the Fake Dice and tweak the volume
            if time.time() - timer > change_period:

                current_volume = self.roll_fake_dice(current_volume)
                self.volume(current_volume)

                # Reset the timer
                timer = time.time()

        return None

    def partytime(self, show_lenght):

        """ Play ambient tracks for the specified length """

        # Start time
        show_start = time.time()

        # Play ambient
        while time.time() - show_start < show_lenght:

            # Get and play randomly chosen track from 'ambient' category
            print('Playing ambient')
            self.play_track(self.get_track('ambient'), set_volume=self.current_volume)

            # Tweak the track volume during playtime
            print('Animating ambient')
            self.animate_track()

            # Window of the opportunity for scenic sample (1/5)
            # if randrange(1, 5, 1) > 4:
            #     # Play random scenic sample
            #     self.play_track(self.get_track('scene'))
            #     self.wait_for_end_of_track()

        return None

    @staticmethod
    def wait_for_end_of_track():
        """ Only wait for track to end and simply return control afterwards """
        while pygame.mixer.music.get_busy():
            pass
        return None

    def announce(self):
        self.play_track(self.get_track('announce'), set_volume=self.speech_volume)
        self.wait_for_end_of_track()
        return None

    def self_test(self):
        # pygame.mixer.music.load('{}/self_test.mp3'.format(self.audio_path))
        pygame.mixer.music.load('{}/ambient-full-MP3.mp3'.format(self.audio_path))
        pygame.mixer.music.play()
        timer = 0
        current_volume = self.default_volume

        while pygame.mixer.music.get_busy():

            if timer == 0:
                timer = time.time()

            if time.time() - timer > 5:
                # After 5 seconds
                current_volume = self.roll_fake_dice(current_volume)
                self.volume(current_volume)
                timer = 0
        exit()
        # filename: self_test.mp3

    @staticmethod
    def roll_fake_dice(from_volume):
        """
        Volume range: 0..1
        Volume step: 0.2 to both directions
        Volume step distribution:

        """
        current_volume = int(from_volume * 10)
        min_volume = 1
        max_volume = 9

        left_boundary = -abs(current_volume - min_volume)
        right_boundary = max_volume - current_volume

        if left_boundary < -2:
            left_boundary = -2

        if right_boundary > 2:
            right_boundary = 2

        new = current_volume + randrange(left_boundary, right_boundary, 1)
        print('P: {}, N: {}, L: {}, R: {}'.format(str(current_volume), str(new), str(left_boundary), str(right_boundary)))
        return new / 10

    def playlist(self, category):
        """ Create random loop """
        pass

    def list(self):
        for category in self.Category:
            print(category)
            print('---')
            for audio_name in sorted(self.Category[category]):
                print(' * {}'.format(audio_name))
        print('===')

    @staticmethod
    def volume(value):
         pygame.mixer.music.set_volume(value)
