import numpy as np
import matplotlib.pyplot as plt
import spectra

def main():
    low, high = 200, 820
    wavelengths = np.arange(low, high)
    c_values = np.array([spectra.wav2RGB(wavelength) for wavelength in wavelengths])
    
    r = c_values[:, spectra.RED]
    g = c_values[:, spectra.GREEN]
    b = c_values[:, spectra.BLUE]

    fig, ax = plt.subplots()

    ax.plot(wavelengths, r, 'r')
    ax.plot(wavelengths, g, 'g')
    ax.plot(wavelengths, b, 'b')
    ax.set_facecolor("white")
    ax.set_xlim([low, high])
    plt.show()

if __name__=="__main__":
    main()