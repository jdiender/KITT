from defsignal import defsignal;

import sys;
import numpy as np;

def main() -> int:
    # Test your channel function here:
    # Channel
    h = np.array([1, 2, 3, 2, 1])
    # Lhat = 5  # Estimate of channel length L, but could be different.

    # Input length
    N = 20

    # Input: x1, x2, x3
    x1 = [0, -1, 0.5]
    x1 = defsignal(np.pad(x1, (0, N - len(x1))))

    omega = 0.5
    x2 = defsignal(np.cos(omega * np.arange(N)))

    x3 = defsignal(np.sign(np.random.rand(N)-0.5))

    ## Output: y1, y2, y3
    y1 = defsignal(x1.convolve(h))
    y2 = defsignal(x2.convolve(h))
    y3 = defsignal(x3.convolve(h))

    # Channel estimation via ch3: h1, h2, h3
    # suitable epsi: try values between 0.001 and 0.05
    epsi = 0.01

    print(type(x1))

    h1 = defsignal(defsignal(defsignal(y1.channel(x1))))
    h2 = y2.channel(x2)
    h3 = y3.channel(x3)

    # Print result, should give true channel (which is [1,2,3,2,1])
    print(h1)
    print(h2)
    print(h3)

    defsignal(h2).naive_plot()
    return 0;

if __name__ == "__main__":
    sys.exit(main())
