from os import path
import wave
import struct

STRUCT_FORMAT_STRINGS = {
    1: 'b',
    2: 'h',
    4: 'l'
}

def parse_file(fn, channel):
    """ Parse an audio file and return a (width, samples) tuple. """
    _, ext = path.splitext(fn)
    if ext == '.wav':
        wav = wave.open(fn, 'rb')
        rate = wav.getframerate()
        width = wav.getsampwidth()
        channels = wav.getnchannels()

        data = wav.readframes(wav.getnframes())
        samples = []
        for i in range(channel * width, len(data), channels * width):
            samples.append(struct.unpack('<' + STRUCT_FORMAT_STRINGS[width], data[i:i + width])[0])
            
        return rate, width, data
    raise ValueError('Unknown input format: {}'.format(ext))

def write_snt(fn, width, samples):
    """ Write a SNT file containing the given samples. """
