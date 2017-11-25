from setuptools import setup, find_packages
from glob import glob

setup(
    name = 'ariastro',
    packages = find_packages(),
    version = '0.17.11.25.0',
    license = 'GNU GPLv3',
    platforms = 'any',
    description = 'Ari Astro tools',
    install_requires = ['numpy', 'astropy', 'matplotlib', 'f311>=0.17.11.25.0'],
    scripts = glob('ariastro/scripts/*.py')  # Considers system scripts all .py files in 'ariastro/scripts' directory
)