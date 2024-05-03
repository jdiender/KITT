import pyaudio
import numpy as np
import matplotlib.pyplot as plt  # Import matplotlib for plotting
import keyboard

# Constants
FORMAT = pyaudio.paInt16
CHANNELS = 5
RATE = 48000  # Adjust as necessary
CHUNK = 1024000  # Number of audio samples per frame

# Initialize PyAudio
pyaudio_handle = pyaudio.PyAudio()s
for i in range(pyaudio_handle.get_device_count()):
    device_info = pyaudio_handle.get_device_info_by_index(i)
    print(i, device_info['name'])

# Open the stream
stream = pyaudio_handle.open(
    input=True,
    format=FORMAT,
    channels=CHANNELS,
    rate=RATE,
    frames_per_buffer=CHUNK
)

print("Recording...")

# Read the first chunk of audio data
samples = stream.read(CHUNK)
data = np.frombuffer(samples, dtype='int16')


if keyboard.read_key()=='s':   
# Close the stream
    stream.stop_stream()
    stream.close()
    pyaudio_handle.terminate()
    print("Recording stopped.")

# Assuming interlaced audio data for 5 channels
# Reshape the data into 5 separate streams
if data.shape[0] % CHANNELS == 0:
    reshaped_data = data.reshape(-1, CHANNELS)
    channel_data = [reshaped_data[:, i] for i in range(CHANNELS)]
else:
    print("Error: The number of samples is not a multiple of the number of channels.")
# Processing or storing the channel data
for idx, channel_samples in enumerate(channel_data):
    print(f"Data from microphone {idx + 1}: {channel_samples[:10]}...")  # Print first 10 samples

# Plotting the data for each channel
plt.figure(figsize=(15, 10))  # Set the figure size
for i in range(CHANNELS):
    plt.subplot(CHANNELS, 1, i + 1)  # Create a subplot for each channel
    plt.plot(channel_data[i])
    plt.title(f'Channel {i + 1}')
    plt.xlabel('Sample Number')
    plt.ylabel('Amplitude')
plt.tight_layout()  # Adjust subplots to fit into figure areas
plt.show()