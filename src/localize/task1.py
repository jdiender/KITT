import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, ifft
from scipy.signal import convolve, unit_impulse
from scipy.signal import find_peaks

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
    data.append((audio_data))
#slice audio data[0] only indices 40 till 60
audio_sliced0 = [
    [],
    [],
    [],
    [],
    []
]
audio_sliced0[0] = data[0][120000:150000, 0]
audio_sliced0[1] = data[0][120000:150000, 1]
audio_sliced0[2] = data[0][120000:150000, 2]
audio_sliced0[3] = data[0][120000:150000, 3]
audio_sliced0[4] = data[0][120000:150000, 4]


audio_sliced1 = [
    [],
    [],
    [],
    [],
    []
]


audio_sliced1[0] = data[1][120000:150000, 0]
audio_sliced1[1] = data[1][120000:150000, 1]
audio_sliced1[2] = data[1][120000:150000, 2]
audio_sliced1[3] = data[1][120000:150000, 3]
audio_sliced1[4] = data[1][120000:150000, 4]


audio_sliced2 = [
    [],
    [],
    [],
    [],
    []
]

audio_sliced2[0] = data[2][120000:150000, 0]
audio_sliced2[1] = data[2][120000:150000, 1]
audio_sliced2[2] = data[2][120000:150000, 2]
audio_sliced2[3] = data[2][120000:150000, 3]
audio_sliced2[4] = data[2][120000:150000, 4]

audio_sliced3 = [
    [],
    [],
    [],
    [],
    []
]

audio_sliced3[0] = data[3][120000:150000, 0]
audio_sliced3[1] = data[3][120000:150000, 1]
audio_sliced3[2] = data[3][120000:150000, 2]
audio_sliced3[3] = data[3][120000:150000, 3]
audio_sliced3[4] = data[3][120000:150000, 4]

audio_sliced4 = [
    [],
    [],
    [],
    [],
    []
]

audio_sliced4[0] = data[4][120000:150000, 0]
audio_sliced4[1] = data[4][120000:150000, 1]
audio_sliced4[2] = data[4][120000:150000, 2]
audio_sliced4[3] = data[4][120000:150000, 3]
audio_sliced4[4] = data[4][120000:150000, 4]




audio_sliced5 = [
    [],
    [],
    [],
    [],
    []
]
audio_sliced5[0] = data[5][120000:150000, 0]
audio_sliced5[1] = data[5][120000:150000, 1]
audio_sliced5[2] = data[5][120000:150000, 2]
audio_sliced5[3] = data[5][120000:150000, 3]
audio_sliced5[4] = data[5][120000:150000, 4]



audio_sliced6 = [
    [],
    [],
    [],
    [],
    []
]
audio_sliced6[0] = data[6][120000:150000, 0]
audio_sliced6[1] = data[6][120000:150000, 1]
audio_sliced6[2] = data[6][120000:150000, 2]
audio_sliced6[3] = data[6][120000:150000, 3]
audio_sliced6[4] = data[6][120000:150000, 4]


audio_sliced=[
    [audio_sliced0],
    [audio_sliced1],
    [audio_sliced2],
    [audio_sliced3],
    [audio_sliced4],
    [audio_sliced5],
    [audio_sliced6],

]
# # Assuming audio_sliced is your list of recordings, each containing lists of channels
# for i, recording in enumerate(audio_sliced):
#     for j, channel in enumerate(recording[0]):  # Access the first (and only) item in each recording list, which contains the channels
#         plt.figure(figsize=(10, 4))  # Optional: Set figure size
#         plt.title(f'Recording {i+1}, Channel {j+1}')
#         plt.plot(channel)
#         plt.xlabel('Sample Index')
#         plt.ylabel('Amplitude')
#         plt.show()

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

ref_sliced = ref[:,0]
h=[]
h1=ch3(audio_sliced0[1],ref[120000:150000,0],0.01)
for i in range(5):
    hi=ch3(audio_sliced0[i],ref[120000:150000,0],0.01)
    h.append(hi)
    plt.plot(abs(h[i]))
    plt.show()

