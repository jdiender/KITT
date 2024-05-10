import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, ifft
from scipy.signal import convolve, unit_impulse
from scipy.signal import find_peaks
from scipy.linalg import pinv
# Assuming task1 and functions are custom modules you've created
from task1 import h, ch3
from functions import calculate_distances_for_channel_pairs, load

# Constants
Fs_RX = 44100  # Sampling frequency

# Load reference signal
sample_rate_ref, reference_signal = wavfile.read(r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\reference.wav")

# Microphone coordinates
mic_x_coordinates = np.array([0, 0, 4.8, 4.8, 0])
mic_y_coordinates = np.array([0, 4.8, 4.8, 0, 2.4])

# Calculate distances between microphone pairs
mic_pair_distances = calculate_distances_for_channel_pairs(load(1, -1))

# Generate pairs and their x, y differences
mic_pairs = []
for j in range(5):
    for k in range(j + 1, 5):
        x_diff = mic_x_coordinates[k] - mic_x_coordinates[j]
        y_diff = mic_y_coordinates[k] - mic_y_coordinates[j]
        mic_pairs.append((j + 1, k + 1, x_diff, y_diff))

# Construct matrix A based on microphone pairs and distances
matrix_A = []
for i in range(10):
    row = [2 * (mic_pairs[i][2]), 2 * (mic_pairs[i][3])] + [0] * 4
    row[mic_pair_distances[i][1]] = -2 * mic_pair_distances[i][2]
    matrix_A.append(row)

# Construct matrix B (right-hand side)
matrix_B = []
for i in range(10):
    r_squared = mic_pair_distances[i][2]**2
    x_left = (mic_x_coordinates[mic_pair_distances[i][0]-1]**2 + mic_y_coordinates[mic_pair_distances[i][0]-1]**2)
    x_right = (mic_x_coordinates[mic_pair_distances[i][1]-1]**2 + mic_y_coordinates[mic_pair_distances[i][1]-1]**2)
    value = r_squared - x_left + x_right
    matrix_B.append(value)

# Convert lists to numpy arrays
A = np.array(matrix_A)
B = np.array(matrix_B).reshape(-1, 1)

# Solve for Y using the pseudo-inverse of A
Y = np.matmul(np.linalg.pinv(A), B)

# Output the result
print("Estimated Parameters:", Y)