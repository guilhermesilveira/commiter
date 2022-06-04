# TODO CECILIA keep display visually the last commit number
# TODO CECILIA onmouseclick: commit
# TODO CECILIA qrcode + share + video WHEN?

# Raspberry PI

Enable camera based on 
https://www.raspberrypi.com/documentation/accessories/camera.html#:~:text=Run%20sudo%20raspi%2Dconfig%20.,Reboot%20your%20Raspberry%20Pi%20again.

# Creating keys

```shell
mkdir keys
ssh-keygen -t ed25519 -C "guilherme.silveira@gmail.com" -f keys/id_ed25519
ssh-add keys/id_ed25519
pbcopy < .ssh/id_ed25519.pub
open https://github.com/guilhermesilveira/commiter-results/settings/keys

scp -rC keys admin@192.168.86.32:~/
```


# Install

```shell
ssh admin@192.168.86.32
cd keys
ssh-add keys/id_ed25519
mkdir -p work
cd work

git clone git@github.com:guilhermesilveira/commiter.git
sh commiter/install/install-opencv2.sh
sh commiter/install/install-libgit2.sh
cd commiter
# sh install/build.sh
# or
# git clone git@github.com:guilhermesilveira/commiter-results.git output
# git clone https://github.com/guilhermesilveira/commiter-results.git
```

# Run

```shell
python main.py screenshot
```

# Cleaning output and keys

```shell
rm -fr output/.git
rm -f keys/*
```