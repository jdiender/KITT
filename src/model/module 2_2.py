import serial
import keyboard
import time
import pandas as pd

class KITT:
    def __init__(self, port, baudrate=115200):
        self.serial = serial.Serial(port, baudrate, rtscts=True)
        self.angle = 150  # Default neutral angle
        self.speed = 150 # Default no angle
        self.measurements  = []
        
    def send_command(self, command):
        self.serial.write(command.encode())

    def set_angle(self, angle):
        self.angle = angle
        self.send_command(f'D{angle}\n')

    def stop(self):
        self.set_angle(150)  # Return to neutral position

    def sensor_data_distance(self):
        self.serial.write(b'Sd\n')
        data = self.serial.read_until(b'\x04')
        return data
    
    def __del__(self):
        self.serial.close()

    def test_distance_with_object_placement(self):
        # KITT remains stationary
        sensor_distance = self.sensor_data_distance()
        if sensor_distance is not None:
            print(f"Measured Sensor Distance: {sensor_distance} cm")
        self.measurements.append(sensor_distance)
        print(self.measurements)
        self.serial.close()
        return self.measurements
            

    
if __name__ == "__main__":
    kitt = KITT('COM3')
    print("Testing how quickly the sensor detects changes in distance...")
    start_time = time.time()
    a=kitt.test_distance_with_object_placement()
    stop_time = time.time() - start_time
    print(stop_time)
