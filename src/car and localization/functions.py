import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, ifft

mic_xcoordinates = np.array([0, 0, 4.6, 4.6, 0])
mic_ycoordinates = np.array([0, 4.6, 4.6, 0, 2.3])
#mic_zcoordinates = np.array([0.50, 0.50, 0.50, 0.50, 0.8])-0.27
mic_zcoordinates = np.array([0.0, 0.0, 0.0, 0.0, 0.0])
def locate(recording):
    # calculate TDOA pairs in distance
    r_ij = calculate_distances_for_channel_pairs(recording)
    
    pair = []
    x_temp = np.zeros(len(r_ij))
    for j in range(5):
        for k in range(j+1,5):
                #for i in range(len(r_ij)):
                x_temp = mic_xcoordinates[k] - mic_xcoordinates[j]
                y_temp = mic_ycoordinates[k] - mic_ycoordinates[j]
                z_temp = mic_zcoordinates[k] - mic_zcoordinates[j]
                pair.append((j+1,k+1,x_temp,y_temp,z_temp))
    
    # Assuming r_ij is a 1D array with the distances for each pair in the same order as 'pair'
    # Initialize an empty list to hold the rows of the new matrix
    matrix = []
    for i in range(10):
        row = [2*(pair[i][2]), 2*(pair[i][3]), 2*pair[i][4]] + [0] * 4
        row[r_ij[i][1]] = -2 * r_ij[i][2]
        matrix.append(row)

    # righthand-side of the matrix
    matrix2 = []
    for i in range(10):
        r = r_ij[i][2]**2
        x_left = (mic_xcoordinates[r_ij[i][0]-1]**2 + mic_ycoordinates[r_ij[i][0]-1]**2 + mic_zcoordinates[r_ij[i][0]-1]**2)
        x_right = (mic_xcoordinates[r_ij[i][1]-1]**2 + mic_ycoordinates[r_ij[i][1]-1]**2 + mic_zcoordinates[r_ij[i][1]-1]**2)
        value = r - x_left + x_right
        matrix2.append(value)
    
    A = np.array(matrix)
    B = np.array(matrix2).reshape(-1, 1)

    Y = np.matmul(np.linalg.pinv(A), B)

    return Y

def calculate_distances_for_channel_pairs(channels):
    # load reference channel
    _, ref = wavfile.read(r"C:\Users\julie\Documents\TU\Y2 23-24\EPO4Git\KITT\ref1.wav")
    ref = ref[48000:56000]
    plt.plot(ref)
    plt.show()
    # crop channels in paramater `channels`
    cropped_channels = crop_channels(channels)

    # calculate impulse response for each channel
    h = []
    for i in range(5):
        hi=abs(ch3(cropped_channels[i], ref, 0.01))
        h.append(hi)

    TDOA = []
    for i in range(5):
        for j in range(i + 1, 5):  # Ensure pairs are unique and not repeated
            h0 = h[i]
            h1 = h[j]            
            dist = calc_distance(h0, h1)
            TDOA.append((i+1, j+1, dist))
            #print(f"TDOA from microphone {i+1} to microphone {j+1}: {dist} meter")
    return TDOA

def crop_channels(channels):
    width = 10000
    channels = [
        channels[0],
        channels[1],
        channels[2],
        channels[3],
        channels[4]
    ]
    base_channel = channels[0] # determine the same offset for all channels
    base_channel_tmp = base_channel[int(len(base_channel)/2):] # temporarily take the right part of the channel to avoid false peaks
    base_peak = np.argmax(np.abs(base_channel_tmp)) + len(base_channel_tmp) # determine the midpoint of all channels
    left_index = base_peak - width # offset from left
    right_index = base_peak + width # offset from right

    # fill cropped_channels with each individual channel of the corresponding recording
    cropped_channels = []
    for j in range(5):
        cropped_channels.append(channels[j][left_index:right_index]) # gets emptied after out of scope
    return cropped_channels

Fs_RX = 44100
def calc_distance(h0, h1):
  return (np.argmax(h0) - np.argmax(h1)) / Fs_RX * 343

def ch3(x,y,epsi):
    Nx = len(x) # Length of x
    Ny = len(y) # Length of y
    Nh = Ny - Nx + 1 # Length of h

    # Force x to be the same length as y
    if Nx < Ny: 
        x = np.pad(x, (0, Ny - Nx))
    else:
        y = np.pad(y, (0, Nx - Ny))
    
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

def load(recording_number, channel_number):
    audio_array=[r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\record_x64_y40.wav",
            r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\record_x82_y399.wav",
             r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\record_x109_y76.wav",
             r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\record_x143_y296.wav",
             r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\record_x150_y185.wav",
             r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\record_x178_y439.wav",
             r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\record_x232_y275.wav"]
    recording_name = audio_array[recording_number - 1]
    _, recording = wavfile.read(recording_name)
    if channel_number == -1:
        return [
            recording[:, 0],
            recording[:, 1],
            recording[:, 2],
            recording[:, 3],
            recording[:, 4]
        ]
    else:
        return recording[:, channel_number - 1]

def crop(recording):
    width = 10000
    recording = recording
    recording_tmp = recording[int(len(recording)/2):]
    peak = np.argmax(np.abs(recording_tmp)) + len(recording_tmp) 
    recording = recording[peak-width:peak+width]
    return recording
