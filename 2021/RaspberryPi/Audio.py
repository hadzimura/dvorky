from glob import glob
import pygame


class Samples(object):

    def __init__(self, audio_path=None):
        pygame.mixer.init()
        pygame.mixer.music.set_volume(1)
        files = glob(audio_path + '*.mp3')
        for p in files:
            print('{}'.format(p))
            pygame.mixer.music.load(p)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue

