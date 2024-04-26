from scipy.io import wavfile
from defsignal import defsignal

import sys


def main() -> int:
    # 5 cm
    _, audio = wavfile.read('../../recordings/Recording-7-real-5cm.wav')
    y5cm = (defsignal(audio[:, 0]), defsignal(audio[:, 1]))
    h5cm = (defsignal(y5cm[0].channel(y5cm[0])),
            defsignal(y5cm[1].channel(y5cm[0])))
    print(f"INFO: distance: {h5cm[0].calculate_distance(h5cm[1])}")

    # 1 m
    _, audio = wavfile.read('../../recordings/Recording-7-real-1m.wav')
    y1m = (defsignal(audio[:, 0]), defsignal(audio[:, 1]))
    h1m = (defsignal(y1m[0].channel(y1m[0])),
           defsignal(y1m[1].channel(y1m[0])))
    print(f"INFO: distance: {h1m[0].calculate_distance(h1m[1])}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
