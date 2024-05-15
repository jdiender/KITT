import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, ifft
from scipy.signal import convolve, unit_impulse

# Coordinates of microphones and recording locations
mic_xcoordinates = np.array([0, 4.80, 4.80, 0, 0])
mic_ycoordinates = np.array([0, 0, 4.80, 4.80, 2.40])
rec_xcoordinates = np.array([0.64, 0.82, 1.09, 1.43, 1.50, 1.78, 2.32])
rec_ycoordinates = np.array([0.40, 3.99, 0.76, 2.96, 1.85, 4.39, 2.75])

# Calculate distances
distances = np.zeros((len(mic_xcoordinates), len(rec_xcoordinates)))

for i in range(len(mic_xcoordinates)):
    for j in range(len(rec_xcoordinates)):
        distances[i, j] = np.sqrt((mic_xcoordinates[i] - rec_xcoordinates[j])**2 + (mic_ycoordinates[i] - rec_ycoordinates[j])**2)

# Print distances
# for i in range(len(mic_xcoordinates)):
#     print(f"Distances to Microphone {i+1}:")
#     for j in range(len(rec_xcoordinates)):
#         print(f"Recording {j+1}: {distances[i, j]:.2f} meters")
#     print()  # Blank line for readability

# Print distances from each microphone to Recording 1
for i in range(len(mic_xcoordinates)):
    print(f"Distance from Microphone {i+1} to Recording 1: {distances[i, 6]:.2f} meters")

# enes->1; naufal->5
# enes->2; naufal->2/3
# enes->3; naufal->1
# enes->4; naufal->2/3
# enes->5; naufal->4
# Given beacon at location 0.64; 0.40
beacon_x = 0.64
beacon_y = 0.40

# Calculate distances to the beacon
distances_to_beacon = np.zeros((len(mic_xcoordinates), 1))

for i in range(len(mic_xcoordinates)):
    distances_to_beacon[i] = np.sqrt((mic_xcoordinates[i] - beacon_x)**2 + (mic_ycoordinates[i] - beacon_y)**2)

for i in range(5):
    for j in range (i+1, 5):
        print(f"Distance from Microphone {i+1} to Microphone {j+1}: {distances_to_beacon[i]-distances_to_beacon[j]:.2f} meters")

    print()  # Blank line for readability