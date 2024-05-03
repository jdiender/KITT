import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, ifft
from scipy.signal import convolve, unit_impulse

# from refsignal import refsignal            # model for the EPO4 audio beacon signal
# from wavaudioread import wavaudioread
# from recording_tool import recording_tool
Fs_RX = 44100

def ch3(x,y,epsi):
    Nx = len(x) # Length of x
    Ny = len(y) # Length of y
    Nh = Ny - Nx + 1 # Length of h

    # Force x to be the same length as y
    x = np.pad(x, (0, Ny - Nx))

    # Deconvolution in frequency domain
    X = fft(x)
    Y = fft(y)
    #if X is not 0:
    H = Y / X
    #else:
     # H = 0
    # Threshold to avoid blow ups of noise during inversion
    ii = np.absolute(X) < epsi * max(np.absolute(X))
    for idx in range(len(ii)):
        if ii[idx] is False:
            H[idx] = 0

    h = np.real(ifft(H))    # ensure the result is real
    #h = h[:Lhat]    # optional: truncate to length Lhat (L is not reliable?)
    return h


#Defining the period and the time- and frequency axis
#period = 1/Fs_TX

sampled_rate,y5cm=wavfile.read(r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\record_x232_y275.wav")

# Channel estimation via ch3: h1, h2, h3



def calc_distance(h0, h1):
  return abs(np.argmax(h0) - np.argmax(h1)) / Fs_RX * 343

h0_5cm = ch3(y5cm[:,1],y5cm[:,0],0.01)
h1_5cm = ch3(y5cm[:,0],y5cm[:,0],0.01)
dist_5cm = calc_distance(h0_5cm, h1_5cm)
print('Estimated distance is', dist_5cm, 'm')

sampled_rate2,y1m=wavfile.read(r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\record_x232_y275.wav")
sampled_rate2,ref=wavfile.read(r"C:\Users\naufa\OneDrive\Bureaublad\EPO4\student_recording\student_recording\reference.wav")
for  j in range(y1m.shape[1]):
  print("for reference sample", j )
  for i in range(y1m.shape[1]):
      h0 = ch3(y1m[:, i],ref[:, j],0.01)
      h1 = ch3(ref[:, j],ref[:, j],0.01)
      dist = calc_distance(h1, h0)
      peak_time_index = np.argmax(h0)
#print(peak_time_index)
      print('distance', i, 'is ', dist,'m')

    


# h0 = ch3(y1m[:, 4],ref[:, 0],0.01)
# h1 = ch3(ref[:, 0],ref[:, 0],0.01)
# dist = calc_distance(h1, h0)
# peak_time_index = np.argmax(h0)
# #print(peak_time_index)
# print('Estimated distance is', dist, 'm')
#print(h0.shape)
t = np.arange(0, len(h0)/Fs_RX, 1/Fs_RX)
fig, ax = plt.subplots(2, 1, figsize=(10, 7))

ax[0].set_title("Impulse response of microphone 40cm distanced")
ax[0].set_xlabel("Time [s]")
ax[0].set_ylabel("Magnitude")
ax[0].plot(t,h0)
ax[0].set_xlim([0,0.02])
ax[0].plot(t[peak_time_index], h0[peak_time_index], 'ro')  # Marking the peak with a red dot

ax[1].set_title("Impulse response of reference signal")
ax[1].set_xlabel("Time [s]")
ax[1].set_ylabel("Magnitude")
ax[1].plot(h1)
ax[1].set_xlim([0,10])


fig.tight_layout()