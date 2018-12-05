# Kadu's code for PSF 
def make_vband_psf(fwhm, beta, radius, outfile="psf.fits"):
    import numpy as np
    from astropy.io import fits as pf
    alpha = fwhm / (2 * np.sqrt(np.power(2., 1/beta) - 1.))
    r = np.linspace(-radius, radius, 2 * radius + 1)
    print(r)
    X, Y = np.meshgrid(r, r)
    R = np.sqrt(X**2 + Y**2)
    I = (beta - 1.) / (np.pi * alpha**2) * \
        np.power(1. + np.power(R / alpha, 2), -beta)
    hdu = pf.PrimaryHDU(I)
    hdulist = pf.HDUList([hdu])
    hdulist.writeto(outfile, clobber=True)
    return
 
