#!/usr/bin/python

import glob
import os
from ariastro.library import *
import sys


def replace_pattern_in_template(template, pattern, str_replace):
    """pattern by galaxy name and returns new string"""
    contents1 = template.replace(pattern, str_replace)
    return contents1


# PATH = "./all-fits"
PATH = "."

# # Extract all galaxy names
ff = glob.glob(os.path.join(PATH, "psf*.fits"))
galaxy_names = []
for f in ff:
    filename = os.path.basename(f)
    # print filename
    pieces = filename.split("_")
    galaxy_name = pieces[1]
    galaxy_names.append(galaxy_name)


# # Reads some input data
# template 
with open("galfit.feedme.template", "r") as file:
  template = file.read()
# Galaxy table in CSV format
table = load_jma_gri("CALIFA-JMA-gri.mfmtk_mag")


# print table[0]
# sys.exit()


# # Runs script for all galaxies
FEEDME_FILENAME = "galfit.feedme"
COMMAND = "./galfitm-1.2.1-osx  "+FEEDME_FILENAME
for galaxy_name in galaxy_names:
    filename_test = os.path.join(PATH, galaxy_name+"_g.fits")

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
        columns_needed = ["x0Fit2D_g", "x0Fit2D_r", "x0Fit2D_i", "y0Fit2D_g", "y0Fit2D_r", "y0Fit2D_i", "skybg_g",
                          "skybg_r", "skybg_i", "g_2", "r", "i", ]

        for name in columns_needed:
            if not row[name]:
                print "**WARNING**: row '%s' is empty, cannot process galaxy '%s' :(" % (name, galaxy_name)
                goes = False
                break

    if goes:
        width, height = get_dims(filename_test)

        row = find_row_by_galaxy_name(table, galaxy_name)
        #except:
        #    print "Could not find galaxy '%s' in table" % galaxy_name

        if row:            
            contents = replace_pattern_in_template(template, "@@@@@@", galaxy_name)
            contents = replace_pattern_in_template(contents, "WWWWWW", str(width))
            contents = replace_pattern_in_template(contents, "HHHHHH", str(height))
            contents = replace_pattern_in_template(contents, "XGXGXG", row["x0Fit2D_g"]) 
            contents = replace_pattern_in_template(contents, "XRXRXR", row["x0Fit2D_r"]) 
            contents = replace_pattern_in_template(contents, "XIXIXI", row["x0Fit2D_i"]) 
            contents = replace_pattern_in_template(contents, "YGYGYG", row["y0Fit2D_g"]) 
            contents = replace_pattern_in_template(contents, "YRYRYR", row["y0Fit2D_r"]) 
            contents = replace_pattern_in_template(contents, "YIYIYI", row["y0Fit2D_i"]) 
            contents = replace_pattern_in_template(contents, "BKGG", row["skybg_g"]) 
            contents = replace_pattern_in_template(contents, "BKGR", row["skybg_r"]) 
            contents = replace_pattern_in_template(contents, "BKGI", row["skybg_i"]) 
            contents = replace_pattern_in_template(contents, "MMAGG", row["g_2"]) 
            contents = replace_pattern_in_template(contents, "MMAGR", row["r"]) 
            contents = replace_pattern_in_template(contents, "MMAGI", row["i"]) 


#        contents = replace_pattern_in_template(contents, "XXXXXX", str(float(width)/2))
#        contents = replace_pattern_in_template(contents, "YYYYYY", str(float(height)/2))
        
            with open(FEEDME_FILENAME, "w") as file:
                file.write(contents)
            os.system(COMMAND)  
#	break

##Read outputs from the SS fit
create_output_table("../outputs")
sys.exit()



#    pieces = os.path.basename(f)

