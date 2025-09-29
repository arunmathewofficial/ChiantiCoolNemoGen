# Other packages
import numpy as np
import sys
import argparse
import os
from os.path import join
from tool import print_to_file, nemo_format
import time
from Chianti import chianti

print(f" Chianti NEMO Cooling Table Generator")

ion_list = [
    # Hydrogen
    'H', 'H1+',
    # Helium
    'He', 'He1+', 'He2+',
    # Carbon
    'C', 'C1+', 'C2+', 'C3+', 'C4+', 'C5+', 'C6+',
    # Nitrogen
    'N', 'N1+', 'N2+', 'N3+', 'N4+', 'N5+', 'N6+', 'N7+',
    # Oxygen
    'O', 'O1+', 'O2+', 'O3+', 'O4+', 'O5+', 'O6+', 'O7+', 'O8+',
    # Neon
    'Ne', 'Ne1+', 'Ne2+', 'Ne3+', 'Ne4+', 'Ne5+', 'Ne6+', 'Ne7+', 'Ne8+', 'Ne9+', 'Ne10+',
    # Silicon
    'Si', 'Si1+', 'Si2+', 'Si3+', 'Si4+', 'Si5+', 'Si6+', 'Si7+', 'Si8+', 'Si9+', 'Si10+',
    'Si11+', 'Si12+', 'Si13+', 'Si14+',
    # Sulfur
    'S', 'S1+', 'S2+', 'S3+', 'S4+', 'S5+', 'S6+', 'S7+', 'S8+', 'S9+', 'S10+', 'S11+',
    'S12+', 'S13+', 'S14+', 'S15+', 'S16+',
    # Iron
    'Fe', 'Fe1+', 'Fe2+', 'Fe3+', 'Fe4+', 'Fe5+', 'Fe6+', 'Fe7+', 'Fe8+', 'Fe9+', 'Fe10+',
    'Fe11+', 'Fe12+', 'Fe13+', 'Fe14+', 'Fe15+', 'Fe16+', 'Fe17+', 'Fe18+', 'Fe19+',
    'Fe20+', 'Fe21+', 'Fe22+', 'Fe23+', 'Fe24+', 'Fe25+', 'Fe26+'
]

# Input Arguments ##########################################################
parser = argparse.ArgumentParser(
    description='Chianti Cooling Table Generator for NEMO',
    usage='script.py <output_dir> ')

parser.add_argument('output_dir', help='output directory')
args = parser.parse_args()

# Making necessary Output directories #######################################
outdir = args.output_dir
# Create CoolingRatePlots directory
cooling_plot_dir = join(outdir, 'CoolingRatePlots')
try:
    os.mkdir(cooling_plot_dir)
    print(" Output image directory:", cooling_plot_dir, "created.")
except FileExistsError:
    print(" Output image directory", cooling_plot_dir, "already exists.")

# Create CoolingTabs directory
cooling_tab_dir = join(outdir, 'CoolingTabs')
try:
    os.mkdir(cooling_tab_dir)
    print(" Output tab directory:", cooling_tab_dir, "created.")
except FileExistsError:
    print(" Output tab directory", cooling_tab_dir, "already exists.")


# Making temperature and electron number density array #################
temperature = []
for i in range(81):
    log_temp = 1.0 + i * 0.1
    temperature.append(pow(10, log_temp))

ne = []
for i in range(27):
    log_ne = i * 0.5
    ne.append(pow(10, log_ne))

for ion in ion_list:

    # creating list for this ion
    data = {}
    data.update({'Temperature': np.log10(temperature)})

    # loop over electron number density
    for i in range(len(ne)):
        chianti_ion = chianti(pion_ion=ion, temperature=temperature, eDensity=ne[i])

        print_statement = f" Computing {ion} cooling rate for log(ne) {np.log10(ne[i])}"
        print(print_statement, end="\r")

        # getting the cooling table
        cooling_rate = chianti_ion.get_radiative_cooling(IncludeFreeBound=False)

        # plotting the cooling rate
        chianti_ion.plot_cooling_rate(cooling_rate, cooling_plot_dir)

        # print to file
        total_rate = cooling_rate['total-rate']
        total_rate[total_rate < pow(10, -50)] = pow(10, -50)
        data.update({str(np.log10(ne[i])): np.log10(total_rate)})

    sys.stdout.write('\x1b[2K')
    sys.stdout.write(f" [DONE] Computed cooling table for {ion}\n")
    cooling_tab = print_to_file(data, ion, cooling_tab_dir)
    nemo_format(cooling_tab, ion, cooling_tab_dir)