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

    def sensor_data(self):
        self.serial.write(b'S\n')
        data = self.serial.read_until(b'\x04').decode().strip()
        return float(data) if data.isdigit() else None
    
    def __del__(self):
        self.serial.close()

    def test_distance_with_object_movement(self):
        print("Start moving the object towards or away from KITT.")
        input("Press Enter to start recording measurements.")
        start_time = time.time()
        try:
            while True:
                measured_distance = self.sensor_data()
                if measured_distance is not None:
                    current_time = time.time() - start_time
                    self.measurements.append((current_time, measured_distance))
                    print(f"Time: {current_time:.2f}s, Measured Distance: {measured_distance} cm")
                if input("Press 'q' to stop or Enter to continue measuring: ") == 'q':
                    break
        finally:
            self.stop()
            self.__del__() #break connection with KITT
            return self.measurements

if __name__ == "__main__":
    kitt = KITT('COM3')
    print("Testing how quickly the sensor detects changes in distance...")
    measurements = kitt.test_distance_with_object_movement()
    # Create a sample DataFrame
    df = pd.DataFrame(measurements)

    # Save to a CSV file
    df.to_csv('measurements2_2.csv', index=False)