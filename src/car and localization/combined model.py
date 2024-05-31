import numpy as np
import matplotlib.pyplot as plt
import math
from localization import localization

class KITTmodel:
    def __init__(self):
        self.v0 = 0
        self.v = 0
        self.dt = 0.01
        self.L = 0.335
        self.z = np.array([0, 0]) #position
        self.d = np.array([0, 1]) #direction
        self.angle = 0

    def velocity(self, mode):
        self.v0 = self.v  # initial velocity
        m = 5.6  # mass of the car
        b = 10  # viscous drag coefficient
        Fd = b * abs(self.v0) #+ c*self.v*self.v # determine drag
        if mode == 'deceleration':
            if self.v<0:
                F_net = -7.4 + Fd  # net force equal to max Fb + Fd
            else:
                F_net = -7.4 - Fd  # net force equal to max Fb - Fd
            a = F_net / m  # determine acceleration
            self.v = self.v0 + a * self.dt  # determine new velocity
        else:
            if self.v<0:
                F_net = 6 + Fd # net force equal to max Fa + Fd
            else:
                F_net = 6- Fd # net force equal to max Fa - Fd
            a = F_net / m  # determine acceleration
            self.v = self.v0 + a * self.dt  # determine new velocity
        return self.v
    
    def direction(self, alpha):
        theta = ((self.v * math.sin(math.radians(alpha))) / self.L) * self.dt  # angle over which the car turns
        r = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])  # determine the rotation vector
        self.d = np.dot(r, self.d)  # calculate the new direction vector
        
    def position(self, mode, alpha):
        self.velocity(mode) #calculate the velocity
        self.direction(alpha) #determine the directionspee
        print(self.v)
        self.z = self.z + self.v * self.dt * self.d  # determine the new position of the car
        return self.z
    
def wasd(kitt, command=None):
    pos = np.array([0, 0])
    if command:
        key = command
    else:
        key = input("Enter command: ")  # using input instead of keyboard for simplicity
        
    if key == 'e':  # Stop for forwards
        pos = kitt.position("deceleration", kitt.angle)
    elif key == 'i': #stop for backwards
        pos = kitt.position("acceleration", kitt.angle)
    elif key == 'a':  # left forward
        kitt.angle =-24.9
        pos = kitt.position("acceleration", kitt.angle)
    elif key == 's':  # straight
        kitt.angle = 0
        pos = kitt.position("acceleration", kitt.angle)
    elif key == 'd':  # right
        kitt.angle = 24.3
        pos = kitt.position("acceleration", kitt.angle)
    elif key == 'x':  # straight Backwards 
        kitt.angle = 0
        pos = kitt.position("deceleration", kitt.angle)
    elif key == 'c':  # right Backwards 
        kitt.angle = 24.3
        pos = kitt.position("deceleration", kitt.angle)
    elif key == 'z':  # Left Backwards 
        kitt.angle = -24.9
        pos = kitt.position("deceleration", kitt.angle)
    return pos
        
def execute_commands(commands):
    kitt = KITTmodel()
    x_data, y_data = [], []
    for command, duration in commands:
        i = int(duration / 0.01)
        for _ in range(i):
            pos = wasd(kitt, command)
            x_data.append(pos[0])
            y_data.append(pos[1])
    return x_data, y_data

def plot(x, y):
    plt.plot(x, y)
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.xlim(-2.5, 2.5)
    plt.ylim(0, 5)
    plt.title('KITT Model Position')
    plt.show()

def state_tracking(kitt, d0y, d0x, b0x, b0y):
    localize = localization(recording)
    location = localize.locate()
    car_x = location[0]
    car_y = location[1]
    theta_direction =  math.atan2((b0y-d0y)/(b0x-d0x)) 
    theta_expected =  math.atan2((b0y-car_y)/(b0x-car_x))
    diff_theta = theta_direction - theta_expected
    if diff_theta < 0:
        # go left
        pos= wasd(kitt, 'a')
    if diff_theta > 0:
        pos= wasd(kitt, 'd')
        # go right
    else:
        pos= wasd(kitt, 's')
        # go straight
        
if __name__ == "__main__":
    commands = [('s', 1),  ('d', 2.4), ('a', 7), ('d', 6), ('e', 1)]  
    #commands = [('s', 0.5), ('d', 2.5), ('a', 2.5), ('e', 0.5), ('z', 2 ), ('e', 1)]  
    x_data, y_data = execute_commands(commands)
    plot(x_data, y_data)
