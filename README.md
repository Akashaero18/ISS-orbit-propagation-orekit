# ISS Orbit Propagation with Orekit

## Description
- ISS Propagation Tool using Orekit. 
- Propagates ISS TLE, computes geodetic coordinates, and visualizes altitude and ground track over 24 hours.

## Features
- Propagates ISS orbit using TLE (Two-Line Element)
- Computes geodetic coordinates (latitude, longitude, altitude)
- Visualizes altitude variation and ground track over 24 hours

## Requirements
- Python 3.10
- Orekit (installed via conda-forge)
- NumPy, Matplotlib
- orekit-data.zip (must be in project directory)

## Installation
```bash
conda create -n orekit-env python=3.10
conda activate orekit-env
conda install -c conda-forge orekit numpy matplotlib
```

## Usage
```bash
python iss_leo_propagator.py
```

## Output
- **Left plot:** ISS altitude (geodetic height) over 24 hours
- **Right plot:** Ground track showing where ISS passes over Earth's surface

## Author
   Akash