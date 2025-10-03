# Other packages
import numpy as np
import sys
import argparse
import os
from os.path import join
from tool import print_to_file, nemo_format
import time
from Chianti import chianti


class ChiantiCoolNemoGen():

    def __init__(self, ion_list, T_min=1.0E+01, T_max=1.0E+09, ne_min=0.0, ne_max=1.0E+13,
                 make_tab=True, cooling_tab_dir='', make_plot=True, make_nemo_format=True,
                 cooling_plot_dir='', IncludeFreeFree=True, IncludeFreeBound=False,
                 IncludeLine=True, Include2photon=True):

        print("Chianti NEMO Cooling Table Generator")

        self.ion_list = ion_list
        self.T_min = T_min
        self.T_max = T_max
        self.ne_min = ne_min
        self.ne_max = ne_max
        self.make_tab = make_tab
        self.make_plot = make_plot
        self.make_nemo_format = make_nemo_format

        # Check directories
        if make_plot and not cooling_plot_dir:
            raise ValueError("cooling_plot_dir must be provided if make_plot is True")
        else:
            self.cooling_plot_dir = cooling_plot_dir

        if make_tab or make_nemo_format:
            if not cooling_tab_dir:
                raise ValueError("cooling_tab_dir must be provided if make_tab or make_nemo_format is True")
            else:
                self.cooling_tab_dir = cooling_tab_dir

        # Cooling processes to include
        self.IncludeFreeFree = IncludeFreeFree
        self.IncludeFreeBound = IncludeFreeBound
        self.IncludeLine = IncludeLine
        self.Include2photon = Include2photon

        # Generate tables
        self.generator()

    def generator(self):

        # Making temperature and electron number density array #################
        temperature = []
        for i in range(81):
            log_temp = 1.0 + i * 0.1
            temperature.append(pow(10, log_temp))

        ne = []
        for i in range(27):
            log_ne = i * 0.5
            ne.append(pow(10, log_ne))

        for ion in self.ion_list:

            # creating list for this ion
            data = {}
            data.update({'Temperature': np.log10(temperature)})

            # loop over electron number density
            for i in range(len(ne)):
                chianti_ion = chianti(pion_ion=ion, temperature=temperature, eDensity=ne[i])

                print_statement = f" Computing {ion} cooling rate for log(ne) {np.log10(ne[i])}"
                print(print_statement, end="\r")

                # getting the cooling table
                cooling_rate = chianti_ion.get_radiative_cooling(
                    IncludeFreeFree=self.IncludeFreeFree, IncludeFreeBound=self.IncludeFreeBound,
                    IncludeLine=self.IncludeLine, Include2photon=self.Include2photon)

                # plotting the cooling rate
                if self.make_plot:
                    chianti_ion.plot_cooling_rate(cooling_rate, self.cooling_plot_dir)


                # print to file
                total_rate = cooling_rate['total-rate']
                total_rate[total_rate < pow(10, -50)] = pow(10, -50)
                data.update({str(np.log10(ne[i])): np.log10(total_rate)})

            sys.stdout.write('\x1b[2K')
            sys.stdout.write(f" [DONE] Computed cooling table for {ion}\n")
            cooling_tab = print_to_file(data, ion, self.cooling_tab_dir)
            nemo_format(cooling_tab, ion, self.cooling_tab_dir)
