#!/usr/bin/env python3
# coding=utf-8

from glob import glob
import pygame
from random import randrange
import time


class Player(object):

    Category = {
        'ambient': list(),
        'speech': list(),
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
        # NOTE: There must be at least 2 tracks in the category
        random_track = randrange(0, len(self.Category[category]), 1)
        return self.Category[category][random_track]

    def play_track(self, track_name, set_volume=None):
        """ Start track playback in the background and return control back to Player """

        # Load track
        pygame.mixer.music.load('{}/{}'.format(self.audio_path, track_name))

        # Set volume of the track
        if set_volume is not None:
            self.volume(set_volume)
        else:
            self.volume(self.current_volume)

        # Play track
        pygame.mixer.music.play()

        return None

    def partytime(self, show_lenght, scene_probability=4):

        """ Play ambient tracks for the specified length """

        # Start time
        show_start = time.time()

        # Play ambient
        while time.time() - show_start < show_lenght:

            # Get and play randomly chosen track from 'ambient' category
            self.play_track(self.get_track('ambient'), set_volume=self.current_volume)

            # Tweak the track volume during playtime
            self.animate_track(change_period=15)

            # Window of the opportunity for scenic sample (1/5)
            if len(self.Category['scene']) > 0:
                # Test if 'scene' should be played
                if randrange(1, 5, 1) > scene_probability:
                    # Play random scenic sample
                    self.play_track(self.get_track('scene'), set_volume=self.default_volume)
                    self.wait_for_end_of_track()

        return None

    def animate_track(self, change_period=5):
        """ While the track is playing, make subtle changes to it's amplitude """
        # Set the timer
        timer = time.time()

        # Loop while the track is playing
        # print('Animating')
        while pygame.mixer.music.get_busy():

            # When the timer expire, roll the Fake Dice and tweak the volume
            if time.time() - timer > change_period:

                # print('Changing')
                new_volume = self.roll_fake_dice()
                self.volume(new_volume)
                self.current_volume = new_volume

                # Reset the timer
                timer = time.time()

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

    def roll_fake_dice(self):
        """
        Volume range: 0..1
        Volume step: 0.2 to both directions
        Volume step distribution:

        """
        current_volume = int(self.current_volume * 10)
        min_volume = 1
        max_volume = 9

        # 1: 1-1=0
        # 2: 2-1=-1
        # 3: 3-1=-2
        # 5: 5-1=-4
        # 8: 8-1=-7
        # 9: 9-1=-8
        left_boundary = -abs(current_volume - min_volume)

        # 1: 9-1=8
        # 2: 9-2=7
        # 6: 9-6=3
        # 7: 9-7=2
        # 8: 9-8=1
        # 9: 9-9=0
        right_boundary = max_volume - current_volume

        if left_boundary < -3:
            left_boundary = -3

        if right_boundary > 3:
            right_boundary = 3

        new = current_volume + randrange(left_boundary, right_boundary, 1)
        # print('FakeDice: {}->{}, ({}, {})'.format(str(current_volume), str(new), str(left_boundary), str(right_boundary)))
        return new / 10

    def volume(self, set_volume, step_delay=0.3):
        """ Linear transition to new volume """

        v_current = int(self.current_volume * 10)
        v_requested = int(set_volume * 10)
        # print('---')
        # print('Volume request: C={} | R={}'.format(str(v_current), str(v_requested)))

        if v_current == v_requested:
            # Volume remains the same
            # print(' - Volume remains the same.')
            pass
        elif abs(v_current - v_requested) == 1:
            # Only changing one level, no need to iterate
            # print(' - Changing one step, no iterations')
            pygame.mixer.music.set_volume(set_volume)
        else:
            # Set boundaries
            start = v_current
            stop = v_requested

            # Recalculate the steps based on the 'direction'
            if start > stop:
                # Going down
                # print('DOWN')
                start -= 1
                stop -= 1
                step = -1
            else:
                # Going up
                # print('UP')
                start += 1
                stop += 1
                step = 1

            # print('Changing: start={}, stop={}'.format(str(start), str(stop)))
            for volume_step in range(start, stop, step):
                # print(' - {}'.format(str(volume_step / 10)))
                pygame.mixer.music.set_volume(volume_step / 10)
                time.sleep(step_delay)

        # print('===')


    @staticmethod
    def wait_for_end_of_track():
        """ Only wait for track to end and simply return control afterwards """
        while pygame.mixer.music.get_busy():
            pass
        return None

    def list(self):
        for category in self.Category:
            print(category)
            print('---')
            for audio_name in sorted(self.Category[category]):
                print(' * {}'.format(audio_name))
        print('===')
