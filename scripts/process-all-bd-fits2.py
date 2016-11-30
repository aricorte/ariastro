#!/usr/bin/python

import glob
import os

from ariastro import *


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
with open("galfit.feedme.template.br", "r") as file:
  template = file.read()
# Galaxy table in CSV format
table = load_jma_gri("output-mega-califa.txt")


# print table[0]
# sys.exit()


# # Runs script for all galaxies
FEEDME_FILENAME = "galfit.feedme"
COMMAND = "./galfitm-1.1.8-osx "+FEEDME_FILENAME
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
        columns_needed = ["2_XC_G", "2_YC_G", "2_XC_R", "2_YC_R", "2_XC_I", "2_YC_I", "1_SKY_0",
                          "1_SKY_1", "1_SKY_2", "2_MAG_G", "2_MAG_R", "2_MAG_I","2_RE_G","2_RE_R","2_RE_I","2_N_R","2_N_G","2_N_I",]

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
            contents = replace_pattern_in_template(contents, "XGXGXG", row["2_XC_G"]) 
            contents = replace_pattern_in_template(contents, "XRXRXR", row["2_XC_R"]) 
            contents = replace_pattern_in_template(contents, "XIXIXI", row["2_XC_I"]) 
            contents = replace_pattern_in_template(contents, "YGYGYG", row["2_YC_G"]) 
            contents = replace_pattern_in_template(contents, "YRYRYR", row["2_YC_R"]) 
            contents = replace_pattern_in_template(contents, "YIYIYI", row["2_YC_I"]) 
            contents = replace_pattern_in_template(contents, "BKGG", row["1_SKY_0"]) 
            contents = replace_pattern_in_template(contents, "BKGR", row["1_SKY_1"]) 
            contents = replace_pattern_in_template(contents, "BKGI", row["1_SKY_2"]) 
            contents = replace_pattern_in_template(contents, "MMABG", row["2_MAG_G"]) 
            contents = replace_pattern_in_template(contents, "MMABR", row["2_MAG_R"]) 
            contents = replace_pattern_in_template(contents, "MMABI", row["2_MAG_I"])
            contents = replace_pattern_in_template(contents, "MMADG", row["2_MAG_G"])
            contents = replace_pattern_in_template(contents, "MMADR", row["2_MAG_R"])
            contents = replace_pattern_in_template(contents, "MMADI", row["2_MAG_I"])
            contents = replace_pattern_in_template(contents, "NNBG", row["2_N_R"])
            contents = replace_pattern_in_template(contents, "REBG", row["2_RE_G"])
            contents = replace_pattern_in_template(contents, "REBR", row["2_RE_R"])
            contents = replace_pattern_in_template(contents, "REBI", row["2_RE_I"]) 
            contents = replace_pattern_in_template(contents, "REDG", row["2_RE_G"])
            contents = replace_pattern_in_template(contents, "REDR", row["2_RE_R"])
            contents = replace_pattern_in_template(contents, "REDI", row["2_RE_I"])


#        contents = replace_pattern_in_template(contents, "XXXXXX", str(float(width)/2))
#        contents = replace_pattern_in_template(contents, "YYYYYY", str(float(height)/2))
        
            with open(FEEDME_FILENAME, "w") as file:
                file.write(contents)
            os.system(COMMAND)  
	break

##Read outputs from the SS fit
#create_output_table("../outputs")
#sys.exit()



#    pieces = os.path.basename(f)

