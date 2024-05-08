import serial
import keyboard
import time
import pyaudio
import numpy as np
import matplotlib.pyplot as plt
class KITT:
    def __init__(self, port, baudrate=115200):
        self.serial = serial.Serial(port, baudrate, rtscts=True)
        self.speed = 150
        self.angle = 150
        self.carrier_frequency = (5000).to_bytes(2, byteorder='big')
        self.bit_frequency = (2500).to_bytes(2, byteorder='big')
        self.repetition_count = (1250).to_bytes(2, byteorder='big')
        self.code = 0xDEADBEEF.to_bytes(4, byteorder='big')
        # state variables such as speed, angle are defined here
    def send_command(self, command):
        self.serial.write(command.encode())
    
    def set_speed(self, speed):
        self.speed = speed #set speed
        self.send_command(f'M{speed}\n')
    
    def set_angle(self, angle):
        self.angle = angle #set angle
        self.send_command(f'D{angle}\n')
        
    def set_audio_beacon_on(self):
        self.send_command(f'A1''\n')
        self.serial.write(b'F' + self.carrier_frequency + b'\n')
        self.serial.write(b'B' + self.bit_frequency + b'\n')
        self.serial.write(b'R' + self.repetition_count + b'\n')
        self.serial.write(b'C' + self.code + b'\n')
        
    def set_audio_beacon_off(self):
        self.send_command(f'A0''\n')

    def stop(self):
        self.set_speed(150)
        self.set_angle(150)
        self.send_command('R')
        
    def emergency_brake(self):
        current_speed=self.speed
        if(current_speed>150):
            self.set_speed(135)
            time.sleep(0.5)  # Brake for 1 second
            self.set_speed(150)   
        elif(current_speed<150):
            self.set_speed(165)
            time.sleep(0.3)  # Brake for 1 second
            self.set_speed(150) 
        else: 
            self.set_speed(150) 
    
    def record(self):
        # Constants
        FORMAT = pyaudio.paInt16
        CHANNELS = 5
        RATE = 48000  # Adjust as necessary
        CHUNK = 102400  # Number of audio samples per frame
        self.set_audio_beacon_on()
        
        # Initialize PyAudio
        pyaudio_handle = pyaudio.PyAudio()
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

        stream.stop_stream()
        stream.close()
        pyaudio_handle.terminate()
        print("Recording stopped.")
        self.set_audio_beacon_off()
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


    def __del__(self):
        self.serial.close()
        
def wasd(kitt):
    try:
        while True:
            key = keyboard.read_key()
            if key == 'w': #Forward
                kitt.set_speed(160)
            elif key == 'q': #Stop
                kitt.stop()
            elif key == 'a': #left
                kitt.set_angle(200)
            elif key == 's': #straight
                kitt.set_angle(150)
            elif key == 'd': #right
                kitt.set_angle(100)
            elif key == 'z':#Backwards 
                kitt.set_speed(138)
            elif key == 'e':#Brakes and goes opposite direction for a while
                kitt.emergency_brake()
            elif key == 'p':#Play audio beacon
                kitt.set_audio_beacon_on()
            elif key == 'o':#Turn audio beacon off
                kitt.set_audio_beacon_off()
            elif key == 'l':
                kitt.record()
            elif key == 'x':
                break  # Exit loop
    finally:
        kitt.stop()
        if kitt.serial:
            kitt.serial.close()      
        
if __name__ == "__main__":
    kitt = KITT('COM3')
    wasd(kitt)
    kitt.serial.close()
    #use kitt.record for audio
    #use wasd to steer kitt