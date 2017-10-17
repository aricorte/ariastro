__all__ = ["get_dims", "load_jma_gri", "find_row_by_galaxy_name", "find_row_by_galaxy_name2", "read_output",
           "create_output_table", "get_exptime", "write_bad_fit", "write_not_run","get_x0y0","fromNMAGYtoCOUNTs"]

import numpy as np

from astropy.io import fits
from collections import OrderedDict
import glob
import os
import re
import multiprocessing as mp

FILENAME_NOT_RUN = "not-run.csv"
FILENAME_BAD_FIT = "bad-fit.csv"
_file_not_run = open(FILENAME_NOT_RUN, "w")
_file_bad_fit = open(FILENAME_BAD_FIT, "w")


def write_not_run(galaxy_name, s):
    _file_not_run.write('%-40s,"%s"\n' % (galaxy_name, s))


def write_bad_fit(galaxy_name, s):
    _file_bad_fit.write('%-40s,"%s"\n' % (galaxy_name, s))


def get_dims(filename):
    """Returns a tuple (width, height)"""
    hdulist = fits.open(filename)
    hdu = hdulist[0]
    ret = (hdu.header["NAXIS1"], hdu.header["NAXIS2"])
    hdulist.close()
    return ret


def get_exptime(filename):
    """Returns exposure-time from image header"""
    hdulist = fits.open(filename)
    hdu = hdulist[0]
    ret = hdu.header["EXPTIME"]
    hdulist.close()
    return ret

