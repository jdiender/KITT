import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, ifft
from scipy.signal import convolve, unit_impulse
from scipy.signal import find_peaks

# from refsignal import refsignal            # model for the EPO4 audio beacon signal
# from wavaudioread import wavaudioread
# from recording_tool import recording_tool
Fs_RX = 44100

def ch3(x,y,epsi):
    Nx = len(x) # Length of x
    Ny = len(y) # Length of y
    Nh = Ny - Nx + 1 # Length of h

    # Force x to be the same length as y
    x = np.pad(x, (0, Ny - Nx))

    # Deconvolution in frequency domain
    X = fft(x)
    Y = fft(y)
    #if X is not 0:
    H = Y / X
    #else:
     # H = 0
    # Threshold to avoid blow ups of noise during inversion
    ii = np.absolute(X) < epsi * max(np.absolute(X))
    # for idx in range(len(ii)):
    #     if ii[idx] is False:
    #         H[idx] = 0
    H[ii] = 0

    h = np.real(ifft(H))    # ensure the result is real
    #h = h[:Lhat]    # optional: truncate to length Lhat (L is not reliable?)
    return h

sampled_rate2,ref=wavfile.read(r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\reference.wav")
audio_files = {
    "file1": r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\record_x64_y40.wav",
    "file2": r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\record_x82_y399.wav",
    "file3": r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\record_x109_y76.wav",
    "file4": r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\record_x143_y296.wav",
    "file5": r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\record_x150_y185.wav",
    "file6": r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\record_x178_y439.wav",
    "file7": r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\record_x232_y275.wav"
    # Add more files as needed
}
audio_array=[r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\record_x64_y40.wav",
            r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\record_x82_y399.wav",
             r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\record_x109_y76.wav",
             r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\record_x143_y296.wav",
             r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\record_x150_y185.wav",
             r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\record_x178_y439.wav",
             r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\record_x232_y275.wav"]
audio_data = {}
data = []

#print("audio array is ",audio_array[1])
# Loop through each file path in the audio_files dictionary
for file_path in audio_files.values():
    # Read the audio file
    rate, audio_data = wavfile.read(file_path)
    # Append the tuple of (rate, audio_data) to the list
    data.append(( audio_data))


def calc_distance(h0, h1):
  return abs(np.argmax(h0) - np.argmax(h1)) / Fs_RX * 343

peaks1 = find_peaks(audio_data[40000:65000,0], height=[100,])[0]
print("PEAK IS", peaks1[0])
plt.plot(audio_data[:,0])
plt.show()

for k in range(7):
    print("audio file",k)
    for j in range(audio_data.shape[1]):
        print("For reference sample", j)
        for i in range(audio_data.shape[1]):
            h0 = ch3(data[k][:, i], ref[:, j], 0.01)
            h1 = ch3(ref[:, j],ref[:, j],0.01)
            dist = calc_distance(h1, h0)
            print("Distance from microphone", i, "to beacon :", dist, "meters")

