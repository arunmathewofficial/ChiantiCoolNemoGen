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

## Author
Arun Mathew  
Astronomy & Astrophysics  
Computational and High Energy Astrophysics  
Dublin Institute for Advanced Studies (DIAS), Ireland  

