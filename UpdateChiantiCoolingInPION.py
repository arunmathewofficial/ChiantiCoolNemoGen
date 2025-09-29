import re
import os
import tool

# Main C++ file
nemo_chianti_cpp_file = "out/chianti_cooling.cpp"

# Path where all individual cooling table files are located
cooling_dir = "out/CoolingTabs"  # Replace with the correct folder

# List of ions
ion_list = ['H', 'H1+', 'He', 'He1+', 'He2+']

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
