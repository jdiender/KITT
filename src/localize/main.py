from scipy.io import wavfile
from defsignal import defsignal

import sys


def main() -> int:
    fs, audio = wavfile.read('./Recording-7-real-1m.wav')

    y5cm_0 = defsignal(audio[:, 0])
    y5cm_1 = defsignal(audio[:, 1])

    h0 = defsignal(y5cm_0.channel(y5cm_0))
    h1 = defsignal(y5cm_1.channel(y5cm_0))

    print(h0.calculate_distance(h1))

    return 0


if __name__ == '__main__':
    sys.exit(main())
