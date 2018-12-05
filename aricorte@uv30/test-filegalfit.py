from f311 import filetypes as ft
from f311 import explorer as ex
f = ft.FileGalfit()

if False:
    f.load("1237668494708178979_ss.fits")
else:
    f.load("3115_allfree_1disk_C02PA1BA1.fits")

v = ex.VisGalfitFig()
v.use(f)