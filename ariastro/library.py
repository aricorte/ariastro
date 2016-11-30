__all__ = ["get_dims", "load_jma_gri", "find_row_by_galaxy_name","find_row_by_galaxy_name2","read_output","create_output_table"]

import numpy as np

from astropy.io import fits
from collections import OrderedDict
import glob
import os
import re


def get_dims(filename):
    """Returns a tuple (width, height)"""
    hdulist = fits.open(filename)
    hdu = hdulist[0]
    ret = (hdu.header["NAXIS1"], hdu.header["NAXIS2"])
    hdulist.close()
    return ret
    

def load_jma_gri(filename):
    """Loads a file such as CALIFA-JMA-gri.mfmtk (it is a CSV file)

    Returns a numpy object q    q???
    """
    
    ret = []
    
    with open(filename, "r") as f:
        s = f.readline().strip()[1:].strip()
        
        fieldnames = s.split(",")
        
        for line in f:
            fieldvalues = line.strip().split(",")
            
            #for i in range(len(fieldvalues)):
            #    try:
            #        fieldvalues[i] = float(fieldvalues[i])
            #    except:
            #        pass

            row = OrderedDict()
            for key, value in zip(fieldnames, fieldvalues):
                row[key] = value
            ret.append(row)
    return ret
    
    
def find_row_by_galaxy_name(table, galaxy_name):
    """Returns dictionary, or None if not found"""
    ret = None
    for row in table:
        if row["rootname69_u"] == galaxy_name:
            ret = row
            break
    return ret

def find_row_by_galaxy_name2(table, galaxy_name):
    """Returns dictionary, or None if not found"""
    ret = None
    for row in table:
        if row["galaxy_name"] == galaxy_name:            
            ret = row
            break
    return ret
    
#   galaxy_name
#   
#   x0Fit2D_g, y0Fit2D_g
#   x0Fit2D_r, y0Fit2D_r
#   x0Fit2D_i, y0Fit2D_i


def read_output(filename):
    """
    Reads FITS file and extracts selected information from fifth frame header

    Returns: dictionary with keys as in sample header below, with the initial "2_" replaced by
             "B_" as in "Bulge"

    Header sample taken from ds9:
        2_XC_G  = '[146.4001]'         / X center [pixel]
        2_XC_R  = '[149.6384]'         / X center [pixel]
        2_XC_I  = '[146.7359]'         / X center [pixel]
        2_YC_G  = '[139.9570]'         / Y center [pixel]
        2_YC_R  = '[150.7310]'         / Y center [pixel]
        2_YC_I  = '[143.6689]'         / Y center [pixel]
        2_MAG_G = '15.7492 +/- 0.0026' / Integrated magnitude [mag]
        2_MAG_R = '15.6563 +/- 0.0024' / Integrated magnitude [mag]
        2_MAG_I = '15.0261 +/- 0.0030' / Integrated magnitude [mag]
        2_RE_G  = '27.5178 +/- 0.0701' / Effective radius Re [pixels]
        2_RE_R  = '27.9453 +/- 0.0505' / Effective radius Re [pixels]
        2_RE_I  = '28.3532 +/- 0.0839' / Effective radius Re [pixels]
        2_N_G   = '0.7177 +/- 0.0051'  / Sersic index
        2_N_R   = '0.7633 +/- 0.0035'  / Sersic index
        2_N_I   = '0.8069 +/- 0.0060'  / Sersic index
        2_AR_G  = '0.9221 +/- 0.0014'  / Axis ratio (b/a)
        2_AR_R  = '0.9221 +/- 0.0014'  / Axis ratio (b/a)
        2_AR_I  = '0.9221 +/- 0.0014'  / Axis ratio (b/a)
        2_PA_G  = '-64.7095 +/- 1.0063' / Position Angle (PA) [degrees: Up=0, Left=90]
        2_PA_R  = '-64.7095 +/- 1.0063' / Position Angle (PA) [degrees: Up=0, Left=90]
        2_PA_I  = '-64.7095 +/- 1.0063' / Position Angle (PA) [degrees: Up=0, Left=90]

    >>> ret = read_output("CGCG163-062_ss.fits")
    >>> print(ret)
    OrderedDict([('2_XC_G', '[146.4001]'), ('2_XC_R', '[149.6384]'), ('2_XC_I', '[146.7359]'), ('2_YC_G', '[139.9570]'), ('2_YC_R', '[150.7310]'), ('2_YC_I', '[143.6689]'), ('2_MAG_G', '15.7492 +/- 0.0026'), ('2_MAG_R', '15.6563 +/- 0.0024'), ('2_MAG_I', '15.0261 +/- 0.0030'), ('2_RE_G', '27.5178 +/- 0.0701'), ('2_RE_R', '27.9453 +/- 0.0505'), ('2_RE_I', '28.3532 +/- 0.0839'), ('2_N_G', '0.7177 +/- 0.0051'), ('2_N_R', '0.7633 +/- 0.0035'), ('2_N_I', '0.8069 +/- 0.0060'), ('2_AR_G', '0.9221 +/- 0.0014'), ('2_AR_R', '0.9221 +/- 0.0014'), ('2_AR_I', '0.9221 +/- 0.0014'), ('2_PA_G', '-64.7095 +/- 1.0063'), ('2_PA_R', '-64.7095 +/- 1.0063'), ('2_PA_I', '-64.7095 +/- 1.0063')])
    """


    fields_to_extract = ["2_XC_U", "2_XC_G", "2_XC_R", "2_XC_I","2_XC_Z","2_YC_U", "2_YC_G", "2_YC_R", "2_YC_I", "2_YC_Z", "2_MAG_U", "2_MAG_G",
                         "2_MAG_R", "2_MAG_I", "2_MAG_Z", "2_RE_U", "2_RE_G", "2_RE_R", "2_RE_I", "2_RE_Z", "2_N_U", "2_N_G", "2_N_R",
                         "2_N_I", "2_N_Z", "2_AR_U", "2_AR_G", "2_AR_R", "2_AR_I", "2_AR_Z", "2_PA_U", "2_PA_G", "2_PA_R", "2_PA_I", "2_PA_Z",
                         "1_SKY_0","1_SKY_1","1_SKY_2","1_SKY_3","1_SKY_4"]
    hdulist = fits.open(filename)

    ret = OrderedDict()
    for name in fields_to_extract:
        expr = hdulist[7].header[name]

        # Matches pattern such as '15.7492 +/- 0.0026'
        gg = re.match("([0-9.-]+)\s*\+/-\s*([0-9.-]+)", expr)

        if gg is not None:
            value, error = gg.groups()
            # We know that it is a (value, error) pair
        elif expr.startswith("["):
            value = expr.strip()[1:-1]
            error = '0.'
        else:
            value = expr
            error = '0.'

        ret[name] = value
        ret[name + "_ERROR"] = error

    hdulist.close()
    return ret