def get_x0y0(filename):
    """Returns x0,y0 from image header"""
    hdulist = fits.open(filename)
    hdu = hdulist[0]
    ret = (hdu.header["OBJXPIX"],hdu.header["OBJYPIX"])
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

            # for i in range(len(fieldvalues)):
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
    Reads FITS file and extracts selected information from penultimate frame data

    Returns:
        dictionary: a "flattened" version of the table data in the penultimate frame of the FITS file.
                    The keys are <original field name in numpy array>_<band letter>, for example: "COMP1_XC_U"
                    (field was "COMP1_XC" and band is "U")


    hdulist[-2].data sample:

        FITS_rec([ ('u', 430.0, 0.0, 0, 430.0, 0.0, 0, -0.0012000001, 0.0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 430.76367, 0.43971181, 1, 437.45587, 2.3212292, 1, 18.2036, 0.039023668, 1, 70.497238, 1.6941882, 1, 0.33186108, 0.025464246, 1, 0.19848995, 0.0050456659, 1, 1.8755809, 0.40784442, 1),
                   ('g', 430.0, 0.0, 0, 430.0, 0.0, 0, -0.00066999998, 0.0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 430.4393, 0.26242495, 1, 438.08072, 1.1981732, 1, 17.397177, 0.020027174, 1, 68.003441, 0.8296113, 1, 0.41161668, 0.011642374, 1, 0.22190171, 0.0025764173, 1, 2.1990237, 0.21120539, 1),
                   ('r', 430.0, 0.0, 0, 430.0, 0.0, 0, -0.00023000001, 0.0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 429.79575, 0.22847107, 1, 435.85583, 1.0234721, 1, 16.614887, 0.016775975, 1, 64.772774, 0.56382304, 1, 0.50353318, 0.010757586, 1, 0.23668186, 0.0020852997, 1, 2.4045742, 0.17398277, 1),
                   ('i', 430.0, 0.0, 0, 430.0, 0.0, 0, -0.00211, 0.0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 430.63159, 0.18267216, 1, 435.00528, 0.76906836, 1, 15.907736, 0.014295106, 1, 61.425461, 0.57469875, 1, 0.58814436, 0.010949646, 1, 0.23751204, 0.0020082004, 1, 2.4187121, 0.16746925, 1),
                   ('z', 430.0, 0.0, 0, 430.0, 0.0, 0, -0.00056999997, 0.0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 430.80585, 0.17817506, 1, 432.51694, 0.80425751, 1, 14.291779, 0.016046198, 1, 57.510559, 0.84336847, 1, 0.67633432, 0.02100935, 1, 0.22380203, 0.0031048364, 1, 2.2337053, 0.25965932, 1)],
                  dtype=(numpy.record, [('BAND', 'S17'), ('COMP1_XC', '>f4'), ('COMP1_XC_ERR', '>f4'), ('COMP1_XC_FIT', '>i4'), ('COMP1_YC', '>f4'), ('COMP1_YC_ERR', '>f4'), ('COMP1_YC_FIT', '>i4'), ('COMP1_SKY', '>f4'), ('COMP1_SKY_ERR', '>f4'), ('COMP1_SKY_FIT', '>i4'), ('COMP1_DSDX', '>f4'), ('COMP1_DSDX_ERR', '>f4'), ('COMP1_DSDX_FIT', '>i4'), ('COMP1_DSDY', '>f4'), ('COMP1_DSDY_ERR', '>f4'), ('COMP1_DSDY_FIT', '>i4'), ('COMP2_XC', '>f4'), ('COMP2_XC_ERR', '>f4'), ('COMP2_XC_FIT', '>i4'), ('COMP2_YC', '>f4'), ('COMP2_YC_ERR', '>f4'), ('COMP2_YC_FIT', '>i4'), ('COMP2_MAG', '>f4'), ('COMP2_MAG_ERR', '>f4'), ('COMP2_MAG_FIT', '>i4'), ('COMP2_Re', '>f4'), ('COMP2_Re_ERR', '>f4'), ('COMP2_Re_FIT', '>i4'), ('COMP2_n', '>f4'), ('COMP2_n_ERR', '>f4'), ('COMP2_n_FIT', '>i4'), ('COMP2_AR', '>f4'), ('COMP2_AR_ERR', '>f4'), ('COMP2_AR_FIT', '>i4'), ('COMP2_PA', '>f4'), ('COMP2_PA_ERR', '>f4'), ('COMP2_PA_FIT', '>i4')]))

    Usage example:

        >>> ret = read_output("CGCG163-062_ss.fits")
        >>> print(ret)
        TODO get output and paste here
    """

    print(("Processing file '{}'".format(filename)))

    hdulist = fits.open(filename)
    data = hdulist[-2].data
    fields_to_extract = [field_name for field_name, __ in data.dtype.descr][1:]
    band_names = [x.upper() for x in data["BAND"]]

    ret = OrderedDict()
    for field_name in fields_to_extract:
        for i, band_name in enumerate(band_names):
            ret[field_name+"_"+band_name] = data[i][field_name]

            # expr = hdulist[-2].header[field_name]
            #
            # # if expr.startswith("*"):
            # if "*" in expr:
            #     msg = "Invalid value for header '{}': '{}'".format(field_name, expr)
            #     raise RuntimeError(msg)
            #     # flag_invalid = True
            #     # break
            #     # print expr, name, filename
            #     # continue
            #
            # # Matches pattern such as '15.7492 +/- 0.0026'
            # gg = re.match("([0-9.-]+)\s*\+/-\s*([0-9.-]+)", expr)
            #
            # if gg is not None:
            #     value, error = gg.groups()
            #     # We know that it is a (value, error) pair
            #     # print expr
            #
            # elif expr.startswith("["):
            #     value = expr.strip()[1:-1]
            #     error = '0.'
            # else:
            #     value = expr
            #     error = '0.'
            #
            # ret[field_name] = value
            # ret[field_name + "_ERROR"] = error

    hdulist.close()

    return ret

def read_output_chi2(filename):
    """
    Reads FITS file and extracts selected information from penultimate frame data

    Returns:
        dictionary: a "flattened" version of the table data in the penultimate frame of the FITS file.
                    The keys are <original field name in numpy array>_<band letter>, for example: "COMP1_XC_U"
                    (field was "COMP1_XC" and band is "U")


    hdulist[-2].data sample:

        FITS_rec([ ('u', 430.0, 0.0, 0, 430.0, 0.0, 0, -0.0012000001, 0.0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 430.76367, 0.43971181, 1, 437.45587, 2.3212292, 1, 18.2036, 0.039023668, 1, 70.497238, 1.6941882, 1, 0.33186108, 0.025464246, 1, 0.19848995, 0.0050456659, 1, 1.8755809, 0.40784442, 1),
                   ('g', 430.0, 0.0, 0, 430.0, 0.0, 0, -0.00066999998, 0.0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 430.4393, 0.26242495, 1, 438.08072, 1.1981732, 1, 17.397177, 0.020027174, 1, 68.003441, 0.8296113, 1, 0.41161668, 0.011642374, 1, 0.22190171, 0.0025764173, 1, 2.1990237, 0.21120539, 1),
                   ('r', 430.0, 0.0, 0, 430.0, 0.0, 0, -0.00023000001, 0.0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 429.79575, 0.22847107, 1, 435.85583, 1.0234721, 1, 16.614887, 0.016775975, 1, 64.772774, 0.56382304, 1, 0.50353318, 0.010757586, 1, 0.23668186, 0.0020852997, 1, 2.4045742, 0.17398277, 1),
                   ('i', 430.0, 0.0, 0, 430.0, 0.0, 0, -0.00211, 0.0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 430.63159, 0.18267216, 1, 435.00528, 0.76906836, 1, 15.907736, 0.014295106, 1, 61.425461, 0.57469875, 1, 0.58814436, 0.010949646, 1, 0.23751204, 0.0020082004, 1, 2.4187121, 0.16746925, 1),
                   ('z', 430.0, 0.0, 0, 430.0, 0.0, 0, -0.00056999997, 0.0, 0, 0.0, 0.0, 0, 0.0, 0.0, 0, 430.80585, 0.17817506, 1, 432.51694, 0.80425751, 1, 14.291779, 0.016046198, 1, 57.510559, 0.84336847, 1, 0.67633432, 0.02100935, 1, 0.22380203, 0.0031048364, 1, 2.2337053, 0.25965932, 1)],
                  dtype=(numpy.record, [('BAND', 'S17'), ('COMP1_XC', '>f4'), ('COMP1_XC_ERR', '>f4'), ('COMP1_XC_FIT', '>i4'), ('COMP1_YC', '>f4'), ('COMP1_YC_ERR', '>f4'), ('COMP1_YC_FIT', '>i4'), ('COMP1_SKY', '>f4'), ('COMP1_SKY_ERR', '>f4'), ('COMP1_SKY_FIT', '>i4'), ('COMP1_DSDX', '>f4'), ('COMP1_DSDX_ERR', '>f4'), ('COMP1_DSDX_FIT', '>i4'), ('COMP1_DSDY', '>f4'), ('COMP1_DSDY_ERR', '>f4'), ('COMP1_DSDY_FIT', '>i4'), ('COMP2_XC', '>f4'), ('COMP2_XC_ERR', '>f4'), ('COMP2_XC_FIT', '>i4'), ('COMP2_YC', '>f4'), ('COMP2_YC_ERR', '>f4'), ('COMP2_YC_FIT', '>i4'), ('COMP2_MAG', '>f4'), ('COMP2_MAG_ERR', '>f4'), ('COMP2_MAG_FIT', '>i4'), ('COMP2_Re', '>f4'), ('COMP2_Re_ERR', '>f4'), ('COMP2_Re_FIT', '>i4'), ('COMP2_n', '>f4'), ('COMP2_n_ERR', '>f4'), ('COMP2_n_FIT', '>i4'), ('COMP2_AR', '>f4'), ('COMP2_AR_ERR', '>f4'), ('COMP2_AR_FIT', '>i4'), ('COMP2_PA', '>f4'), ('COMP2_PA_ERR', '>f4'), ('COMP2_PA_FIT', '>i4')]))

    Usage example:

        >>> ret = read_output("CGCG163-062_ss.fits")
        >>> print(ret)
        TODO get output and paste here
    """

    print(("Processing file '{}'".format(filename)))

    hdulist = fits.open(filename)
    data = hdulist[-4].data
    fields_to_extract = [field_name for field_name, __ in data.dtype.descr][1:-1]
#    band_names = [x.upper() for x in data["BAND"]]

    ret = OrderedDict()
    for field_name in fields_to_extract:
#        for i, band_name in enumerate(band_names):
        ret[field_name] = data[field_name]
            # expr = hdulist[-2].header[field_name]
            #
            # # if expr.startswith("*"):
            # if "*" in expr:
            #     msg = "Invalid value for header '{}': '{}'".format(field_name, expr)
            #     raise RuntimeError(msg)
            #     # flag_invalid = True
            #     # break
            #     # print expr, name, filename
            #     # continue
            #
            # # Matches pattern such as '15.7492 +/- 0.0026'
            # gg = re.match("([0-9.-]+)\s*\+/-\s*([0-9.-]+)", expr)
            #
            # if gg is not None:
            #     value, error = gg.groups()
            #     # We know that it is a (value, error) pair
            #     # print expr
            #
            # elif expr.startswith("["):
            #     value = expr.strip()[1:-1]
            #     error = '0.'
            # else:
            #     value = expr
            #     error = '0.'
            #
            # ret[field_name] = value
            # ret[field_name + "_ERROR"] = error

    hdulist.close()

    return ret

def read_output_bd(filename):
    """
    Not useful anymore, read_output.py does everything

    Reads FITS file and extracts selected information from fifth frame header

    Returns: dictionary with keys as in sample header below, with the initial "2_" replaced by
             "B_" as in "Bulge"

    2_XC_U  = '249.2548 +/- 0.0382' / X center [pixel]
    2_XC_G  = '249.6460 +/- 0.0382' / X center [pixel]
    2_XC_R  = '248.8654 +/- 0.0382' / X center [pixel]
    2_XC_I  = '248.8550 +/- 0.0382' / X center [pixel]
    2_XC_Z  = '249.0299 +/- 0.0382' / X center [pixel]
    2_YC_U  = '249.3147 +/- 0.0516' / Y center [pixel]
    2_YC_G  = '249.4742 +/- 0.0516' / Y center [pixel]
    2_YC_R  = '249.0633 +/- 0.0516' / Y center [pixel]
    2_YC_I  = '249.1092 +/- 0.0516' / Y center [pixel]
    2_YC_Z  = '249.0897 +/- 0.0516' / Y center [pixel]
    2_MAG_U = '19.3482 +/- 0.1520' / Integrated magnitude [mag]
    2_MAG_G = '17.9082 +/- 0.0691' / Integrated magnitude [mag]
    2_MAG_R = '16.5893 +/- 0.0465' / Integrated magnitude [mag]
    2_MAG_I = '15.5702 +/- 0.0393' / Integrated magnitude [mag]
    2_MAG_Z = '13.4458 +/- 0.0312' / Integrated magnitude [mag]
    2_RE_U  = '8.3340 +/- 1.1544'  / Effective radius Re [pixels]
    2_RE_G  = '7.7037 +/- 0.6040'  / Effective radius Re [pixels]
    2_RE_R  = '7.7923 +/- 0.4497'  / Effective radius Re [pixels]
    2_RE_I  = '8.7270 +/- 0.4563'  / Effective radius Re [pixels]
    2_RE_Z  = '10.6748 +/- 0.4463' / Effective radius Re [pixels]
    2_N_U   = '1.5647 +/- 0.2898'  / Sersic index
    2_N_G   = '1.9657 +/- 0.1551'  / Sersic index
    2_N_R   = '2.2742 +/- 0.1139'  / Sersic index
    2_N_I   = '2.3974 +/- 0.1062'  / Sersic index
    2_N_Z   = '2.3424 +/- 0.0838'  / Sersic index
    2_AR_U  = '0.6018 +/- 0.0082'  / Axis ratio (b/a)
    2_AR_G  = '0.6018 +/- 0.0082'  / Axis ratio (b/a)
    2_AR_I  = '0.6018 +/- 0.0082'  / Axis ratio (b/a)
    2_AR_Z  = '0.6018 +/- 0.0082'  / Axis ratio (b/a)
    2_AR_R  = '0.6018 +/- 0.0082'  / Axis ratio (b/a)
    2_PA_U  = '-34.6905 +/- 1.0838' / Position Angle (PA) [degrees: Up=0, Left=90]
    2_PA_G  = '-34.6905 +/- 1.0838' / Position Angle (PA) [degrees: Up=0, Left=90]
    2_PA_R  = '-34.6905 +/- 1.0838' / Position Angle (PA) [degrees: Up=0, Left=90]
    2_PA_I  = '-34.6905 +/- 1.0838' / Position Angle (PA) [degrees: Up=0, Left=90]
    2_PA_Z  = '-34.6905 +/- 1.0838' / Position Angle (PA) [degrees: Up=0, Left=90]
    COMMENT ------------------------------------------------------------------------
    3_XC_U  = '248.6784 +/- 0.1768' / X center [pixel]
    3_XC_G  = '249.0696 +/- 0.1768' / X center [pixel]
    3_XC_R  = '248.2890 +/- 0.1768' / X center [pixel]
    3_XC_I  = '248.2786 +/- 0.1768' / X center [pixel]
    3_XC_Z  = '248.4535 +/- 0.1768' / X center [pixel]
    3_YC_U  = '248.9206 +/- 0.2522' / Y center [pixel]
    3_YC_G  = '249.0801 +/- 0.2522' / Y center [pixel]
    3_YC_R  = '248.6692 +/- 0.2522' / Y center [pixel]
    3_YC_I  = '248.7151 +/- 0.2522' / Y center [pixel]
    3_YC_Z  = '248.6956 +/- 0.2522' / Y center [pixel]
    3_MAG_U = '19.0583 +/- 0.1125' / Integrated magnitude
    3_MAG_G = '17.2588 +/- 0.0366' / Integrated magnitude
    3_MAG_R = '15.9627 +/- 0.0238' / Integrated magnitude
    3_MAG_I = '15.0478 +/- 0.0225' / Integrated magnitude
    3_MAG_Z = '13.3756 +/- 0.0270' / Integrated magnitude
    3_RS_U  = '14.4636 +/- 0.4146' / Scalelength [pixels]
    3_RS_G  = '17.4697 +/- 0.2682' / Scalelength [pixels]
    3_RS_R  = '21.0490 +/- 0.1447' / Scalelength [pixels]
    3_RS_I  = '24.4642 +/- 0.2031' / Scalelength [pixels]
    3_RS_Z  = '28.1612 +/- 0.3731' / Scalelength [pixels]
    3_AR_U  = '0.6051 +/- 0.0054'  / Axis ratio (b/a)
    3_AR_G  = '0.6051 +/- 0.0054'  / Axis ratio (b/a)
    3_AR_R  = '0.6051 +/- 0.0054'  / Axis ratio (b/a)
    3_AR_I  = '0.6051 +/- 0.0054'  / Axis ratio (b/a)
    3_AR_Z  = '0.6051 +/- 0.0054'  / Axis ratio (b/a)
    3_PA_U  = '5.9352 +/- 0.6999'  / Position Angle (PA) [degrees: Up=0, Left=90]
    3_PA_G  = '5.9352 +/- 0.6999'  / Position Angle (PA) [degrees: Up=0, Left=90]
    3_PA_R  = '5.9352 +/- 0.6999'  / Position Angle (PA) [degrees: Up=0, Left=90]
    3_PA_I  = '5.9352 +/- 0.6999'  / Position Angle (PA) [degrees: Up=0, Left=90]
    3_PA_Z  = '5.9352 +/- 0.6999'  / Position Angle (PA) [degrees: Up=0, Left=90]

    >>> ret = read_output("CGCG163-062_bd.fits")
    >>> print(ret)
    OrderedDict([('2_XC_G', '[146.4001]'), ('2_XC_R', '[149.6384]'), ('2_XC_I', '[146.7359]'), ('2_YC_G', '[139.9570]'), ('2_YC_R', '[150.7310]'), ('2_YC_I', '[143.6689]'), ('2_MAG_G', '15.7492 +/- 0.0026'), ('2_MAG_R', '15.6563 +/- 0.0024'), ('2_MAG_I', '15.0261 +/- 0.0030'), ('2_RE_G', '27.5178 +/- 0.0701'), ('2_RE_R', '27.9453 +/- 0.0505'), ('2_RE_I', '28.3532 +/- 0.0839'), ('2_N_G', '0.7177 +/- 0.0051'), ('2_N_R', '0.7633 +/- 0.0035'), ('2_N_I', '0.8069 +/- 0.0060'), ('2_AR_G', '0.9221 +/- 0.0014'), ('2_AR_R', '0.9221 +/- 0.0014'), ('2_AR_I', '0.9221 +/- 0.0014'), ('2_PA_G', '-64.7095 +/- 1.0063'), ('2_PA_R', '-64.7095 +/- 1.0063'), ('2_PA_I', '-64.7095 +/- 1.0063')])
    """

    fields_to_extract = ["2_XC_U", "2_XC_G", "2_XC_R", "2_XC_I", "2_XC_Z", "2_YC_U", "2_YC_G", "2_YC_R", "2_YC_I",
                         "2_YC_Z", "2_MAG_U", "2_MAG_G",
                         "2_MAG_R", "2_MAG_I", "2_MAG_Z", "2_RE_U", "2_RE_G", "2_RE_R", "2_RE_I", "2_RE_Z", "2_N_U",
                         "2_N_G", "2_N_R",
                         "2_N_I", "2_N_Z", "2_AR_U", "2_AR_G", "2_AR_R", "2_AR_I", "2_AR_Z", "2_PA_U", "2_PA_G",
                         "2_PA_R", "2_PA_I", "2_PA_Z",
                         "1_SKY_0", "1_SKY_1", "1_SKY_2", "1_SKY_3", "1_SKY_4", "3_XC_U", "3_XC_G", "3_XC_R", "3_XC_I",
                         "3_XC_Z", "3_YC_U", "3_YC_G", "3_YC_R", "3_YC_I", "3_YC_Z", "3_MAG_U", "3_MAG_G",
                         "3_MAG_R", "3_MAG_I", "3_MAG_Z", "3_RS_U", "3_RS_G", "3_RS_R", "3_RS_I", "3_RS_Z", "3_AR_U",
                         "3_AR_G", "3_AR_R", "3_AR_I", "3_AR_Z", "3_PA_U", "3_PA_G", "3_PA_R", "3_PA_I",
                         "3_PA_Z"]
    hdulist = fits.open(filename)

    ret = OrderedDict()
    flag_invalid = False  # will be set to True if any values has a "*"
    for name in fields_to_extract:
        expr = hdulist[7].header[name]
        # if expr.startswith("*"):
        if "*" in expr:
            msg = "Invalid value for header '{}': '{}'".format(name, expr)
            raise RuntimeError(msg)
            # flag_invalid = True
            # break
            # print expr, name, filename
            # continue

        # Matches pattern such as '15.7492 +/- 0.0026'
        gg = re.match("([0-9.-]+)\s*\+/-\s*([0-9.-]+)", expr)

        if gg is not None:
            value, error = gg.groups()
            # We know that it is a (value, error) pair
            # print expr

        elif expr.startswith("["):
            value = expr.strip()[1:-1]
            error = '0.'
        else:
            value = expr
            error = '0.'

        ret[name] = value
        ret[name + "_ERROR"] = error

    hdulist.close()

    # if flag_invalid:
    #    return None

    return ret


# def read_output_chi2(filename):
#     """
#     Reads FITS file and extracts selected information from last frame header
#
#     Returns: chi2, chi2_min, niter,cputime_setup,cputime_fit,cpu_time_total
#
#     """
#
#  #   fields_to_extract = ["2_XC_G", "2_XC_R", "2_XC_I", "2_YC_G", "2_YC_R", "2_YC_I", "2_MAG_G",
#                          "2_MAG_R", "2_MAG_I", "2_RE_G", "2_RE_R", "2_RE_I", "2_N_G", "2_N_R",
#                          "2_N_I", "2_AR_G", "2_AR_R", "2_AR_I", "2_PA_G", "2_PA_R", "2_PA_I",
#                          "1_SKY_0", "1_SKY_1", "1_SKY_2"]
#
#  #   fields_to_extract_chi = ["NITER", "CPUTIME_SETUP", "CPUTIME_FIT", "CPUTIME_TOTAL", "CHISQ", "CHI2NU", ]
#
#     ret = OrderedDict()
#
#     hdulist = fits.open(filename)
#
#     # PART 1
#     for name in fields_to_extract:
#         expr = hdulist[4].header[name]
#
#         # Matches pattern such as '15.7492 +/- 0.0026'
#         gg = re.match("([0-9.-]+)\s*\+/-\s*([0-9.-]+)", expr)
#
#         if gg is not None:
#             value, error = gg.groups()
#             # We know that it is a (value, error) pair
#         elif expr.startswith("["):
#             value = expr.strip()[1:-1]
#             error = '0.'
#         else:
#             value = expr
#             error = '0.'
#
#         ret[name] = value
#         ret[name + "_ERROR"] = error
#
#         # print ret
#
#     # PART 2
#     for frame in hdulist:
#         data = frame.data
#
#         if not isinstance(data, fits.fitsrec.FITS_rec):
#             continue
#
#         # frame is a candidate here
#
#         names = data.names
#
#         good = True
#         for desired_field in fields_to_extract_chi:
#             if not desired_field in names:
#                 good = False
#                 break
#
#         if not good:
#             continue
#
#         # we found the frame
#
#         for desired_field in fields_to_extract_chi:
#             temp = str(data[desired_field]).strip()
#
#             # removes brackets in case it is a number between brackets
#             if temp.startswith("["):
#                 temp = temp[1:-1].strip()
#
#             ret[desired_field] = temp
#
#             # ret[desired_field] = str(data[desired_field])
#
#     # print ret
#     # if ret.startswith("["):
#     #        value = ret.strip()[1:-1]
#
#     # print ret
#     hdulist.close()
#     return ret
#

