# `ariastro`

## Installation



### Set the path to `galfitm-1.2.1-linux-x86_64`

```shell
cd /usr/local/bin
sudo ln -s <path-to-galfit>/galfitm-1.2.1-linux-x86_64
```

### Install `ariastro` package and scripts

```shell
cd CALIFA/github
sudo python setup.py develop
cd scripts
chmod +x *.py
```



## How to setup GitHub project

### On GitHub

Create project `ariastro`

### Local machine

#### Setup git 

```shell
git init
git remote add origin ssh://git@github.com/aricorte/ariastro.git
```

:notes: It is necessary to setup SSH key: please check https://github.com/trevisanj/oblivion/blob/master/github-ssh.md

#### Create commits 

```
git add . --all
git commit -m "first commit"
git push
```

## PyCharm shortcuts

  - rename file: Shift+F6
  - find file by name: Ctrl+Shift+N

## Astroenv
  
   source activate astroenv