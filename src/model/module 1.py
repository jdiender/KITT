import serial
import keyboard
import time

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
            elif key == 'a': #Right
                kitt.set_angle(200)
            elif key == 's': #straight
                kitt.set_angle(150)
            elif key == 'd': #links
                kitt.set_angle(100)
            elif key == 'z':#Backwards 
                kitt.set_speed(140)
            elif key == 'e':#Brakes and goes opposite direction for a while
                kitt.emergency_brake()
            elif key == 'p':#Play audio beacon
                kitt.set_audio_beacon_on()
            elif key == 'o':#Turn audio beacon off
                kitt.set_audio_beacon_off()
            elif key == 'x':
                break  # Exit loop
    finally:
        kitt.stop()
        if kitt.serial:
            kitt.serial.close()
        
if __name__ == "__main__":
    kitt = KITT('COM3')
    wasd(kitt)