def create_output_table(dir_=".", output_filename="output-mega-califa.txt"):
    """
    Reads all files in directory specified and saves as a txt file

    Returns: number of fits files written

    >>> create_output_table(".")
    3
    """

    filenames = glob.glob(os.path.join(dir_, "*.fits"))

    p = mp.Pool(8)
    rows = p.map(read_output, filenames)

    num_files = len(filenames)
    # print files
    n = 0
    with open(os.path.join(dir_, output_filename), "w") as out:
        for filename, data in zip(filenames, rows):
            galaxy_name = os.path.split(filename)[1].split("_")[0]

            if n == 0:
                out.write("#" " " + "galaxy_name" + " " + " ".join(list(data.keys())) + "\n")

            out.write(galaxy_name + " " + " ".join([str(x) for x in list(data.values())]) + "\n")

            n += 1

            if n % 10 == 0:
                print(("Processed {}/{} files".format(n, num_files)))

    return n

def create_output_table_chi2(dir_=".", output_filename="output-mega-califa_chi2.txt"):
    """
    Reads all files in directory specified and saves as a txt file

    Returns: number of fits files written

    >>> create_output_table_chi2(".")
    3
    """

    filenames = glob.glob(os.path.join(dir_, "*.fits"))

    print(("test'".format(filenames)))

    #parada = raw_input('paused')


    p = mp.Pool(8)
    rows = p.map(read_output_chi2, filenames)

    num_files = len(filenames)
    # print files
    n = 0
    with open(os.path.join(dir_, output_filename), "w") as out:
        for filename, data in zip(filenames, rows):
            galaxy_name = os.path.split(filename)[1].split("_")[0]

            if n == 0:
                out.write("#" " " + "galaxy_name" + " " + " ".join(list(data.keys())) + "\n")

            out.write(galaxy_name + " " + " ".join([str(x) for x in list(data.values())]) + "\n")

            n += 1

            if n % 10 == 0:
                print(("Processed {}/{} files".format(n, num_files)))

    return n

