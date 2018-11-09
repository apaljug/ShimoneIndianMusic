#! /usr/env python

from aubio import source, tempo
from numpy import median, diff
import sox
from pydub import AudioSegment

def mp3towav(src):
    dst = "{}.wav".format(src[:-4])
    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format= "wav")
    return dst

def bandreject_filter(path, num):
    """ filter file using band reject
        rejecting range from 100 to 10000
    """
    dst = "{}filter.wav".format(path)


    tfm = sox.Transformer()
    tfm.loudness(10,50)
    if num == 0:
        tfm.bandreject(4600 ,4500)
        tfm.highpass(10000,10,1)
        tfm.lowpass(100,10,1)
    elif num == 1:
        tfm.highpass(10000,10,1)
    elif num == 2:
        tfm.lowpass(100,10,1)
    elif num == 3:
        tfm.bandreject(4600 ,4500)
    tfm.build("{0}.wav".format(path) , dst)

def get_file_bpm(path, params=None):
    """ Calculate the beats per minute (bpm) of a given file.
        path: path to the file
        param: dictionary of parameters
    """
    if params is None:
        params = {}
    # default:
    samplerate, win_s, hop_s = 4000, 128, 64
    if 'mode' in params:
        if params.mode in ['super-fast']:
            # super fast
            samplerate, win_s, hop_s = 4000, 128, 64
        elif params.mode in ['fast']:
            # fast
            samplerate, win_s, hop_s = 8000, 512, 128
        elif params.mode in ['slow']:
            # slow
            samplerate, win_s, hop_s = 44100, 1024, 512
        elif params.mode in ['default']:
            pass
        else:
            raise ValueError("unknown mode {:s}".format(params.mode))
    if 'filter' in params:
        if "mp3" in path:
            path = mp3towav(path)
        if params.filter in ['all']:
            bandreject_filter(path[:-4],0)
            path = "{}filter.wav".format(path[:-4])
        elif params.filter in ['high']:
            bandreject_filter(path[:-4],1)
            path = "{}filter.wav".format(path[:-4])
        elif params.filter in ['low']:
            bandreject_filter(path[:-4],2)
            path = "{}filter.wav".format(path[:-4])
        elif params.filter in ['reject']:
            bandreject_filter(path[:-4],3)
            path = "{}filter.wav".format(path[:-4])
        else:
            raise ValueError("unknown mode {:s}".format(params.mode))

    if 'samplerate' in params:
        samplerate = params.samplerate
    if 'win_s' in params:
        win_s = params.win_s
    if 'hop_s' in params:
        hop_s = params.hop_s

    s = source(path, samplerate, hop_s)
    samplerate = s.samplerate
    o = tempo("specdiff", win_s, hop_s, samplerate)
    # List of beats, in samples
    beats = []
    # Total number of frames read
    total_frames = 0

    while True:
        samples, read = s()
        is_beat = o(samples)
        if is_beat:
            this_beat = o.get_last_s()
            beats.append(this_beat)
        total_frames += read
        if read < hop_s:
            break

    def beats_to_bpm(beats, path):
        # if enough beats are found, convert to periods then to bpm
        if len(beats) > 1:
            if len(beats) < 4:
                print("few beats found in {:s}".format(path))
            bpms = 60./diff(beats)
            return median(bpms)
        else:
            print("not enough beats found in {:s}".format(path))
            return 0

    return beats_to_bpm(beats, path)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode',
            help="mode [default|fast|super-fast]",
            dest="mode", default='fast')
    parser.add_argument('-f', '--filter',
            help="filter [all|reject|low|high]",
            dest="filter", default='reject')
    parser.add_argument('sources',
            nargs='+',
            help="input_files")
    args = parser.parse_args()
    for f in args.sources:
        bpm = get_file_bpm(f, params = args)
        if "filter" in args:
            f = "{}filter.wav".format(f[:-4])
        print("{:6s} {:s}".format("{:2f}".format(bpm), f))
