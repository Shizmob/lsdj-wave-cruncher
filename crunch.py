import sys
import argparse

from lib import format, pitch, transforms


def crunch(fn, frequency=None, channel=0, normalize=False, interpolate=None):
    rate, width, samples = format.parse_file(fn, channel)

    if frequency is None:
        frequency, probability = pitch.estimate_pitch(samples, rate=rate)
        if probability < 0.9:
            raise ValueError('Could not accurately determine frequency for {}'.format(fn))
    print(frequency)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="CRUNCH! I'll add it to the heap!")
    parser.add_argument('sample', metavar='SAMPLE.WAV', help='input sample')
    parser.add_argument('frequency', metavar='FREQUENCY', type=float, default=None, nargs='?', help='frequency')
    parser.add_argument('-c', '--channel', type=int, default=0, help='input channel to use')
    parser.add_argument('-n', '--normalize', action='store_true', default=False, help='normalize result')
    parser.add_argument('-i', '--interpolate', metavar='METHOD', default=None, help='interpolation method (linear, exponential)')
    args = parser.parse_args()

    try:
        crunch(args.sample, frequency=args.frequency, channel=args.channel, normalize=args.normalize, interpolate=args.interpolate)
    except ValueError as e:
        sys.exit(e)
