# MotorsWalking

Version 0.1.0

# Introduction
MotorsWalking simulates how molecular motors stochastically walk along a infinite filament. These molecules stochastically bind to and unbind from a track. They walk along  the track by taking 8 nm steps that occure stochastically.
To solve the time evolution of the position of these motors a Gillespie algorithm is implemented. 

# Installation
### Prerequisites
- Phython 3.6.9
### Clone
```
$ git clone https://github.com/drflorianberger/motors.git
```
This will create a structure of the following folders:
### Project organization

```
.
├── .gitignore
├── CITATION.md
├── LICENSE.md
├── README.md
├── requirements.txt
├── bin                <- Compiled and external code, ignored by git (PG)
│   └── external       <- Any external source code, ignored by git (RO)
├── config             <- Configuration files (HW)
├── data               <- All project data, ignored by git
│   ├── processed      <- The final, canonical data sets for modeling. (PG)
│   ├── raw            <- The original, immutable data dump. (RO)
│   └── temp           <- Intermediate data that has been transformed. (PG)
├── docs               <- Documentation notebook for users (HW)
│   ├── manuscript     <- Manuscript source, e.g., LaTeX, Markdown, etc. (HW)
│   └── reports        <- Other project reports and notebooks (e.g. Jupyter, .Rmd) (HW)
├── results
│   ├── figures        <- Figures for the manuscript or reports (PG)
│   └── output         <- Other output for the manuscript or reports (PG)
└── src                <- Source code for this project (HW)

```
### Running
Go to ../motors/src/ and start
```
$ python Motors_walking.py
```
This will generate a figure with simulated trajectory which is stored in .../motors/results/figures/

### Running with Binder
https://mybinder.org/v2/gh/drflorianberger/motors/main

### Configuring
You can change the different parameters for the simulation in the config.ini file located in .../motors/config/

## License

This project is licensed under the terms of the [MIT License](/LICENSE.md)

## Citation

Please [cite this project as described here](/CITATION.md).