def read_output_chi2(filename):
    """
    Reads FITS file and extracts selected information from last frame header

    Returns: chi2, chi2_min, niter,cputime_setup,cputime_fit,cpu_time_total

    """


    fields_to_extract = ["2_XC_G", "2_XC_R", "2_XC_I", "2_YC_G", "2_YC_R", "2_YC_I", "2_MAG_G",
                         "2_MAG_R", "2_MAG_I", "2_RE_G", "2_RE_R", "2_RE_I", "2_N_G", "2_N_R",
                         "2_N_I", "2_AR_G", "2_AR_R", "2_AR_I", "2_PA_G", "2_PA_R", "2_PA_I",
                         "1_SKY_0","1_SKY_1","1_SKY_2"]

    fields_to_extract_chi = ["NITER", "CPUTIME_SETUP", "CPUTIME_FIT", "CPUTIME_TOTAL", "CHISQ", "CHI2NU",]

    ret = OrderedDict()

    hdulist = fits.open(filename)

    # PART 1
    for name in fields_to_extract:
        expr = hdulist[4].header[name]

        # Matches pattern such as '15.7492 +/- 0.0026'
        gg = re.match("([0-9.-]+)\s*\+/-\s*([0-9.-]+)", expr)

        if gg is not None:
            value, error = gg.groups()
            # We know that it is a (value, error) pair
        elif expr.startswith("["):
            value = expr.strip()[1:-1]
            error = '0.'
        else:
            value = expr
            error = '0.'

        ret[name] = value
        ret[name + "_ERROR"] = error

        #print ret

    # PART 2
    for frame in hdulist:
        data = frame.data

        if not isinstance(data, fits.fitsrec.FITS_rec):
            continue

        # frame is a candidate here

        names = data.names

        good = True
        for desired_field in fields_to_extract_chi:
            if not desired_field in names:
                good = False
                break

        if not good:
            continue

        # we found the frame

        for desired_field in fields_to_extract_chi:
            temp = str(data[desired_field]).strip()

            # removes brackets in case it is a number between brackets
            if temp.startswith("["):
                temp = temp[1:-1].strip()

            ret[desired_field] = temp

            # ret[desired_field] = str(data[desired_field])

    #print ret
    #if ret.startswith("["):
    #        value = ret.strip()[1:-1]
            
    #print ret        
    hdulist.close()
    return ret


def create_output_table(dir_=".", output_filename="output-mega-califa.txt"):
    """
    Reads all files in directory specified and saves as a txt file

    Returns: number of fits files written

    >>> create_output_table(".")
    3
    """

    files = glob.glob(os.path.join(dir_, "*.fits"))
    print files
    n = 0
    with open(os.path.join(dir_, output_filename), "w") as out:
        for filename in files:
            galaxy_name = os.path.split(filename)[1].split("_")[0]

            try:
                data = read_output(filename)
            except Exception as e:
                print "Error dealing with file '{}': {}: {}".format(filename, e.__class__.__name__, str(e))
                continue

            #data = read_output_chi2(filename)

            if n == 0:
                out.write("#" " "+"galaxy_name"+" "+" ".join(data.keys())+"\n")

            out.write(galaxy_name+" "+" ".join(data.values())+"\n")

            n += 1

    return n






def dump_header(filename):
    """
    Reads FITS file and dumps all headers into a text file named <filename>.txt
    """

    hdulist = fits.open(filename)
    
    output_filename = filename+".txt"
    
    with open(output_filename, "w") as f:
        i = 0
        for hdu in hdulist:
            f.write("\n\n***** FRAME %02d *****\n" % i)
            f.write(repr(hdu.header)+"\n")
            i += 1


