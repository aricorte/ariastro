# INSTALL BUTTERFLY IN ALPHACRUCIS (you need to have access to the cluster)

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
pip install f311
```

Note Every time you want to work with F311, you will need to activate the environment:

```
source activate astroenv
```

To deactivate the environment:

```
source deactivate
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
