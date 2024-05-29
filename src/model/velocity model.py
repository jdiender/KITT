import numpy as np
import matplotlib.pyplot as plt

# Constants
m = 5.6          # mass of the car in kg
b = 10            # drag coefficient 
Fa_max = 6      # maximum force from the engine in N
Fb_max = 7      # maximum braking force in N
dt = 0.01        # time step in seconds
T = 8            # total simulation time in seconds

# Time array
t = np.arange(0, T, dt)

def simulate(F_max, initial_velocity, mode='acceleration'):
    N = len(t)
    v = np.zeros(N)
    z = np.zeros(N)
    v[0] = initial_velocity

    for i in range(1, N):
        # Calculate drag force linearly dependent on the velocity
        Fd = b * abs(v[i-1])  # use abs to ensure drag is always opposite to motion
        
        if mode == 'deceleration':
            # During deceleration, both braking and drag forces slow down the car
            F_net = -F_max + Fd  # Notice the drag adds to the braking force
        else:
            # During acceleration, subtract drag from engine force
            F_net = F_max - Fd

        # Acceleration calculation
        a = F_net / m
        v[i] = v[i-1] + a * dt
        z[i] = z[i-1] + v[i-1] * dt + 0.5 * a * dt**2

    return v, z

# Simulation for Acceleration
v_accel, z_accel = simulate(Fa_max, 0, mode='acceleration')

# Simulation for Deceleration from a starting speed
v_decel, z_decel = simulate(Fb_max, v_accel[-1], mode='deceleration')

# Plotting
plt.figure(figsize=(12, 10))

plt.subplot(2, 2, 1)
plt.plot(t, v_accel, 'r')
plt.title('Velocity vs Time (Acceleration)')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.grid(True)
    
plt.subplot(2, 2, 2)
plt.plot(t, z_accel, 'g')
plt.title('Position vs Time (Acceleration)')
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.grid(True)

plt.subplot(2, 2, 3)
plt.plot(t, v_decel, 'b')
plt.title('Velocity vs Time (Deceleration)')
plt.xlabel('Time (s)')
plt.ylabel('Velocity (m/s)')
plt.grid(True)

plt.subplot(2, 2, 4)
plt.plot(t, z_decel, 'orange')
plt.title('Position vs Time (Deceleration)')
plt.xlabel('Time (s)')
plt.ylabel('Position (m)')
plt.grid(True)

plt.tight_layout()
plt.show()
