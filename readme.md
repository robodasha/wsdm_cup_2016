# WSDM Cup 2016

In this repository you'll find the complete source codes which were used to produce our final submission to WSDM Cup 2016.

We used python, pandas, numpy and scipy and also HDF5 format and the pytables library for storing data.

## How to run:

1. Download and install Python 3.x ([https://www.python.org/downloads/](https://www.python.org/downloads/), project won't work with previous versions of Python)
2. Checkout the project and cd to the root directory
3. To install dependencies run `pip install -r requirements.txt`
4. Copy test data from `./test_data` into directory specified in wsdmcup/config.py
5. Run the project using `python3.x run.py` and follow the instructions:) You will need to first run steps 0-7 for the step 'rank' to work.