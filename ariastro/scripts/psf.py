#!/usr/bin/env python
"""
Kadu code, This script should be probably run from the 'outputs' directory or similar
"""
from ariastro import *
import glob
import os
import numpy
PATH = "."
radius = 10
def main():
    global output_pattern, template, table
    # # Extract all galaxy names
    ff = glob.glob(os.path.join(PATH, "*.fits"))
    galaxy_names = []
    band_names = []
    field_names = []
    filenames = []
    for f in ff:
        filename = os.path.basename(f)
        fwhm, beta =  get_psf_data(filename)
        print(filename,fwhm,beta)
        make_psf(fwhm, beta, radius, "psf_" + filename)
        pieces = filename.split("_")
        galaxy_name = pieces[1]
        band_name = pieces[2]
        field_name = pieces[0]
        band_names.append(band_name)
        galaxy_names.append(galaxy_name)
        field_names.append(field_name)
        filenames.appen(filename)
    galaxy_names = list(set(galaxy_names))
    band_names  = list(set(band_names))
    field_names = list(set(field_names))
    filenames = list(set(filenames))

    igal = 0
#    for filename in filenames:
#        fwhm, beta =  get_psf_data(filename_test)
#        psf(fwhm, beta, radius, filename_test".psf")

if __name__ == "__main__":
    main()