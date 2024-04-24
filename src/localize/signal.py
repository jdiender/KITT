import numpy as np;

@dataclass
class signal:
    epsi = 0.01
    fs_rx = 10e3 # TODO: what sampling frequency is required by specs?

    def __init__(self, signal):
        self.signal = signal

    def channel(self, y):
        x = self.signal
        y = y

        Nx = len(x)
        Ny = len(y)
        Nh = Ny - Nx + 1

        # Force x to be the same length as y
        x = np.pad(x, (0, Ny - Nx))

        # Deconvolution in the frequency domain.
        X = fft(x)
        Y = fft(y)

        H = Y / X

        # Threshold to avoid blow ups of noise during inversion.
        ii = np.absolute(X) < epsi * max(np.absolute(X))
        for idx in range(len(ii)):
            if ii[idx] is False:
                H[idx] = 0

        # Ensure the result is real.
        h = np.real(ifft(H))

        # Return calculated impulse response.
        return h

    def calculate_distance(self, h):
        h0 = self.channel(self.signal, h)
        h1 = self.channel(self.signal, self.signal)

        distance = abs(np.argmax(h0) - np.argmax(h1)) / fs_rx * 343
        return distance
