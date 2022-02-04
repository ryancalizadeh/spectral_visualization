import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['axes.facecolor'] = 'black'
RED = 0
GREEN = 1
BLUE = 2

def wav2RGB(wavelength):
    w = int(wavelength)
    if w == 0:
        return (0, 0, 0)

    # colour
    if w >= 380 and w < 440:
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
    elif w >= 645 and w <= 780:
        R = 1.0
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0

    # intensity correction
    if w >= 380 and w < 420:
        SSS = 0.3 + 0.7*(w - 350) / (420 - 350)
    elif w >= 420 and w <= 700:
        SSS = 1.0
    elif w > 700 and w <= 780:
        SSS = 0.3 + 0.7*(780 - w) / (780 - 700)
    else:
        SSS = 0.0

    return (SSS*R, SSS*G, SSS*B)

def make_spectrum(wavelengths: np.ndarray):
    visible_spectrum = np.arange(350, 750)
    emissions = np.zeros(len(visible_spectrum), dtype=bool)
    for wavelength in wavelengths:
        emissions[wavelength-350] = 1
    
    colors = [wav2RGB(wav * emissions[i]) for i, wav in enumerate(visible_spectrum)]

    return visible_spectrum, emissions, colors


def main():
    ax1: plt.Axes
    ax2: plt.Axes

    fig, (ax1, ax2)= plt.subplots(2, 1)

    visible_spectrum, emissions, colors = make_spectrum(np.array([578, 545, 435, 608]))
    ax1.bar(visible_spectrum, emissions, color=colors, width=1.0)
    ax1.set_title("Unknown Gas")
    ax1.get_yaxis().set_visible(False)

    visible_spectrum, emissions, colors = make_spectrum(np.arange(350, 749)) #np.array([704, 658, 638, 623, 612, 607, 602, 579, 577, 546, 491, 435, 434, 407, 414])
    ax2.bar(visible_spectrum, emissions, color=colors, width=1.0)
    ax2.set_title("Mercury")
    ax2.get_yaxis().set_visible(False)

    plt.show()

if __name__=="__main__":
    main()

