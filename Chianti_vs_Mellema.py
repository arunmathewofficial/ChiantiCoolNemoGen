

import pandas as pd
import matplotlib.pyplot as plt

# Specify the file path
Mellema_path = 'Orig-Mellema-Cool-Tab/H0-cool.tab'
Nemo_cooling_tab = 'Chianti-No-BB/h_1.txt'


# Read the data into a DataFrame
Mellema_data = pd.read_csv(Mellema_path, delim_whitespace=True, header=None, skiprows=1)
Nemo_data = pd.read_csv(Nemo_cooling_tab, delim_whitespace=True, header=None)

Mellema_logT = Mellema_data[0]
Mellema_rate = Mellema_data[1]

Nemo_logT = Nemo_data[0]
Nemo_rate = Nemo_data[1]

# Plot the data
plt.figure(figsize=(8, 6))
#plt.plot(pion_chianti_logT, pion_chianti_rate, linestyle='-', color='crimson', label='Chianti including BB')
plt.plot(Mellema_logT, Mellema_rate, linestyle='--', color='crimson', label='Raga et al. 1997')
plt.plot(Nemo_logT, Nemo_rate, linestyle='-', color='darkblue', label='NEMO v1.0')
# Add labels, title, and legend
plt.xlabel('log T (K) Label', fontsize=12)
plt.ylabel('log($\Lambda$) erg cm^3 s^-1', fontsize=12)
plt.legend()

# Display the plot
plt.grid(True)
plt.savefig('compare.png')
