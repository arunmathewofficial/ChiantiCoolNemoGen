# PION Chianti Cooling Table Generator

Python code to calculate cooling table for NEMO using ChiantiPy.
CHIANTI provides a database of atomic data that can be used to interpret
the emission of spectral lines and continua emitted from
high-temperature, optically-thin astrophysical sources.
see: https://chiantipy.readthedocs.io/en/latest/api/ChiantiPy.core.html?highlight=FreeFree#id11

### Setting up the chianti environment variable in `.bashrc` file.

```bash
mathew@gamma2021:~$ touch file.bashrc
mathew@gamma2021:~$ chmod +x file.bashrc
mathew@gamma2021:~$ XUVTOP="/home/mathew/Chianti_database"
mathew@gamma2021:~$ export XUVTOP
mathew@gamma2021:~$ bash
mathew@gamma2021:~$ echo $XUVTOP
/home/mathew/Chianti_database/
```

### Creating a virtual environment
```bash
python3 -m venv venv   
source venv/bin/activate     
```

### installing ChiantiPy
```bash
python3 -m pip install ChiantiPy
```


pip install NebulaPy
# This will also install dependencies

# Download and set up the CHIANTI database (require ~1 GB disk space)
wget https://download.chiantidatabase.org/CHIANTI_10.1_database.tar.gz

# Extract it to a directory (~5 GB disk space required)
tar -xzf CHIANTI_10.1_database.tar.gz -C CHIANTI-DATABASE-DIRECTORY

# Add the following environmental variable to your .bashrc
echo "export XUVTOP=CHIANTI-DATABASE-DIRECTORY" >> ~/.bashrc

# Reload your .bashrc
source ~/.bashrc

# Install the Python-SILO interface:
# Execute the following command from the NebulaPy root directory.
install-silo

# Fix the SILO library path in your local distribution:
# Open the file:
#   ${HOME}/.local/venv/lib/python3.11/site-packages/pypion/SiloHeader_data.py
# Modify line 18 to append /lib to the path

# To download the NebulaPy database:
# Execute the following command from the NebulaPy root directory.
# If a destination path is not specified, the download will default to the
# root directory. This requires approximately 270 MB of additional space.
download-database [destination_path]

# Add environmental variable for NebulaPy Database
echo "export NEBULAPYDB=NEBULAPY-DATABASE-DIRECTORY" >> ~/.bashrc

# Reload your .bashrc
source ~/.bashrc
```

## Usage

For detailed usage instructions, examples, and features, please 
visit [NebulaPy Wiki](https://github.com/arunmathewofficial/NebulaPy/wiki). 
Sample scripts demonstrating NebulaPy functionalities can be found
in the `NebulaPy/problems` directory.


## Documentation

Check the full documentation at [NebulaPy GitHub](https://github.com/arunmathewofficial/NebulaPy).

## Support

For bug reports and feature requests, visit the
[issues section](https://github.com/arunmathewofficial/NebulaPy/issues) of the repository:

## Changelog
- **Version 1.0.0-beta** – March 5, 2025: Beta release
- **Version 1.0.1-beta** – March 6, 2025: Minor bug fixes
- **Version 1.0.2-beta** – March 6, 2025: Include silo installation script
- **Version 1.0.3-beta** – March 6, 2025: Fixed bugs in spectral line emissivity map script

## Author
Arun Mathew  
Astronomy & Astrophysics  
Computational and High Energy Astrophysics  
Dublin Institute for Advanced Studies (DIAS), Ireland  

