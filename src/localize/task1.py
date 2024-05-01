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
audio_sliced = [
    [],
    [],
    [],
    [],
    []
]
audio_sliced[0] = data[0][4000:14000, 0]
audio_sliced[1] = data[0][4000:14000, 1]
audio_sliced[2] = data[0][4000:14000, 2]
audio_sliced[3] = data[0][4000:14000, 3]
audio_sliced[4] = data[0][4000:14000, 4]

for i in range(len(audio_sliced)):
    plt.title(f'record {i}')
    plt.plot(audio_sliced[i])
    plt.show()
