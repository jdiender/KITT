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
        
    def __del__(self):
        self.serial.close()   
             
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
        
    def sensor_data_distance(self):
        self.serial.write(b'Sd\n')
        data = self.serial.read_until(b'\x04').decode().strip()
        return float(data) if data.isdigit() else None
    
    def test_distance_with_object_placement(self):
        # KITT remains stationary
        try:
            while True:
                true_distance_left = input("Enter the true measured distance to the object in cm from the left sensor(type 'q' to quit): ")
                if true_distance_left.lower() == 'q':
                    break
                true_distance_right = input("Enter the true measured distance to the object in cm from the right sensor(type 'q' to quit): ")
                if true_distance_right.lower() == 'q':
                    break
                input("Adjust the object to the given distance and press Enter to measure with sensors.")
                sensor_distance = self.sensor_data()
                if sensor_distance is not None:
                    print(f"Measured Sensor Distance: {sensor_distance} cm")
                    self.measurements.append(float(true_distance_left), float(true_distance_right),sensor_distance)
        finally:
            self.serial.close()
            return self.measurements
            

    def test_beam_angle(self):
        results = {}
        angles = range(-45, 46, 15)  # from -45 to 45 degrees in 15 degree increments
        for angle in angles:
            self.set_angle(angle)
            time.sleep(10)  # Wait for any physical adjustment to settle
            distance = self.sensor_data()
            results[angle] = distance
            print(f"Angle: {angle} degrees, Distance: {distance} cm")
        return results

        
if __name__ == "__main__":
    kitt = KITT('COM3')
    print("Starting distance measurement test with object placement...")
    measurement_data = kitt.test_distance_with_object_placement()
    kitt.test_beam_angle(kitt)

    # Create a sample DataFrame
    df = pd.DataFrame(measurement_data)

    # Save to a CSV file
    df.to_csv('measurements2_1.csv', index=False)
