import serial
import keyboard
import time
import matplotlib.pyplot as plt # install with: pip install matplotlib

class KITT:
    def __init__(self, port, baudrate=115200):
        self.serial = serial.Serial(port, baudrate, rtscts=True)
        self.speed = 150
        self.angle = 150
        self.carrier_frequency = (5000).to_bytes(2, byteorder='big')
        self.bit_frequency = (2500).to_bytes(2, byteorder='big')
        self.repetition_count = (1250).to_bytes(2, byteorder='big')
        self.code = 0xDEADBEEF.to_bytes(4, byteorder='big')
        self.measurements = []
        # state variables such as speed, angle are defined here

    def send_command(self, command):
        self.serial.write(command.encode())

    def set_speed(self, speed):
        self.speed = speed  # set speed
        self.send_command(f'M{speed}\n')

    def set_angle(self, angle):
        self.angle = angle  # set angle
        self.send_command(f'D{angle}\n')

    def stop(self):
        self.set_speed(150)
        self.set_angle(150)
        self.send_command('R')

    def emergency_brake(self):
        current_speed = self.speed
        if current_speed > 150:
            self.set_speed(135)
            time.sleep(0.5)  # Brake for 0.5 seconds
            self.set_speed(150)
        elif current_speed < 150:
            self.set_speed(165)
            time.sleep(0.3)  # Brake for 0.3 seconds
            self.set_speed(150)
        else:
            self.set_speed(150)

    def sensor_data(self):
        self.serial.write(b'Sd\n')
        data = self.serial.read_until(b'\x04').decode()
        left_distance = int(data.split('USL')[1][:3])  # Separate the distance sensors for the left sensor. Assumes format USL###\n
        right_distance = int(data.split('USR')[1][:3])  # Separate the distance sensors for the right sensor. Assumes format USR###\n
        return left_distance, right_distance

    def __del__(self):
        self.serial.close()

    def run_distance_measurement(self):
        target_distance = 85  # Set this to a safe distance in cm before hitting the wall
        try:
            while True:
                left_distance, right_distance = self.sensor_data()
                current_time = time.time()
                self.measurements.append((current_time, left_distance, right_distance))  # Log the time and distance
                if target_distance >= left_distance:
                    self.emergency_brake()
                    break  # Stop if close enough to the target distance
                elif target_distance >= right_distance:
                    self.emergency_brake()
                    break
                else:
                    self.set_speed(160)
        finally:
            self.__del__()  # break connection with KITT
            return self.measurements  # Return the collected measurements

def calculate_velocity(measurements):
    velocities = []
    for i in range(1, len(measurements)):
        time_diff = measurements[i][0] - measurements[i-1][0]
        left_distance_diff = measurements[i][1] - measurements[i-1][1]
        right_distance_diff = measurements[i][2] - measurements[i-1][2]
        left_velocity = left_distance_diff / time_diff if time_diff != 0 else 0
        right_velocity = right_distance_diff / time_diff if time_diff != 0 else 0
        velocities.append((measurements[i][0], left_velocity, right_velocity))
    return velocities

def plot_distance_and_velocity(measurements, velocities):
    times = [m[0] for m in measurements]
    left_distances = [m[1] for m in measurements]
    right_distances = [m[2] for m in measurements]
    
    velocity_times = [v[0] for v in velocities]
    left_velocities = [v[1] for v in velocities]
    right_velocities = [v[2] for v in velocities]

    # Normalize time data to start from zero
    start_time = times[0]
    times = [t - start_time for t in times]
    velocity_times = [t - start_time for t in velocity_times]

    fig, ax1 = plt.subplots(figsize=(10, 5))

    color = 'tab:blue'
    ax1.set_xlabel('Time (seconds)')
    ax1.set_ylabel('Distance (cm)', color=color)
    ax1.plot(times, left_distances, marker='o', linestyle='-', color='blue', label='Left Sensor Distance')
    ax1.plot(times, right_distances, marker='o', linestyle='-', color='red', label='Right Sensor Distance')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.legend(loc='upper left')
    
    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:green'
    ax2.set_ylabel('Velocity (cm/s)', color=color)  # we already handled the x-label with ax1
    ax2.plot(velocity_times, left_velocities, marker='x', linestyle='--', color='green', label='Left Sensor Velocity')
    ax2.plot(velocity_times, right_velocities, marker='x', linestyle='--', color='purple', label='Right Sensor Velocity')
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.legend(loc='upper right')

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.title('Time vs. Distance and Velocity Measurement of KITT')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    kitt = KITT('COM3')
    # To test KITT for the overall delay in determining how far an object is, when it needs to stop and actually stopping
    data = kitt.run_distance_measurement()
    # Calculate velocity from the measurements
    velocities = calculate_velocity(kitt.measurements)
    # Plot the distance and velocity measurements vs time
    plot_distance_and_velocity(kitt.measurements, velocities)
    kitt = KITT('COM3')
    kitt.serial.write(b'Sv\n')
    data = kitt.serial.read_until(b'\x04')
    kitt.serial.close()
    print(data)
