import numpy as np
import matplotlib.pyplot as plt
import math

class KITTmodel:
    def __init__(self):
        self.v0 = 0
        self.v = 0
        self.dt = 0.2
        self.L = 0.335
        self.z = np.array([0.0, 0.0])  # position
        self.d = np.array([0, 1])  # direction
        self.angle = 0

    def velocity(self, mode):
        self.v0 = self.v  # initial velocity
        m = 5.6  # mass of the car
        b = 10.2  # viscous drag coefficient
        Fd = b * abs(self.v0)  # determine drag
        match mode:
            case "acceleration":
                if self.v < 0:
                    F_net = 7.36 + Fd  # net force equal to max Fa + Fd
                else:
                    F_net = 7.36 - Fd  # net force equal to max Fa - Fd
            case "acceleration right":
                if self.v < 0:
                    F_net = 5.9 + Fd  # net force equal to max Fa + Fd
                else:
                    F_net = 5.9 - Fd  # net force equal to max Fa - Fd
            case "acceleration left":
                if self.v < 0:
                    F_net = 5.94 + Fd  # net force equal to max Fa + Fd
                else:
                    F_net = 5.94 - Fd  # net force equal to max Fa - Fd        
            case 'deceleration':
                if self.v < 0:
                    F_net = -7.4 + Fd  # net force equal to max Fb + Fd
                else:
                    F_net = -7.4 - Fd  # net force equal to max Fb - Fd 
            case 'left reverse':
                if self.v > 0:
                    F_net = -5.94 - Fd  # net force equal to max Fb - Fd
                else:
                    F_net = -5.94 + Fd  # net force equal to max Fb + Fd
            case 'right reverse':
                if self.v > 0:
                    F_net = -5.9 - Fd  # net force equal to max Fb - Fd
                else:
                    F_net = -5.9 + Fd  # net force equal to max Fb + Fd       
        a = F_net / m  # determine acceleration
        self.v = self.v0 + a * self.dt  # determine new velocity
            
        return self.v

    def direction(self, alpha):
        theta = ((self.v * math.sin(math.radians(alpha))) / self.L) * self.dt  # angle over which the car turns
        r = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])  # determine the rotation vector
        self.d = np.dot(r, self.d)  # calculate the new direction vector
        return self.d

    def position(self, mode, alpha):
        self.velocity(mode)  # calculate the velocity
        self.direction(alpha)  # determine the direction
        self.z = self.z + self.v * self.dt * self.d  # determine the new position of the car
        return self.z

    def check_boundary(self, x, y, max_x, max_y, min_x, min_y):
            if (min_x <= x <= max_x):
                if (min_y <= y <= max_y):
                    return True
                else:
                    return False
            else:
                return False
            
