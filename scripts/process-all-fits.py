#!/usr/bin/python

import glob
import os
from ariastro.library import *
import sys


# # Definition of constants

FEEDME_FILENAME = "galfit.feedme"
COMMAND = "./galfitm-1.2.1-linux-x86_64  " + FEEDME_FILENAME
FILENAME_CSV_TABLE = "all-gal.csv"
# PATH = "./all-fits"
PATH = "."

#
#
#

def replace_pattern_in_template(template, pattern, str_replace):
    """pattern by galaxy name and returns new string"""
    contents1 = template.replace(pattern, str_replace)
    return contents1



# # Extract all galaxy names
ff = glob.glob(os.path.join(PATH, "psf*.fits"))
galaxy_names = []
for f in ff:
    filename = os.path.basename(f)
    # print filename
    pieces = filename.split("_")
    galaxy_name = pieces[1]
    galaxy_names.append(galaxy_name)

galaxy_names = list(set(galaxy_names))

# # Reads some input data
# template
with open("galfit.feedme.template", "r") as file:
    template = file.read()
# Galaxy table in CSV format
table = load_jma_gri(FILENAME_CSV_TABLE)

#print table[0]
# sys.exit()


# # Runs script for all galaxies

# print(galaxy_names)
# sys.exit()


for galaxy_name in galaxy_names:
    filename_test = os.path.join(PATH, galaxy_name + "_g.fits")

    goes = True
    if not os.path.isfile(filename_test):
        print "**WARNING**: file '%s' not found, skipping galaxy '%s' :(" % (filename_test, galaxy_name)
        goes = False

    if goes:
        row = find_row_by_galaxy_name(table, galaxy_name)

        if not row:
            print "**WARNING**: galaxy '%s' not found in table :(" % (galaxy_name,)
            goes = False

    if goes:
        columns_needed = ["x0Fit2D_u", "x0Fit2D_g", "x0Fit2D_r", "x0Fit2D_i", "x0Fit2D_z", "y0Fit2D_u", "y0Fit2D_g",
                          "y0Fit2D_r", "y0Fit2D_i", "y0Fit2D_z", "skybg_u", "skybg_g",
                          "skybg_r", "skybg_i", "skybg_z", "u", "g", "r", "i", "z"]

        for name in columns_needed:
            if not row[name]:
                print "**WARNING**: row '%s' is empty, cannot process galaxy '%s' :(" % (name, galaxy_name)
                goes = False
                # break

    if goes:
        width, height = get_dims(filename_test)

        row = find_row_by_galaxy_name(table, galaxy_name)
        # except:
        #    print "Could not find galaxy '%s' in table" % galaxy_name

        if row:

            if False:
                print("GONNA PROCESS GALAXY {}".format(galaxy_name))
                continue

            contents = replace_pattern_in_template(template, "@@@@@@", galaxy_name)
            contents = replace_pattern_in_template(contents, "WWWWWW", str(width))
            contents = replace_pattern_in_template(contents, "HHHHHH", str(height))
            contents = replace_pattern_in_template(contents, "XUXUXU", row["x0Fit2D_u"])
            contents = replace_pattern_in_template(contents, "XGXGXG", row["x0Fit2D_g"])
            contents = replace_pattern_in_template(contents, "XRXRXR", row["x0Fit2D_r"])
            contents = replace_pattern_in_template(contents, "XIXIXI", row["x0Fit2D_i"])
            contents = replace_pattern_in_template(contents, "XZXZXZ", row["x0Fit2D_z"])
            contents = replace_pattern_in_template(contents, "YUYUYU", row["x0Fit2D_u"])
            contents = replace_pattern_in_template(contents, "YGYGYG", row["y0Fit2D_g"])
            contents = replace_pattern_in_template(contents, "YRYRYR", row["y0Fit2D_r"])
            contents = replace_pattern_in_template(contents, "YIYIYI", row["y0Fit2D_i"])
            contents = replace_pattern_in_template(contents, "YZYZYZ", row["x0Fit2D_z"])
            contents = replace_pattern_in_template(contents, "BKGU", row["skybg_u"])
            contents = replace_pattern_in_template(contents, "BKGG", row["skybg_g"])
            contents = replace_pattern_in_template(contents, "BKGR", row["skybg_r"])
            contents = replace_pattern_in_template(contents, "BKGI", row["skybg_i"])
            contents = replace_pattern_in_template(contents, "BKGZ", row["skybg_z"])
            contents = replace_pattern_in_template(contents, "MMAGU", row["u"])
            contents = replace_pattern_in_template(contents, "MMAGG", row["g"])
            contents = replace_pattern_in_template(contents, "MMAGR", row["r"])
            contents = replace_pattern_in_template(contents, "MMAGI", row["i"])
            contents = replace_pattern_in_template(contents, "MMAGZ", row["z"])

            #        contents = replace_pattern_in_template(contents, "XXXXXX", str(float(width)/2))
            #        contents = replace_pattern_in_template(contents, "YYYYYY", str(float(height)/2))

            with open(FEEDME_FILENAME, "w") as file:
                file.write(contents)
            os.system(COMMAND)
            #	break

##Read outputs from the SS fit
# create_output_table("../outputs")
# XSsys.exit()



#    pieces = os.path.basename(f)

