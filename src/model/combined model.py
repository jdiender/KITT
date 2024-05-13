import numpy as np
import matplotlib.pyplot as plt
import keyboard
import math

class KITTmodel:
    def __init__(self):
        self.v0 = 0
        self.v = 0
        self.dt = 0.01
        self.L = 0.335
        self.z = np.array([0, 0])
        self.d = np.array([0, 1])

    def velocity(self, mode):
        self.v0 = self.v  # initial velocity
        m = 5.6  # mass of the car
        b = 5  # viscous drag coefficient
        Fd = b * abs(self.v0)  # determine drag
        if mode == 'deceleration':
            F_net = -14 + Fd  # deceleration has an opposite net force
        else:
            F_net = 10 - Fd
        a = F_net / m  # determine acceleration
        self.v = self.v0 + a * self.dt  # determine new velocity
        return self.v
    
    def direction(self, alpha):
        theta = ((self.v * math.sin(math.radians(alpha))) / self.L) * self.dt  # angle over which the car turns
        r = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])  # determine the rotation vector
        self.d = np.dot(r, self.d) #calculate the new direction vector
        
    def position(self, mode, alpha):
        self.velocity(mode)
        self.direction(alpha)
        self.z = self.z + self.v * self.dt * self.d #Determine the new position of the car
        return self.z
    
def wasd(kitt):
    plt.ion()
    fig, ax = plt.subplots()
    x_data, y_data = [], []

    try:
        while True:
            key = keyboard.read_key()
            if key == 'w':  # Forward
                pos = kitt.position("acceleration", 0)
            elif key == 'q':  # Stop
                pos = kitt.position("deceleration", 0)
            elif key == 'a':  # left
                pos = kitt.position("acceleration", -24.9)
            elif key == 's':  # straight
                pos = kitt.position("acceleration", 0)
            elif key == 'd':  # right
                pos = kitt.position("acceleration", 24.9)
            elif key == 'z':  # Backwards 
                kitt.velocity("deceleration")
                pos = kitt.z  # Maintain current position for plotting
            elif key == 'x':
                break  # Exit loop
            x_data.append(pos[0])
            y_data.append(pos[1])
            ax.plot(x_data, y_data, color='blue')
            fig.canvas.draw()
            fig.canvas.flush_events()

    finally:
        kitt.v = 0
        plt.ioff()
        plt.show()
        
if __name__ == "__main__":
    kitt = KITTmodel()
    wasd(kitt)
