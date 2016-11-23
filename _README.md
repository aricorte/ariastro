# `ariastro`

## Installation


### Set the path to `galfitm-1.2.1-linux-x86_64`

```shell
cd /usr/local/bin
sudo ln -s <path-to-galfit>/galfitm-1.2.1-linux-x86_64

### Install `ariastro` package and scripts

```shell
sudo python setup.py develop
```



## How to setup GitHub project

### On GitHub

Create project `ariastro`

### Local machine

```shell
git init
git remote add origin ssh://git@github.com/aricorte/ariastro.git
git add . --all
git commit -m "first commit"
git push
```