import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, ifft
from scipy.signal import convolve, unit_impulse
from scipy.signal import find_peaks
from scipy.linalg import pinv
from task1 import h
from task1 import ch3
from functions import  calculate_distances_for_channel_pairs
from functions import load, locate

Fs_RX = 44100
sampled_rate2,ref=wavfile.read(r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\reference.wav")


mic_xcoordinates = np.array([0, 0, 4.8, 4.8, 0])
mic_ycoordinates = np.array([0, 4.8, 4.8, 0, 2.4])
mic_zcoordinates = np.array([0.50, 0.50, 0.50, 0.50, 0.8])

#r_ij = calculate_distances_for_channel_pairs(load(4,-1))

recording_x = np.array([0.64, 0.82, 1.09, 1.43, 1.50, 1.78, 2.32,0,0,0,0])
recording_y = np.array([0.40, 3.99 ,0.76, 2.96, 1.85, 4.93, 2.75,0,0,0,0])

for z in range(7):
    r_ij = calculate_distances_for_channel_pairs(load(z+1,-1))
    pair = []
    x_temp = np.zeros(len(r_ij))
    for j in range(5):
        for k in range(j+1,5):
                #for i in range(len(r_ij)):
                x_temp = mic_xcoordinates[k] - mic_xcoordinates[j]
                y_temp = mic_ycoordinates[k] - mic_ycoordinates[j]
                pair.append((j+1,k+1,x_temp,y_temp))


    # Assuming r_ij is a 1D array with the distances for each pair in the same order as 'pair'
    # Initialize an empty list to hold the rows of the new matrix
    matrix = []
    for i in range(10):
        row = [2*(pair[i][2]), 2*(pair[i][3])] + [0] * 4
        row[r_ij[i][1]] = -2 * r_ij[i][2]
        matrix.append(row)
    #print(matrix)

    # righthand-side
    matrix2 = []
    for i in range(10):
        r = r_ij[i][2]**2
        x_left = (mic_xcoordinates[r_ij[i][0]-1]**2 + mic_ycoordinates[r_ij[i][0]-1]**2)
        x_right = (mic_xcoordinates[r_ij[i][1]-1]**2 + mic_ycoordinates[r_ij[i][1]-1]**2 )
        value = r - x_left + x_right
        #print(x_left)
        matrix2.append(value)
    #print(matrix2)

    A = np.array(matrix)
    B = np.array(matrix2).reshape(-1, 1)

    Y = np.matmul(np.linalg.pinv(A), B)
    #print("DISTANCES ARE ", Y[0]-recording_x[z], Y[1]-recording_y[z])
    # print(np.array(r_ij))
    # print()

print(locate(
     load(2, -1)
))