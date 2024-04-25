from scipy.fft import fft, ifft
from dataclasses import dataclass;

import numpy as np;
import matplotlib.pyplot as plt;

@dataclass
class defsignal:
    __epsi = 0.01
    __fs_rx = 10e3 # TODO: what sampling frequency is required by specs?

    def __init__(self, y):
        while type(self) == type(y):
            y = y.signal
        assert y.ndim == 1, "ERROR: signal should be flat"
        self.signal = y

    def convolve(self, x):
        if type(x) == type(self):
            x = x.signal
        return np.convolve(self.signal, x)

    def channel(self, x):
        if type(x) == type(self):
            x = x.signal
        assert x.ndim == 1, "ERROR: signal should be flat"

        x = x
        y = self.signal

        Nx = x.size
        Ny = y.size

        # Force x to be the same length as y
        x = np.pad(x, (0, Ny - Nx))

        # Deconvolution in the frequency domain.
        X = fft(x)
        Y = fft(y)

        # `H = Y/X` only does not check for cases where `X == 0`.
        H = np.array([])
        for (y, x) in zip(Y, X):
            if x != 0:
                H = np.append(H, [y/x])
            else:
                H = np.append(H, [0])

        # Threshold to avoid blow ups of noise during inversion.
        ii = np.absolute(X) < self.__epsi * max(np.absolute(X))
        for idx in range(len(ii)):
            if ii[idx] is False:
                H[idx] = 0

        # Ensure the result is real.
        h = np.real(ifft(H))

        # Return the calculated impulse response.
        return h

    def calculate_distance(self, h):
        if type(h) == type(self):
            h = h.signal
        h0 = self.channel(h)
        h1 = self.channel(self.signal)
        distance = abs(np.argmax(h0) - np.argmax(h1)) / self.__fs_rx * 343
        return distance

    def naive_plot(self):
        y = self.signal
        plt.figure(figsize=(11,4))
        plt.title("?")
        plt.xlabel("? [?]")
        plt.ylabel("? [?]")
        plt.plot(y)
        plt.show()
