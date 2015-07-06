#!/bin/bash
# TROPIUS install, to be run on 192.168.8.200 after startup
root="root"
user="tropius"
guest="guest"
password="tropius"

# Set the root password
echo "$password" | passwd "$root" --stdin > /dev/null 2>&1

# Set the hostname
echo "TROPIUS" > "/etc/hostname"
hostnamectl set-hostname "TROPIUS"

# Add the tropius and gues users
useradd -m -s "/bin/bash" "$user"
useradd -m -s "/bin/bash" "$guest"
echo "$password" | passwd "$user" --stdin
echo "$password" | passwd "$guest" --stdin

# Upgrade pacman
pacman -Syu --noconfirm
echo 'all' | pacman-db-upgrade # XXX This probably doesn't work...
pacman -S base-devel --noconfirm

# Install sudo
pacman -S sudo --noconfirm
chmod +w "/etc/sudoers"
echo "tropius ALL=(ALL) ALL" >> "/etc/sudoers"
chmod -w "/etc/sudoers"

# Install other useful packages
pacman -S yajl --noconfirm
# TODO add package-query and yaourt packages to install
pacman -S vim --noconfirm
pacman -S ipython2 --noconfirm
echo "alias ipython='ipython2'" >> ~/.bashrc
pacman -S python2-flask --noconfirm
