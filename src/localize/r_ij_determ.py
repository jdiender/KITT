from functions import *
import numpy as np
import matplotlib.pyplot as plt
recording_x = np.array([0.64, 0.82, 1.09, 1.43, 1.50, 1.78, 2.32,0,0,0,0])
recording_y = np.array([0.40, 3.99 ,0.76, 2.96, 1.85, 4.93, 2.75,0,0,0,0])
r_ij =[]
for i in range(5):
    for j in range (i+1, 5):
        mici_dist= np.sqrt((mic_xcoordinates[i]-recording_x[0])**2 + (mic_ycoordinates[i]-recording_y[0])**2)
        micj_dist= np.sqrt((mic_xcoordinates[j]-recording_x[0])**2 + (mic_ycoordinates[j]-recording_y[0])**2)
        diff = mici_dist -micj_dist
        r_ij.append( diff)

print("expected r_ij :", np.array(r_ij).reshape(-1,1))
                           