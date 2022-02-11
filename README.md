# spectral_visualization
Framework to create simulated emission spectra in python

Command Line Syntax:

`python spectra.py <Data File> <Output Image File>`

Where `<Data File>` is a csv file with each column containing the name of your sample and the wavelengths of light emitted and `<Output Image File>` is the name of the jpg or png file you would like to write the result. Note that if `<Output Image File>` cannot be found, matplotlib will create the file for you.

Example:

`python spectra.py data.csv spectra.png`

With the data.csv file located in this directory produces the following:

![Emission spectrum of unknown gas compared to mercury](spectra.png?raw=true "Emission spectrum of unknown gas compared to mercury")

If you are curious about how the wavelengths are converted to RGB colours, try running the file "analysis.py"

Sources:

https://en.wikipedia.org/wiki/CIE_1931_color_space
