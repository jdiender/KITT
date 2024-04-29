import serial
import keyboard
import time
import matplotlib.pyplot as plt #install with: pip install matplotlib
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
        
    def sensor_data(self):
        self.serial.write(b'Sd\n')
        data = self.serial.read_until(b'\x04').decode().strip()
        return float(data) if data.isdigit() else None
        
    def run_distance_measurement(self, target_distance):
        self.set_speed(160)  # Set speed for moving forward
        measurements = []
        try:
            while True:
                distance = float(self.sensor_data())  # Get distance measurement from sensor
                measurements.append((time.time(), distance))  # Log the time and distance
                if distance <= target_distance:
                    break  # Stop if close enough to the target distance
        finally:
            self.stop()  # Ensure KITT stops moving
            self.__del__() #break connection with KITT
            return measurements  # Return the collected measurements   
            
    def __del__(self):
        self.serial.close()
        
        
def plot_distance_vs_time(times, distances):
    # Normalize time data to start from zero
    start_time = times[0]
    times = [t - start_time for t in times]

    # Plotting the data
    plt.figure(figsize=(10, 5))
    plt.plot(times, distances, marker='o', linestyle='-', color='b')
    plt.title('Time vs. Distance Measurement of KITT')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Distance (cm)')
    plt.grid(True)
    plt.show()        
        
if __name__ == "__main__":
    kitt = KITT('COM3')
    target_distance = 50  # Set this to a safe distance in cm before hitting the wall
    data = kitt.run_distance_measurement(target_distance)

    # Extracting time and distance data
    times = [item[0] for item in data]
    distances = [item[1] for item in data]

    # Calling the plot function
    plot_distance_vs_time(times, distances)