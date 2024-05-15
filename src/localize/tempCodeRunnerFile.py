for cropped_chan in cropped_channels:
    plt.plot(cropped_chan)
    peak2 = np.argmax(np.abs(cropped_chan))
    plt.plot(peak2,cropped_chan[peak2],'ro')
    plt.show()