# INSTALL BUTTERFLY IN ALPHACRUCIS (you need to have access to the cluster)
#This program is a python wrap of GALFITM () and it can be used in two ways:
#1) running GALFITM on a set of stamp with given PSF and input table of initial parameters (examples can be found here)
#2) create images and plots starting from GALFITM outputs, as fits tables and images (example can be found here)


## 1) load python3 in uv30
```
module load anaconda/3-2.5.0/python-3.5 
```
(https://lai.iag.usp.br/projects/lai/wiki/FAQ)


## 2) install "f311" Python package and create Anaconda virtual environment "astroenv" (or other name you like)

https://trevisanj.github.io/f311/install.html

```
conda create --name astroenv python=3.5
source activate astroenv
```
```
pip install f311 ....
```

Note Every time you want to work with F311, you will need to activate the environment:

```
source activate astroenv
```

To deactivate the environment:

```
source deactivate
```

## 3) install our version of MegaMorph

```
git clone -b butterfly git@github.com:aricorte/ariastro.git
```
if not working 

1) go to https://github.com/aricorte/ariastro 
2) clic on "Clone or download" and choose "Download zip"
3) copy the zip in the directory where you want to use it
4) unzip *.zip

## 4) make the programs ready to run in every directory

cd ariastro-butterfly
sudo python setup.py develop
cd ariastro/scripts
chmod +x *.py

## 5) always keep your data and output in silo1

https://lai.iag.usp.br/projects/lai/wiki/FAQ (Como eu crio um ponto de montagem usando sshfs?)

```
ssh <USER>@silo1.iag.usp.br
exit
```

Conecte-se na alphacrucis e crie um diretório para o ponto de montagem
```
mkdir silo1
sshfs <USER>@silo1.iag.usp.br:/sto/home/usuário ./silo1
```

BE HAPPY
