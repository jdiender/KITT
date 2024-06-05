import numpy as np
import matplotlib.pyplot as plt
import math

class KITTmodel:
    def __init__(self):
        self.v0 = 0
        self.v = 0
        self.dt = 0.2
        self.L = 0.335
        self.z = np.array([3.5, 0.5])  # position
        self.d = np.array([0, 1])  # direction
        self.angle = 0

    def velocity(self, mode):
        self.v0 = self.v  # initial velocity
        m = 5.6  # mass of the car
        b = 10  # viscous drag coefficient
        Fd = b * abs(self.v0)  # determine drag
        if mode == 'deceleration':
            if self.v < 0:
                F_net = -7.4 + Fd  # net force equal to max Fb + Fd
            else:
                F_net = -7.4 - Fd  # net force equal to max Fb - Fd
            a = F_net / m  # determine acceleration
            self.v = self.v0 + a * self.dt  # determine new velocity
        else:
            if self.v < 0:
                F_net = 6.3 + Fd  # net force equal to max Fa + Fd
            else:
                F_net = 6.3 - Fd  # net force equal to max Fa - Fd
            a = F_net / m  # determine acceleration
            self.v = self.v0 + a * self.dt  # determine new velocity
        return self.v

    def direction(self, alpha):
        theta = ((self.v * math.sin(math.radians(alpha))) / self.L) * self.dt  # angle over which the car turns
        r = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])  # determine the rotation vector
        self.d = np.dot(r, self.d)  # calculate the new direction vector

    def position(self, mode, alpha):
        self.velocity(mode)  # calculate the velocity
        self.direction(alpha)  # determine the direction
        self.z = self.z + self.v * self.dt * self.d  # determine the new position of the car
        return self.z
    
    def state_tracking(self, b0x, b0y):
        current_position = self.z  # position of the car
        x_data, y_data = [], []  # For plotting the path state tracking calculates
        commands = [('s', 0.4)]  # gather commands for car.py
        target_position = np.array([b0x, b0y])
        
        while np.linalg.norm(current_position - target_position) > 0.1:
            d0x, d0y = self.d  # direction vector
            theta_direction = math.degrees(math.atan2(d0y, d0x))  # Angle of the direction vector in degrees
            theta_expected = math.degrees(math.atan2(b0y - current_position[1], b0x - current_position[0]))  # Expected angle
            
            angle_diff = (theta_expected - theta_direction + 360) % 360
            if angle_diff > 180:
                angle_diff -= 360
            
            if np.linalg.norm(current_position - target_position) >= 1.70:
                direction = "forward" if abs(angle_diff) < 90 else "reverse"
            match direction:
                case "forward":
                    if angle_diff < -5:
                        # go right
                        if commands and commands[-1][0] == 'a':
                            commands[-1] = ('a', commands[-1][1] + 0.2)
                        else:
                            commands.append(('a', 0.2))
                        self.angle = -23.9 #-24.9
                    elif angle_diff > 5:
                        # go left
                        if commands and commands[-1][0] == 'd':
                            commands[-1] = ('d', commands[-1][1] + 0.2)
                        else:
                            commands.append(('d', 0.2))
                        self.angle = 23.3 #24.3
                    else:
                        # go straight
                        if commands and commands[-1][0] == 's':
                            commands[-1] = ('s', commands[-1][1] + 0.2)
                        else:
                            commands.append(('s', 0.2))
                        self.angle = 0
                case "reverse":
                    if angle_diff < -5:
                        # go left
                        if commands and commands[-1][0] == 'z':
                            commands[-1] = ('z', commands[-1][1] + 0.2)
                        else:
                            commands.append(('z', 0.2))
                        self.angle = -24.9
                    elif angle_diff > 5:
                        # go right
                        if commands and commands[-1][0] == 'c':
                            commands[-1] = ('c', commands[-1][1] + 0.2)
                        else:
                            commands.append(('c', 0.2))
                        self.angle = 24.3
                    else:
                        # go straight
                        if commands and commands[-1][0] == 'x':
                            commands[-1] = ('x', commands[-1][1] + 0.2)
                        else:
                            commands.append(('x', 0.2))
                        self.angle = 0
            
            current_position = self.position("acceleration" if direction == "forward" else "deceleration", self.angle)
            x_data.append(current_position[0])  # Save x coordinate of the car
            y_data.append(current_position[1])  # Save y coordinate of the car
        commands.append(('e', 1))
        print(commands)
        return x_data, y_data, commands

def wasd(kitt, command=None):
    pos = np.array([0, 0])
    if command:
        key = command
    else:
        key = input("Enter command: ")  # using input instead of keyboard for simplicity

    if key == 'e':  # Stop for forwards
        pos = kitt.position("deceleration", kitt.angle)
    elif key == 'i':  # stop for backwards
        pos = kitt.position("acceleration", kitt.angle)
    elif key == 'a':  # left forward
        kitt.angle = -24.9
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
        i = int(duration / kitt.dt)
        for _ in range(i):
            pos = wasd(kitt, command)
            x_data.append(pos[0])
            y_data.append(pos[1])
    return x_data, y_data

def plot(x, y):
    plt.plot(x, y)
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.xlim(-2.5, 5)
    plt.ylim(-2, 5)
    plt.title('KITT Model Position')
    plt.show()

if __name__ == "__main__":
    kitt = KITTmodel()
    x_data, y_data, commands = kitt.state_tracking(2.5, 3.5)
                                       
    plot(x_data, y_data)
    x_data, y_data = execute_commands(commands)
    plot(x_data, y_data)