# def create_output_table(dir_=".", output_filename="output-mega-califa.txt"):
#     """
#     Reads all files in directory specified and saves as a txt file
#
#     Returns: number of fits files written
#
#     >>> create_output_table(".")
#     3
#     """
#
#     filenames = glob.glob(os.path.join(dir_, "*.fits"))
#     num_files = len(filenames)
#     # print files
#     n = 0
#     with open(os.path.join(dir_, output_filename), "w") as out:
#         for filename in filenames:
#             galaxy_name = os.path.split(filename)[1].split("_")[0]
#
#             try:
#                 data = read_output(filename)
#             except Exception as e:
#                 msg = "Error dealing with file '{}': {}: {}".format(filename, e.__class__.__name__, str(e))
#                 print msg
#                 write_bad_fit(galaxy_name, msg)
#                 continue
#
#             # data = read_output_chi2(filename)
#
#             if n == 0:
#                 out.write("#" " " + "galaxy_name" + " " + " ".join(data.keys()) + "\n")
#
#             out.write(galaxy_name + " " + " ".join([str(x) for x in data.values()]) + "\n")
#
#             n += 1
#
#             if n % 10 == 0:
#                 print("Processed {}/{} files".format(n, num_files))
#
#     return n


def create_output_table_bd(dir_=".", output_filename="output-mega-califa_bd.txt"):
    """
    Reads all files in directory specified and saves as a txt file

    Returns: number of fits files written

    >>> create_output_table_bd(".")
    3
    """

    files = glob.glob(os.path.join(dir_, "*.fits"))
    print(files)
    n = 0
    with open(os.path.join(dir_, output_filename), "w") as out:
        for filename in files:
            galaxy_name = os.path.split(filename)[1].split("_")[0]

            try:
                data = read_output_bd(filename)
            except Exception as e:
                msg = "Error dealing with file '{}': {}: {}".format(filename, e.__class__.__name__, str(e))
                print(msg)
                write_bad_fit(galaxy_name, msg)
                continue

            # data = read_output_chi2(filename)

            if n == 0:
                out.write("#" " " + "galaxy_name" + " " + " ".join(list(data.keys())) + "\n")

            out.write(galaxy_name + " " + " ".join(list(data.values())) + "\n")

            n += 1

    return n


def dump_header(filename):
    """
    Reads FITS file and dumps all headers into a text file named <filename>.txt
    """

    hdulist = fits.open(filename)

    output_filename = filename + ".txt"

    with open(output_filename, "w") as f:
        i = 0
        for hdu in hdulist:
            f.write("\n\n***** FRAME %02d *****\n" % i)
            f.write(repr(hdu.header) + "\n")
            i += 1

def fromNMAGYtoCOUNTs(dir_="."):
    """Transforms NMAGYS into counts for both PSFS and images"""

    ff = glob.glob(os.path.join(dir_, "*.fits"))
    #file_names=[]
    #for f in ff

    #filename = os.path.basaname(f)
    #pieces = filename.split("_")
    #file_name = pieces[1]
        #file_names.append(f)

    #file_names = list(set(file_names))

    
    for file_name in ff:
        print("Converting {}".format(file_name))
        hdulist = fits.open(file_name)

        med = np.mean(hdulist[0].data)
        print("Mmmmmmmmmmmmm {}".format(med))
        hdulist[0].data /= 0.00449599

        os.unlink(file_name)
        
        hdulist.writeto(file_name)
        hdulist.close()
        

    
