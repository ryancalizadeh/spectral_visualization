from typing import Callable
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['axes.facecolor'] = 'black'
import sys
RED = 0
GREEN = 1
BLUE = 2
XYZ_MAX_INVERSE = 0.5604772321544685

def g(x, m, s1, s2):
    if x < m:
        return np.exp(-1/2 * ((x-m)/s1)**2)
    if x >= m:
        return np.exp(-1/2 * ((x-m)/s2)**2)

def wav2RGB(wavelength):
    w = int(wavelength)
    if w == 0:
        return (0, 0, 0)
    
    R = 1.056 * g(w, 599.8, 37.9, 31.0) + 0.362 * g(w, 442.0, 16.0, 26.7) - 0.065 * g(w, 501.1, 20.4, 26.2)
    G = 0.821 * g(w, 568.8, 46.9, 40.5) + 0.286 * g(w, 530.9, 16.3, 31.1)
    B = 1.217 * g(w, 437.0, 11.8, 36.0) + 0.681 * g(w, 459.0, 26.0, 13.8)

    return (R * XYZ_MAX_INVERSE, G * XYZ_MAX_INVERSE, B * XYZ_MAX_INVERSE)

def wav2RGB_bright(wavelength):
    """
    Approximation of the XYZ colorspace using simpler intensity functions.
    Less accurate than wav2RGB, but in general produces brighter lines.
    """
    w = int(wavelength)
    if w == 0:
        return (0, 0, 0)

    # colour
    if w < 440:
        R = -(w - 440.) / (440. - 350.)
        G = 0.0
        B = 1.0
    elif w >= 440 and w < 490:
        R = 0.0
        G = (w - 440.) / (490. - 440.)
        B = 1.0
    elif w >= 490 and w < 510:
        R = 0.0
        G = 1.0
        B = -(w - 510.) / (510. - 490.)
    elif w >= 510 and w < 580:
        R = (w - 510.) / (580. - 510.)
        G = 1.0
        B = 0.0
    elif w >= 580 and w < 645:
        R = 1.0
        G = -(w - 645.) / (645. - 580.)
        B = 0.0
    elif w >= 645:
        R = 1.0
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0

    # intensity correction
    if w >= 350 and w < 380:
        SSS = 0.6 * (w - 350) / (380 - 350)
    elif w >= 380 and w < 420:
        SSS = 0.3 + 0.7*(w - 350) / (420 - 350)
    elif w >= 420 and w <= 700:
        SSS = 1.0
    elif w > 700 and w <= 780:
        SSS = 0.3 + 0.7*(780 - w) / (780 - 700)
    elif w > 780 and w <= 800:
        SSS = -0.3 * (w - 800) / (800 - 780)
    else:
        SSS = 0.0
    
    return (SSS*R, SSS*G, SSS*B)


def make_spectrum(wavelengths: np.ndarray, wavelength_function: Callable):
    visible_spectrum = np.arange(350, 800)
    emissions = np.zeros(len(visible_spectrum), dtype=bool)
    for wavelength in wavelengths:
        if wavelength < 800 and wavelength >= 350:
            emissions[wavelength-350] = 1
        elif wavelength != 0:
            print(f"Warning: Wavelength {wavelength} is outside of the visible spectrum, and was not rendered.")
    
    colors = [wavelength_function(wav * emissions[i]) for i, wav in enumerate(visible_spectrum)]

    return visible_spectrum, emissions, colors


def main():
    args = sys.argv[1:]

    if len(args) > 0:
        df = pd.read_csv(args[0])
        cols = df.columns
        n = len(cols)
        fig, axs = plt.subplots(n, 1)

        for i, col in enumerate(cols):
            wavs = df[col].to_numpy(dtype=np.unsignedinteger)
            wavs = wavs[~np.isnan(wavs)]

            visible_spectrum, emissions, colors = make_spectrum(wavs, wav2RGB)

            axs[i].bar(visible_spectrum, emissions, color=colors, width=1.0)
            axs[i].set_title(col)
            axs[i].get_yaxis().set_visible(False)
        plt.show()

        if len(args) > 1:
            fig.savefig(args[1])

    

if __name__=="__main__":
    main()

