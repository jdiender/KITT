import serial
import keyboard
import time
import pandas as pd


class KITT:
    def __init__(self, port, baudrate=115200):
        self.serial = serial.Serial(port, baudrate, rtscts=True)
        self.speed = 150
        self.angle = 150
        self.carrier_frequency = (5000).to_bytes(2, byteorder='big')
        self.bit_frequency = (2500).to_bytes(2, byteorder='big')
        self.repetition_count = (1250).to_bytes(2, byteorder='big')
        self.code = 0xDEADBEEF.to_bytes(4, byteorder='big')
        self.measurements  = []
        # state variables such as speed, angle are defined here
        
    def send_command(self, command):
        self.serial.write(command.encode())
    
        
    def __del__(self):
        self.serial.close()   
             
        
    def sensor_data_distance(self):
        self.serial.write(b'Sd\n')
        data = self.serial.read_until(b'\x04')
        return data
    
    def sensor_data_voltage(self):
        self.serial.write(b'Sv\n')
        data = self.serial.read_until(b'\x04')
        return data
    
    def test_distance_with_object_placement(self):
        # KITT remains stationary
        sensor_distance = self.sensor_data_distance()
        if sensor_distance is not None:
            print(f"Measured Sensor Distance: {sensor_distance} cm")
        self.measurements.append(sensor_distance)
        print(self.measurements)
        self.serial.close()
        return self.measurements
    
    def test_bluetooth(self):        
        start_time = time.time()
        self.serial.write(b'Sv\n')
        data = self.serial.read_until(b'\x04')
        stop_time = time.time() - start_time
        return(data, stop_time)
    

        
if __name__ == "__main__":
    kitt = KITT('COM3')
    print("Starting distance measurement test with object placement...")
    measurement_data = kitt.test_bluetooth()
    print(measurement_data)
    #kitt.test_beam_angle(kitt)

    # Create a sample DataFrame
    #df = pd.DataFrame(measurement_data)

    # Save to a CSV file
    #df.to_csv('measurements2_1.csv', index=False)
