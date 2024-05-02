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
audio_sliced0[0] = data[0][40000:60000, 0]
audio_sliced0[1] = data[0][40000:60000, 1]
audio_sliced0[2] = data[0][40000:60000, 2]
audio_sliced0[3] = data[0][40000:60000, 3]
audio_sliced0[4] = data[0][40000:60000, 4]

# plt.plot(data[0])
# plt.show()



# for i in range(len(audio_sliced0)):
#     plt.title(f'record {i}')
#     plt.plot(audio_sliced0[i])
#     plt.show()

audio_sliced1 = [
    [],
    [],
    [],
    [],
    []
]


audio_sliced1[0] = data[1][40000:65000, 0]
audio_sliced1[1] = data[1][40000:65000, 1]
audio_sliced1[2] = data[1][40000:65000, 2]
audio_sliced1[3] = data[1][40000:65000, 3]
audio_sliced1[4] = data[1][40000:65000, 4]

# plt.plot(data[1])
# plt.show()



# for i in range(len(audio_sliced1)):
#     plt.title(f'record {i}')
#     plt.plot(audio_sliced1[i])
#     plt.show()

audio_sliced2 = [
    [],
    [],
    [],
    [],
    []
]

audio_sliced2[0] = data[2][85000:105000, 0]
audio_sliced2[1] = data[2][85000:105000, 1]
audio_sliced2[2] = data[2][85000:105000, 2]
audio_sliced2[3] = data[2][85000:105000, 3]
audio_sliced2[4] = data[2][85000:105000, 4]

# plt.plot(data[2])
# plt.show()



# for i in range(len(audio_sliced2)):
#     plt.title(f'record {i}')
#     plt.plot(audio_sliced2[i])
#     plt.show()

audio_sliced3 = [
    [],
    [],
    [],
    [],
    []
]

audio_sliced3[0] = data[3][65000:85000, 0]
audio_sliced3[1] = data[3][65000:85000, 1]
audio_sliced3[2] = data[3][65000:85000, 2]
audio_sliced3[3] = data[3][65000:85000, 3]
audio_sliced3[4] = data[3][65000:85000, 4]

# plt.plot(data[3])
# plt.show()



# for i in range(len(audio_sliced3)):
#     plt.title(f'record {i}')
#     plt.plot(audio_sliced3[i])
#     plt.show()
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

# plt.plot(data[3])
# plt.show()


# for i in range(len(audio_sliced4)):
#     plt.title(f'record {i}')
#     plt.plot(audio_sliced4[i])
#     plt.show()



audio_sliced5 = [
    [],
    [],
    [],
    [],
    []
]
audio_sliced5[0] = data[5][20000:38000, 0]
audio_sliced5[1] = data[5][20000:38000, 1]
audio_sliced5[2] = data[5][20000:38000, 2]
audio_sliced5[3] = data[5][20000:38000, 3]
audio_sliced5[4] = data[5][20000:38000, 4]

# plt.plot(data[5])
# plt.show()


# for i in range(len(audio_sliced5)):
#     plt.title(f'record {i}')
#     plt.plot(audio_sliced5[i])
#     plt.show()

audio_sliced6 = [
    [],
    [],
    [],
    [],
    []
]
audio_sliced6[0] = data[6][40000:62000, 0]
audio_sliced6[1] = data[6][40000:62000, 1]
audio_sliced6[2] = data[6][40000:62000, 2]
audio_sliced6[3] = data[6][40000:62000, 3]
audio_sliced6[4] = data[6][40000:62000, 4]

# plt.plot(data[6])
# plt.show()

# for i in range(len(audio_sliced6)):
#     plt.title(f'(enes) file7: record {i}')
#     plt.plot(audio_sliced6[i])
#     plt.show()
audio_sliced=[
    [audio_sliced0],
    [audio_sliced1],
    [audio_sliced2],
    [audio_sliced3],
    [audio_sliced4],
    [audio_sliced5],
    [audio_sliced6],

]
# Assuming audio_sliced is your list of recordings, each containing lists of channels
for i, recording in enumerate(audio_sliced):
    for j, channel in enumerate(recording[0]):  # Access the first (and only) item in each recording list, which contains the channels
        plt.figure(figsize=(10, 4))  # Optional: Set figure size
        plt.title(f'Recording {i+1}, Channel {j+1}')
        plt.plot(channel)
        plt.xlabel('Sample Index')
        plt.ylabel('Amplitude')
        plt.show()