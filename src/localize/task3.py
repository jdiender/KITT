import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, ifft
from scipy.signal import convolve, unit_impulse
from scipy.signal import find_peaks
from functions import load, crop, ch3, calc_distance

#from task1 import h
from task1 import ch3
Fs_RX = 44100
sampled_rate2,ref=wavfile.read(r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\reference.wav")

width = 10000
cropped_channels_per_recording = []
for i in range(7):
    channel = [
        load(i+1, 1),
        load(i+1, 2),
        load(i+1, 3),
        load(i+1, 4),
        load(i+1, 5)
    ]
    base_channel = load(i+1, 1) # determine the same offset for all channels
    base_channel_tmp = base_channel[int(len(base_channel)/2):] # temporarily take the right part of the channel to avoid false peaks
    base_peak = np.argmax(np.abs(base_channel_tmp)) + len(base_channel_tmp) # determine the midpoint of all channels
    left_index = base_peak - width # offset from left
    right_index = base_peak + width # offset from right

    # fill cropped_channels with each individual channel of the corresponding recording
    cropped_channels = []
    for j in range(5):
        cropped_channels.append(channel[j][left_index:right_index]) # gets emptied after out of scope

    cropped_channels_per_recording.append(cropped_channels) # in order to retain the cropped channels for all recordings

# 
# for cropped_chan in cropped_channels:
#     plt.plot(cropped_chan)
#     peak2 = np.argmax(np.abs(cropped_chan))
#     plt.plot(peak2,cropped_chan[peak2],'ro')
#     plt.show()

uncropped_channels = [
    load(1,1),
    load(1,2),
    load(1,3),
    load(1,4),
    load(1,4)
]

cropped_channels = cropped_channels_per_recording[0]
h = []
# absolute value of impulse response determined for recording 1 for all 5 channels
for i in range(5):
    hi=abs(ch3(cropped_channels[i],ref[120000:150000,0],0.01))
    h.append(hi)
# used to fill the TDOA matrix in order to see time difference of arrival between all microphones
def calculate_distances_for_channel_pairs():
    TDOA = []
    for i in range(5):
        for j in range(i + 1, 5):  # Ensure pairs are unique and not repeated
            h0 = h[i]
            h1 = h[j]            
            time = calc_distance(h1, h0)
            TDOA.append((i, j, time))
            print(f"TDOA from microphone {i} to microphone {j}: {time} meter")
    return TDOA

calculate_distances_for_channel_pairs()
