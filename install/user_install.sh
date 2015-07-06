#!/bin/bash
# User component of the tropius install

$password = "tropius"

# Do some basic user configurations
echo "alias ipython='ipython2'" >> "~/.bashrc"

# Install yaourt
cd "~/TROPIUS/tmp/"
tar -xzvf "package-query.tar.gz"
tar -xzvf "yaourt.tar.gz"
cd "~/TROPIUS/tmp/package-query/"
makepkg
echo "$password" | sudo -S pacman -U package-query-1.6.2-1-armv6h.pkg.tar.xz --noconfirm
cd "~/TROPIUS/tmp/yaourt/"
makepkg
echo "$password" | sudo -S pacman -U yaourt-1.6.1-any.pkg.tar.xz --noconfirm
