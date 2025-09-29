# -*- coding: utf-8 -*-
# ChiantiPy packages
import ChiantiPy
import ChiantiPy.core as ch
import ChiantiPy.tools as util
import ChiantiPy.tools.util as util
import ChiantiPy.tools.data as chdata
from ChiantiPy.base import specTrails

# Other packages
import numpy as np
import matplotlib.pyplot as plt
import warnings
import os
import pandas as pd

class chianti:

    def __init__(self, pion_ion, temperature, eDensity):

        self.ion_name = self.get_chianti_symbol(pion_ion)
        self.temperature = temperature
        self.eDensity = eDensity

        self.ion_info = util.convertName(self.ion_name)
        self.ion_string_name = pion_ion
        self.keys = self.todo_keys()

    # get chianti symbol #######################################################
    def get_chianti_symbol(self, pion_ion):
        '''
            Converts a PION species symbol to a corresponding CHIANTI species symbol.

            This function takes a species symbol used in PION (a computational tool) and
            converts it into the format required by CHIANTI, a database for atomic data.
            The function can generate either the elemental symbol or the ionized symbol
            depending on the 'make' parameter.

            :param species: str, the PION species symbol, which can represent both neutral
                            and ionized states.
            :param make: bool, if True, returns the elemental symbol (e.g., 'h' for hydrogen).
                         if False, returns the CHIANTI ion symbol (e.g., 'h_2' for H+).
            :return: str, the corresponding CHIANTI symbol for the species.
            '''

        # Convert the input species symbol to lowercase and remove any '+' characters
        # (denoting ionization)
        species = pion_ion.lower().replace('+', '')

        # Extract alphabetic characters to identify the element symbol (e.g., 'h' from 'h1' or 'h+')
        element = ''.join(filter(str.isalpha, species))

        # Extract numeric characters to determine the ionization level (e.g., '1' from 'h1')
        ion_level = ''.join(filter(str.isdigit, species))

        # If no numeric characters are found, set the CHIANTI ionization level to 1
        chianti_level = int(ion_level) + 1 if ion_level else 1

        # Return the element symbol followed by the ionization level, separated
        # by an underscore (e.g., 'h_2')
        return f"{element}_{chianti_level}"
    # End of get chianti symbol ################################################

    # todo_keys ##############################################################
    def todo_keys(self):
        '''
        Function to obtain the todo keys for the ion.
        if neutral, no free-free contribution, the ket exclude 'ff'
        if the ion contribute free-bound emission, then the
        key include 'fb'.
        if the ion contributes line emissions, key include
        keywords 'line'

        :param ion_name:
        :param temperature:
        :return: keys
        '''

        ion_info = util.convertName(self.ion_name)
        ionstage = ion_info['Ion']
        charge = 1 - ionstage

        ion_list = []
        ion_list.append(self.ion_name)

        AbundanceName = 'unity'
        abundAll = chdata.Abundance[AbundanceName]['abundance']

        species = specTrails()  # species of the object of the class specTrails
        species.AbundAll = abundAll
        species.Temperature = self.temperature

        species.ionGate(ionList=ion_list, minAbund=None, doLines=True,
                        doContinuum=True, doWvlTest=0, doIoneqTest=0, verbose=False)

        keys = species.Todo[ion_list[0]]
        if charge == 0: keys = '_line_'
        return keys
    # End of todo_keys #########################################################

    # Cooling Table Function ###################################################
    def get_radiative_cooling(self, IncludeFreeFree=True, IncludeFreeBound=True,
                              IncludeLine=True, Include2photon=True):

        '''
                    Calculate the radiative loss rate as a function of temperature and
                    electron number density using Chianti atomic database.
                    '''

        # object for the class continuum
        if 'ff' in self.keys or 'fb' in self.keys:
            cont = ch.continuum(self.ion_name, self.temperature)

        if 'line' in self.keys:
            thisIon = ch.ion(ionStr=self.ion_name, temperature=self.temperature,
                             eDensity=self.eDensity, abundance='unity')

        # set rate tables to zero
        total_rate = np.zeros_like(self.temperature)
        freefree_rate = np.zeros_like(self.temperature)
        freebound_rate = np.zeros_like(self.temperature)
        boundbound_rate = np.zeros_like(self.temperature)
        twophoton_rate = np.zeros_like(self.temperature)

        # get relevant ion information
        Z = self.ion_info['Z']
        ionstage = self.ion_info['Ion']
        dielectronic = self.ion_info['Dielectronic']

        # Free-free loss rate ------------------------------------
        '''
        In this section we calculate the free-free energy loss 
        rate of an ion using the free-free radiative loss rate
        equation given by Eq. 5.15a of Ref[Rybicki and Lightman,
        1979,  Radiative Processes in Astrophysics]

        One may skip the neutral ions since the expression of 
        the rate goes like Z^2. 

        The calculated rates are returned to the FreeFreeLoss
        attributes with title temperature, rate, gf, prefactor
        '''
        if IncludeFreeFree and 'ff' in self.keys:
            cont.freeFreeLoss(includeAbund=False, includeIoneq=False)
            freefree_rate = cont.FreeFreeLoss['rate']
            total_rate += freefree_rate
        # End of Free-free loss rate -----------------------------

        # Free-bound loss rate -----------------------------------
        '''
        Calculate free-bound loss rate using Eq.1a of 106 is 
        integrated over wavelength to get the free-bound loss rate,
        where the free-bound Gaunt factor is given by Eq. 15 of 
        106 and is the numerical constant C_ff from Eq. 4 of 108.

        The rate is returned to FreeBoundLoss with attribute 'rate'.
        '''

        if IncludeFreeBound and 'fb' in self.keys:
            cont.freeBoundLoss(includeAbund=False, includeIoneq=False)
            freebound_rate = cont.FreeBoundLoss['rate']
            total_rate += freebound_rate
        # End of free-bound loss rate ----------------------------

        # line emission rate -------------------------------------
        '''
        Important Note: ChiantiPy uses a defalut ionization fraction to calculate
        the bound-bound loss. To get the correct cooling rate, we need to set the 
        ionization fraction to unity which then make the bound-bound loss rate 
        independent of ionization fraction. This is done by adding a line 
        thisIoneq = np.ones(ntempden, np.float64) 
        in ion.py -> method: boundBoundLoss
        '''
        if IncludeLine and 'line' in self.keys:
            # thisIon = ch.ion(ion_name, temperature, eDensity, abundance='unity')
            thisIon.intensity(allLines=0)
            thisIon.boundBoundLoss()
            boundbound_rate = thisIon.BoundBoundLoss['rate']
            total_rate += boundbound_rate

            if Include2photon and (Z - ionstage) in [0, 1] and not dielectronic:
                thisIon.twoPhotonLoss()
                twophoton_rate = thisIon.TwoPhotonLoss['rate']
                total_rate += twophoton_rate
        # End of line emission rate

        radiative_loss = {'temperature': self.temperature, 'ne': self.eDensity,
                          'ff-rate': freefree_rate, 'fb-rate': freebound_rate,
                          'bb-rate': boundbound_rate,
                          'twophoton-rate': twophoton_rate,
                          'total-rate': total_rate,
                          'ion_string': self.ion_string_name,
                          'Z': Z, 'Ion_stage': ionstage,
                          'Dielectronic': dielectronic,
                          'keys': self.keys
                          }

        del freefree_rate, freebound_rate, boundbound_rate, twophoton_rate, total_rate
        return radiative_loss

    # end of cooling table function ###################################

    # plot cooling table ##############################################
    def plot_cooling_rate(self, cooling_rate, plot_dir):
            '''
            plot cooling table for a specific ion with particular
            electron number density

            :param radiative_loss:
            :param keys:
            :param density_string:
            :return:
            '''

            temperature = cooling_rate['temperature']
            ne = cooling_rate['ne']
            ff_rate = cooling_rate['ff-rate']
            fb_rate = cooling_rate['fb-rate']
            bb_rate = cooling_rate['bb-rate']
            twophoton_rate = cooling_rate['twophoton-rate']
            total_rate = cooling_rate['total-rate']
            ion_name = cooling_rate['ion_string']
            Z = cooling_rate['Z']
            ionisation_stage = cooling_rate['Ion_stage']
            dielectronic = cooling_rate['Dielectronic']

            warnings.filterwarnings("ignore")
            ne_string = str(np.log10(ne))
            plt.figure()
            plt.title(f'{ion_name} Cooling Rate (Chianti v{ChiantiPy.__version__}) for log(nₑ) = {ne_string}')
            plt.xlabel('log(T) K')
            plt.ylabel('log($\Lambda$) erg cm^3 s^-1')
            plt.xlim([1, 9])
            plt.ylim([-30, -15])


            if 'ff' in self.keys:
                plt.plot(np.log10(temperature), np.log10(ff_rate), label='free-free')
            if 'fb' in self.keys:
                plt.plot(np.log10(temperature), np.log10(fb_rate), label='free-bound')
            if 'line' in self.keys:
                plt.plot(np.log10(temperature), np.log10(bb_rate), label='bound-bound')
                if (Z - ionisation_stage) in [0, 1] and not dielectronic:
                    plt.plot(np.log10(temperature), np.log10(twophoton_rate), label='two-photon')

            plt.plot(np.log10(temperature), np.log10(total_rate), label='total')
            plt.legend()
            filename = ion_name.replace('+', '') + '_logne' + ne_string.replace('.', '')
            outfile = os.path.join(plot_dir, filename + ".png")
            plt.savefig(outfile)
            plt.close()
    # end of plot cooling table ##############################################