import re
import os
import tool
import argparse

# Input Arguments ##########################################################
parser = argparse.ArgumentParser(
    description='Update Chianti Cooling Tables in NEMO C++ file',
    usage='script.py <nemo_chianti_cpp_file> <cooling_table_dir>')

parser.add_argument('nemo_chianti_cpp_file', help='path to nemo chianti cooling cpp file')
parser.add_argument('cooling_table_dir', help='directory containing generated cooling table cpp files')
args = parser.parse_args()

nemo_chianti_cpp_file = args.nemo_chianti_cpp_file
cooling_dir = args.cooling_table_dir

# List of ions
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


# Read the main C++ file
with open(nemo_chianti_cpp_file, 'r') as f:
    nemo_chianti_code = f.read()

for ion in ion_list:
    # Escape for regex
    escaped_ion = re.escape(ion)

    print(tool.CYAN + ' [Info] ' + tool.RESET + f"updating Chianti cooling data for {ion}")

    # Get the cooling table generated using ChiantiCoolNemoGen.py ##########################
    cooling_file = os.path.join(cooling_dir, f"{ion.split('+')[0]}_cooling_tab.cpp")
    if not os.path.exists(cooling_file):
        print(tool.RED + " [Error] " + tool.RESET + f"Cooling table for {ion} not found in {cooling_dir}")
        exit(1)
    else:
        print(tool.CYAN + ' [Info] ' + tool.RESET + f"{ion} cooling table file located: {cooling_file}")

    # Read the cooling table C++ file
    with open(cooling_file, 'r') as f:
        cooling_info = f.read()

    # Extract the array named chianti_cooling_tab_<ion>
    new_cooling_array_pattern  = r"chianti_cooling_tab_" + ion.replace('+', '') + r"\s*=\s*\{[\s\S]*?\};"
    extracted_cooling_array = re.search(new_cooling_array_pattern, cooling_info, re.DOTALL)

    if not extracted_cooling_array:
        print(tool.RED + " [Error] " + tool.RESET + f"{ion} cooling array not found in {cooling_file}")
    else:
        final_cooling_array = extracted_cooling_array.group(0).split('=')[1].strip()[:-1]  # remove trailing semicolon
        print(tool.CYAN + ' [Info] ' + tool.RESET + f"{ion} cooling array successfully extracted from the file.")
    # End of Get the cooling table generated using ChiantiCoolNemoGen.py ###################

    # Now update the Chianti NEMO C++ file #################################################
    # Find all occurrences of the ion
    pattern_name = rf"species\[\s*(\d+)\s*\]\.Name\s*=\s*\"{escaped_ion}\"\s*;"
    matches = list(re.finditer(pattern_name, nemo_chianti_code))

    if matches:
        for match in matches:
            index = match.group(1)
            # Replace the rate array for this index
            pattern_rate = re.compile(rf"(species\[{index}\]\.rate\s*=\s*)\{{.*?\}};", re.DOTALL)
            nemo_chianti_code = pattern_rate.sub(rf"\1{final_cooling_array};", nemo_chianti_code)
            print(tool.GREEN + ' [Info] ' + tool.RESET + f"{ion} cooling table {ion} updated successfully")
    else:
        print(tool.RED + " [Error] " + tool.RESET + f"Ion {ion} not found in NEMO Chianti file {nemo_chianti_cpp_file}")

    del extracted_cooling_array, final_cooling_array
# Write back updated C++ file
try:
    with open(nemo_chianti_cpp_file, 'w') as f:
        f.write(nemo_chianti_code)
    print(tool.GREEN + ' [Info] ' + tool.RESET + f"successfully wrote updated cooling data to {nemo_chianti_cpp_file}")
except Exception as e:
    print(f" Failed to write to {nemo_chianti_cpp_file}: {e}")
