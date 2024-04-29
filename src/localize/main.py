from scipy.io import wavfile
from defsignal import defsignal

import sys
import os

import numpy as np


def main() -> int:
    # 5 cm
    _, audio = wavfile.read('../../recordings/Recording-7-real-5cm.wav')
    y = (defsignal(audio[:, 0]), defsignal(audio[:, 1]))
    print(f"INFO: distance: {y[0].calculate_distance(y[1])} meter")

    # 1 m
    _, audio = wavfile.read('../../recordings/Recording-7-real-1m.wav')
    y = (defsignal(audio[:, 0]), defsignal(audio[:, 1]))
    print(f'INFO: distance: {y[0].calculate_distance(y[1])} meter')

    # x = 64 cm, y = 40 cm
    _, audio = wavfile.read('../../recordings/record_x64_y40.wav')
    y = (defsignal(audio[:, 1]), defsignal(audio[:, 4]))
    print(f'INFO: distance: {y[0].calculate_distance(y[1])} meter')

    # load all recordings
    recordings = []
    for path, _, files in os.walk('../../recordings'):
        for recording_name in files:
            recording_name: str = os.path.join(path, recording_name)
            recordings.append(recording_name)
            print(f'INFO: loaded {recording_name}')

    # process all recordings
    _, reference_channels = wavfile.read('../../recordings/reference.wav')
    for recording_name in recordings:
        _, recording_channels = wavfile.read(recording_name)
        for (idx, ref) in enumerate(reference_channels.T):
            for (jdx, rec) in enumerate(recording_channels.T):
                distance = defsignal(ref).calculate_distance(rec)
                print(f'INFO: recording({recording_name}): ', end='')
                print(f'reference({idx}): channel({jdx}): ', end='')
                print(f'distance: {distance} meter')

    return 0


if __name__ == '__main__':
    sys.exit(main())
