from setuptools import setup, find_packages
from glob import glob

setup(
    name = 'ariastro',
    packages = find_packages(),
    version = '0.16.11.11',
    license = 'GNU GPLv3',
    platforms = 'any',
    description = 'Ari Astro tools',
    install_requires = ['numpy', 'astropy', 'matplotlib'],
    scripts = glob('scripts/*.py')  # Considers system scripts all .py files in 'scripts' directory
)