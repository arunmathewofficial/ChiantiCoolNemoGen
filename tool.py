import pandas as pd
import numpy as np
import os

# print to file ##########################################################
def print_to_file(data, ion, outdir):
    filename = ion.replace('+', '') + '_cooling_tab.txt'
    print(f' Writing {ion} cooling rates table to file {filename}')
    table = pd.DataFrame(data)
    outfile = os.path.join(outdir, filename)
    np.savetxt(outfile, table.values, fmt='%f')
    return table.values
# end of print to file  ################################################


# print to file nemo format  ###########################################
def nemo_format(table, ion, outdir):

    print(" Converting cooling table into NEMO format")
    Nrows = len(table)
    Ncols = len(table[0])

    print(" Source table contain " + str(Nrows) + " rows and " + str(Ncols) + " columns")
    filename = ion.replace('+', '') + '_cooling_tab.cpp'
    outfile = os.path.join(outdir, filename)
    outfile = open(outfile, "w")
    print(f" Saving cooling table in NEMO format: {filename}")
    outfile.write('chianti_cooling_tab_' + ion.replace('+', '') + ' = \n {')

    for i in range(0, Nrows):
        line = "{"
        for j in range(1, Ncols):
            line = line + '{:.3f}'.format(table[i, j])
            if j != (Ncols - 1): line = line + ", "
            if j == (Ncols - 1) and i != Nrows - 1: line = line + "}, "
            if j == (Ncols - 1) and i == Nrows - 1: line = line + "}"

        outfile.write(line)
    outfile.write("}")
    outfile.close()
# end of print to file nemo format  ####################################