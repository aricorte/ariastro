#!/usr/bin/env python   
import glob
import os
from ariastro import *
import numpy

# TODO Write script docstring

# # Definition of constants
PROCESS_GALAXIES = True  # Simulation mode or fitting mode
FEEDME_FILENAME = "galfit.feedme"
TEMPLATE_FILENAME = "galfit.feedme.template"
COMMAND = "./galfitm-1.2.1-linux-x86_64  " + FEEDME_FILENAME
FILENAME_CSV_TABLE = "/work/arianna/CALIFA/data/Juliana/images/input.SPLUS.select.csv"
# PATH = "./all-fits"
PATH = "."

def main():
    global output_pattern, template, table

    # # Extract all galaxy names
    ff = glob.glob(os.path.join(PATH, "*.fits"))
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
    with open(TEMPLATE_FILENAME, "r") as file:
        template = file.read()
        output_pattern = get_output_pattern(template)

    # Galaxy table in CSV format
    table = load_jma_gri(FILENAME_CSV_TABLE)
    # # Runs script for all galaxies
    igal = 0
    for galaxy_name in galaxy_names:
        filename_test = os.path.join(PATH, galaxy_name + "_g.fits")

        # # Next is a series of tests to determine whether the galaxy will be **really** processed
        # If it is decided that it will not, a 'continue' statement will skip to the beginning of the next 'for' iteration

        # Test 0
        output_filename = output_pattern.replace("@@@@@@", galaxy_name)
        if os.path.isfile(output_filename):
            print(("**INFO**: output file '%s' already exists, skipping galaxy '%s' :)" % (
            output_filename, galaxy_name)))
            continue

        # Test 1
        if not os.path.isfile(filename_test):
            msg = "**WARNING**: file '%s' not found, skipping galaxy '%s' :(" % (
            filename_test, galaxy_name)
            print(msg)
            write_not_run(galaxy_name, msg)
            continue

        row = find_row_by_galaxy_name(table, galaxy_name)

        # Test 2
        if not row:
            msg = "**WARNING**: galaxy '%s' not found in table :(" % (galaxy_name,)
            print(msg)
            write_not_run(galaxy_name, msg)
            continue

        columns_needed = ["uJAVA_petro","F378_petro","F395_petro","F410_petro","F430_petro","g_petro","F515_petro","r_petro","F660_petro","i_petro","F861_petro","z_petro"]

        # Test 3
        for name in columns_needed:
            if not row[name]:
                msg = "**WARNING**: row '%s' is empty, cannot process galaxy '%s' :(" % (
                name, galaxy_name)
                print(msg)
                write_not_run(galaxy_name, msg)
                continue
                # break

        width, height = get_dims(filename_test)


        # get_exptime(os.path.join(PATH, galaxy_name + "_u.fits"))

        row = find_row_by_galaxy_name(table, galaxy_name)

        # Test 4
        if not row:
            continue

        # **If reached this point in the code it is because the galaxy will be processed**

        # except:
        #    print "Could not find galaxy '%s' in table" % galaxy_name


        # If the following is put 'True', just pretends that galaxy will be processed, but does noth

        print(("**Info**: GONNA PROCESS GALAXY {}".format(galaxy_name)))
        igal = igal + 1

        if not PROCESS_GALAXIES:
            continue

        # deg=8
        # for NN in deg
        # NN=NN+1

        # expt_u=float(get_exptime(os.path.join(PATH, galaxy_name + "_u.fits")))
        zpu = 24.63 - 2.5 * numpy.log10(
            float(get_exptime(os.path.join(PATH, galaxy_name + "_u.fits"))))
        zpg = 25.11 - 2.5 * numpy.log10(
            float(get_exptime(os.path.join(PATH, galaxy_name + "_g.fits"))))
        zpr = 24.80 - 2.5 * numpy.log10(
            float(get_exptime(os.path.join(PATH, galaxy_name + "_r.fits"))))
        zpi = 24.36 - 2.5 * numpy.log10(
            float(get_exptime(os.path.join(PATH, galaxy_name + "_i.fits"))))
        zpz = 22.83 - 2.5 * numpy.log10(
            float(get_exptime(os.path.join(PATH, galaxy_name + "_z.fits"))))

        #x0u, y0u = get_x0y0(os.path.join(PATH, galaxy_name + "_u.fits"))
        #x0g, y0g = get_x0y0(os.path.join(PATH, galaxy_name + "_g.fits"))
        #x0r, y0r = get_x0y0(os.path.join(PATH, galaxy_name + "_r.fits"))
        #x0i, y0i = get_x0y0(os.path.join(PATH, galaxy_name + "_i.fits"))
        #x0z, y0z = get_x0y0(os.path.join(PATH, galaxy_name + "_z.fits"))


        x0u, y0u = get_dims(os.path.join(PATH, galaxy_name + "_u.fits"))
        x0g, y0g = get_dims(os.path.join(PATH, galaxy_name + "_g.fits"))
        x0r, y0r = get_dims(os.path.join(PATH, galaxy_name + "_r.fits"))
        x0i, y0i = get_dims(os.path.join(PATH, galaxy_name + "_i.fits"))
        x0z, y0z = get_dims(os.path.join(PATH, galaxy_name + "_z.fits"))

        #nmgyu = get_nmgy(os.path.join(PATH, galaxy_name + "_u.fits"))
        #nmgyg = get_nmgy(os.path.join(PATH, galaxy_name + "_g.fits"))
        #nmgyr = get_nmgy(os.path.join(PATH, galaxy_name + "_r.fits"))
        #nmgyi = get_nmgy(os.path.join(PATH, galaxy_name + "_i.fits"))
        #nmgyz = get_nmgy(os.path.join(PATH, galaxy_name + "_z.fits"))

        #skybg_u = "skybg_u" /0.0044599
        #skybg_g = row["skybg_g"] /0.0044599
        #skybg_r = row["skybg_r"] /0.0044599
        #skybg_i = row["skybg_i"] /0.0044599
        #skybg_z = row["skybg_z"] /0.0044599


        search_replace = [
            ("@@@@@@", galaxy_name),
            ("WWWWWW", str(width)),
            ("HHHHHH", str(height)),
            ("ZPU", str(float(zpu))),
            ("ZPG", str(float(zpg))),
            ("ZPR", str(float(zpr))),
            ("ZPI", str(float(zpi))),
            ("ZPZ", str(float(zpz))),
            ("XUXUXU", str(float(x0u/2))),
            ("XGXGXG", str(float(x0g/2))),
            ("XRXRXR", str(float(x0r/2))),
            ("XIXIXI", str(float(x0i/2))),
            ("XZXZXZ", str(float(x0z/2))),
            ("YUYUYU", str(float(y0u/2))),
            ("YGYGYG", str(float(y0g/2))),
            ("YRYRYR", str(float(y0r/2))),
            ("YIYIYI", str(float(y0i/2))),
            ("YZYZYZ", str(float(y0z/2))),
            #("BKGU", str(float(row["skybg_u"])/nmgyu)),
            #("BKGG", str(float(row["skybg_g"])/nmgyg)),
            #("BKGR", str(float(row["skybg_r"])/nmgyr)),
            #("BKGI", str(float(row["skybg_i"])/nmgyi)),
            #("BKGZ", str(float(row["skybg_z"])/nmgyz)),
            #("BKGU", str(float(skybg_u))),
            #("BKGG", str(float(skybg_g))),
            #("BKGR", str(float(skybg_r))),
            #("BKGI", str(float(skybg_i))),
            #("BKGZ", str(float(skybg_z))),
            ("MMAGU", row["uJAVA_petro"]),
            ("MMAGG", row["g_petro"]),
            ("MMAGR", row["r_petro"]),
            ("MMAGI", row["i_petro"]),
            ("MMAGZ", row["z_petro"]),
        ]

        # ("XXXXXX", str(float(width)/2))
        # ("YYYYYY", str(float(height)/2))


        contents = solve_feedme_template(template, search_replace)


        with open(FEEDME_FILENAME, "w") as file:
            file.write(contents)

        os.system(COMMAND)
    print(("I fit", igal, "galaxies"))


if __name__ == "__main__":
    main()
