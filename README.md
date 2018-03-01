# `ariastro - being updated`

### This program is a python wrap of GALFITM (https://www.nottingham.ac.uk/astronomy/megamorph/) and it can be used in two ways:

### 1) running GALFITM on a set of stamps with given PSF and input table of initial parameters - including background (examples can be found here)

### 2) create images and plots starting from GALFITM outputs, as fits tables and images (examples can be found here)

### In here we explain how to install it (NB you need to have anaconda and python 3.6 installed in your computer) 

## Installation

### Download GALFITM

Dwonload the appropriate GALFITM from https://www.nottingham.ac.uk/astronomy/megamorph/

### Set the path to GalFit executable

Next we will show you how to create a link named ```galfitm```that will be invoked by ```ariastro``` when needed. This link, in turn, must point to an existing GalFit executable, and it has to be in your system path. Below there is an example to be done if you have sudo access on your machine.

```shell
cd /usr/local/bin  # or other directory that is already in your path
sudo ln -s <path-to-galfit-executable> galfitm
```

#### no-sudo Alternative

If you don't have sudo access, you may try some of the following:

```shell
cd  # chances to home directory
mkdir bin
cd bin
ln -s <path-to-galfit-executable> galfitm
```
Then add the following line to your file ```~/.bashrc```:

```shell
export PATH="${PATH}:~/bin"
```

## 1) load python3 in uv30
```
module load anaconda/3-2.5.0/python-3.5 
```
(https://lai.iag.usp.br/projects/lai/wiki/FAQ)


## 2) install "ariastro" Python package and create Anaconda virtual environment "astroenv" (or other name you like)

```
conda create --name astroenv python=3.5
source activate astroenv
```
```
pip install ariastro
```

Note Every time you want to work with F311, you will need to activate the environment:

```
source activate astroenv
```

To deactivate the environment:

```
source deactivate
```

## If you have already installed

Here is the list of commands to type next time you log onto UV30:

```
module load anaconda/3-2.5.0/python-3.5 
source activate astroenv
```

BE HAPPY


