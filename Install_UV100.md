# INSTALL BUTTERFLY IN ALPHACRUCIS (you need to have access to the cluster)

## 1) load python3 in alphacrucis
```
module load anaconda/3-2.5.0/python-3.5 
```
(https://lai.iag.usp.br/projects/lai/wiki/FAQ)

## 2) create a github account and authenticate
```
https://github.com/trevisanj/oblivion/blob/master/github-ssh.md
```
(question what about ‘change remote url’?)

## 3) install "f311" Python package and create Anaconda virtual environment "astroenv" (or other name you like)

https://trevisanj.github.io/f311/install.html

```
pip install numpy scipy matplotlib astropy configobj bs4 robobrowser requests fortranformat tabulate rows pyqt5 a99 f311
```

```
conda create --name astroenv python=3.5
source activate astroenv
```

## 4) install our version of MegaMorph

```
git clone -b butterfly git@github.com:aricorte/ariastro.git
```

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
