from glob import glob
from playsound import playsound

playsound('myfile.wav')


class Samples(object):

    def __init__(self, audio_path=None):
        files = glob(audio_path + '*.wav')
        for p in files:
            print('{}'.format(p))
            playsound(p)