#check of target in cirle--> door 4 if statement van enes met min(xy) max(xy)
#if in circle --> determine x_delta
    def equation_circle(self, x, y, radius, center_x, center_y):
        distance = np.sqrt((x-center_x)**2 + (y-center_y)**2)
        return distance < radius

        
    def check_range(self, current_x, current_y, target_x, target_y, theta_direction):
        radius = 0.85
        offset_x = radius * np.cos(np.radians(90-theta_direction))
        offset_y = radius * np.sin(np.radians(90-theta_direction))
        center1_x = current_x - offset_x
        center2_x = current_x + offset_x
        center1_y = current_y + offset_y
        center2_y = current_y - offset_y
        
        
        check_x1 = self.equation_circle(target_x, target_y, radius, center1_x, center1_y)
        check_x2 = self.equation_circle(target_x, target_y, radius, center2_x, center2_y)
        
        if check_x1:
            return center1_x, center1_y
        elif check_x2:
            return center2_x, center2_y
        else:
            return False
        
    def find_circle_line_intersections(self, h, k, r, theta, x0, y0):
        theta = math.radians(theta)
        m = math.tan(theta)
        
        # Line equation: y = mx + c
        c = y0 - m * x0
        
        # Substitute y = mx + c into the circle equation
        A = 1 + m**2
        B = 2 * (m * c - m * k - h)
        C = h**2 + k**2 + c**2 - 2 * k * c - r**2
        
        # Quadratic equation: Ax^2 + Bx + C = 0
        discriminant = B**2 - 4 * A * C
        
        if discriminant < 0:
            # No intersection
            return None
        elif discriminant == 0:
            # One intersection (tangent line)
            x1 = -B / (2 * A)
            y1 = m * x1 + c
            return (x1, y1)
        else:
            # Two intersections
            sqrt_discriminant = math.sqrt(discriminant)
            x1 = (-B + sqrt_discriminant) / (2 * A)
            y1 = m * x1 + c
            x2 = (-B - sqrt_discriminant) / (2 * A)
            y2 = m * x2 + c
            return (x1, y1, x2, y2)

    def get_line_eq(self, car_x, car_y, orientation_angle):
       
        slope = math.tan(orientation_angle)
        intercept = car_y - slope * car_x
        return slope, intercept

    def get_perpendicular_line_eq(self, point_x, point_y, slope):
        
        perpendicular_slope = -1 / slope
        intercept = point_y - perpendicular_slope * point_x
        return perpendicular_slope, intercept

    def get_intersection(self, slope1, intercept1, slope2, intercept2):
       
        x = (intercept2 - intercept1) / (slope1 - slope2)
        y = slope1 * x + intercept1
        return x, y

    def calculate_projection_coordinates(self, target_x, target_y):
        car_x = self.z[0]
        car_y = self.z[1]
        radius = 0.85
        d0x, d0y = self.d  # direction vector
        orientation_angle = math.degrees(math.atan2(d0y, d0x))  # Angle of the direction vector in degrees
 
        if self.check_range(car_x, car_y, target_x, target_y, orientation_angle) is not False:
            center_x, center_y = self.check_range(car_x, car_y, target_x, target_y, orientation_angle)
        else:
            return False

        proj = self.find_circle_line_intersections(center_x, center_y, radius, orientation_angle, target_x, target_y)
        
        if proj is None:
            proj_x1, proj_y1, proj_x2, proj_y2 = 0, 0, 0, 0
        elif len(proj) == 2:
            proj_x1, proj_y1 = proj 
            proj_x2, proj_y2 = 0, 0
        else:
            proj_x1, proj_y1, proj_x2, proj_y2 = proj
            
        # Get the equation of the line representing the car's orientation
        car_slope, car_intercept = self.get_line_eq(car_x, car_y, orientation_angle)
        # Get the equation of the perpendicular line that goes through the target
        perp_slope1, perp_intercept1 = self.get_perpendicular_line_eq(proj_x1, proj_y1, car_slope)
        perp_slope2, perp_intercept2 = self.get_perpendicular_line_eq(proj_x2, proj_y2, car_slope)
        # Find the intersection point of the car's orientation line and the perpendicular line
        new_x1, new_y1 = self.get_intersection(car_slope, car_intercept, perp_slope1, perp_intercept1)
        new_x2, new_y2 = self.get_intersection(car_slope, car_intercept, perp_slope2, perp_intercept2)
        
        return [(new_x1,new_y1), (new_x2,new_y2)]
    
    def check_coordinates(self, target_position, z, d):
        self.z = z
        self.d = d
        b0x, b0y = target_position
        max_x = 4.4
        max_y = 4.4
        min_x = 0.2
        min_y = 0.2
        print("check 1")
        projected_coordinates = self.calculate_projection_coordinates(b0x, b0y)
        if not projected_coordinates:
            x_data, y_data, commands = self.multiple_coords(target_position)
        else:
            point1, point2 = self.calculate_projection_coordinates(b0x, b0y)
            x, y = point1
            boundary = self.check_boundary(x, y, max_x, max_y, min_x, min_y)
            if boundary == True:
                
                #waypoints = point1
                waypoints= (point1) + (target_position)
                print(waypoints)
                x_data, y_data, commands = self.multiple_coords(waypoints)
            else:
                x, y = point2
                boundary = self.check_boundary(x, y, max_x, max_y, min_x, min_y)
                if boundary == True:
                    #waypoints = point2
                    waypoints= (point2, target_position)
                    print(waypoints)
                    x_data, y_data, commands = self.multiple_coords(waypoints)
                else:
                    print("error")
            return x_data, y_data, commands
        
    def state_tracking(self, b0x, b0y):
        current_position = self.z  # position of the car
        x_data, y_data = [], []  # For plotting the path state tracking calculates
        commands = [('s', 0.2)]  # gather commands for car.py
        target_position = np.array([b0x, b0y])
        count = 0
        
        while np.linalg.norm(current_position - target_position) > 0.1:
            if count<=10:
                d0x, d0y = self.d  # direction vector
                theta_direction = math.degrees(math.atan2(d0y, d0x))  # Angle of the direction vector in degrees
                theta_expected = math.degrees(math.atan2(b0y - current_position[1], b0x - current_position[0]))  # Expected angle
                
                angle_diff = (theta_expected - theta_direction + 360) % 360
                if angle_diff > 180:
                    angle_diff -= 360

                direction = "forward" if abs(angle_diff) < 90 else "reverse"
                match direction:
                    case "forward":
                        if angle_diff < -5:
                            # go right
                            if commands and commands[-1][0] == 'a':
                                commands[-1] = ('a', commands[-1][1] + 0.2)
                            else:
                                commands.append(('a', 0.2))
                            self.angle = -18.5 #-24.9
                            mode ="acceleration right"
                        elif angle_diff > 5:
                            # go left
                            if commands and commands[-1][0] == 'd':
                                commands[-1] = ('d', commands[-1][1] + 0.2)
                            else:
                                commands.append(('d', 0.2))
                            self.angle = 19.0 #24.3
                            mode ="acceleration left"
                        else:
                            # go straight
                            if commands and commands[-1][0] == 's':
                                commands[-1] = ('s', commands[-1][1] + 0.2)
                            else:
                                commands.append(('s', 0.2))
                            self.angle = 0
                            mode ="acceleration"
                    case "reverse":
                        if angle_diff < -5:
                            # go left
                            if commands and commands[-1][0] == 'z':
                                commands[-1] = ('z', commands[-1][1] + 0.2)
                            else:
                                commands.append(('z', 0.2))
                            self.angle = -18.6
                            mode = "left reverse"
                        elif angle_diff > 5:
                            # go right
                            if commands and commands[-1][0] == 'c':
                                commands[-1] = ('c', commands[-1][1] + 0.2)
                            else:
                                commands.append(('c', 0.2))
                            self.angle = 19
                            mode = "right reverse"
                        else:
                            # go straight
                            if commands and commands[-1][0] == 'x':
                                commands[-1] = ('x', commands[-1][1] + 0.2)
                            else:
                                commands.append(('x', 0.2))
                            self.angle = 0
                            mode ="deceleration"
                count+=1
                current_position = self.position(mode, self.angle)
                x_data.append(current_position[0])  # Save x coordinate of the car
                y_data.append(current_position[1])  # Save y coordinate of the car
            else:
                commands.append(('e', 1))
                commands.append(('r', 10))
                current_position = self.position(mode, self.angle)
                x_data.append(current_position[0])  # Save x coordinate of the car
                y_data.append(current_position[1])  # Save y coordinate of the car
                count = 0
            
            return x_data, y_data, commands
    
    def compare_position(self, bx, by):
        x, y = self.z
        if math.sqrt((x - bx)**2 + (y - by)**2) > 0.3:
            destination = 'False'
            x_data, y_data, commands = self.state_tracking(bx, by)
            return x_data, y_data, commands, destination
        else:
            destination = 'True'
            commands = ('q', 1)
            print("Destination reached")
            return x, y, commands, destination
    
    def multiple_coords(self, target_coords):
        x_data, y_data = [], []
        commands = []
        i = 0
        while (i < len(target_coords)):
            coord_x =  target_coords[i] 
            coord_y = target_coords[i+1]
            x_vals, y_vals, cmd, destination = self.compare_position(coord_x, coord_y)
            x_data += x_vals
            y_data += y_vals
            commands += cmd
            if(destination): i= i+2
        
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
        kitt.angle = -18.6
        pos = kitt.position("acceleration left", kitt.angle)
    elif key == 's':  # straight
        kitt.angle = 0
        pos = kitt.position("acceleration right", kitt.angle)
    elif key == 'd':  # right
        kitt.angle = 19
        pos = kitt.position("acceleration", kitt.angle)
    elif key == 'x':  # straight Backwards
        kitt.angle = 0
        pos = kitt.position("deceleration", kitt.angle)
    elif key == 'c':  # right Backwards
        kitt.angle = 19
        pos = kitt.position("right reverse", kitt.angle)
    elif key == 'z':  # Left Backwards
        kitt.angle = -18.6
        pos = kitt.position("left reverse", kitt.angle)
    elif key == 'r': #start recording
        print("Car should record at this location")
        print(pos)
    return pos

def execute_commands(commands):
    kitt = KITTmodel()
    x_data, y_data = [], []
    iteration_count = 0  # Initialize the iteration counter
    
    for command, duration in commands:
        i = int(duration / kitt.dt)
        for _ in range(i):
            pos = wasd(kitt, command)
            x_data.append(pos[0])
            y_data.append(pos[1])
            iteration_count += 1  # Increment the iteration counter
            
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
    b = (3.2, 2.5)
    z = [1.0, 1.0]
    d = [0, 1]
    x_data, y_data, commands, destination = kitt.check_coordinates(b, z, d)
                                       
    plot(x_data, y_data)
    x_data, y_data = execute_commands(commands)
    plot(x_data, y_data)