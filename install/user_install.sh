#!/bin/bash
# User component of the tropius install

password="tropius"

# Install TROPIUS dependencies
echo "$password" | sudo -S pacman -S base-devel --noconfirm
echo "$password" | sudo -S pacman -S ipython2 --noconfirm
echo "$password" | sudo -S pacman -S vim --noconfirm
echo "$password" | sudo -S pacman -S python2-flask --noconfirm

# Do some basic user configurations
echo "alias ipython='ipython2'" >> "/home/tropius/.bashrc"

# Install yaourt
cd "/home/tropius/TROPIUS/tmp/"
tar -xzvf "package-query.tar.gz"
tar -xzvf "yaourt.tar.gz"
cd "/home/tropius/TROPIUS/tmp/package-query/"
makepkg
echo "$password" | sudo -S pacman -U package-query-1.6.2-1-armv6h.pkg.tar.xz --noconfirm
cd "/home/tropius/TROPIUS/tmp/yaourt/"
makepkg
echo "$password" | sudo -S pacman -U yaourt-1.6-1-any.pkg.tar.xz --noconfirm
cd "/home/tropius/"

# Install the TROPIUS database
python "/home/tropius/TROPIUS/py_tropius/install.py"

# Install TROPIUS daemons
chmod +x "/home/tropius/TROPIUS/api/app.py"
echo "$password" | sudo mv "/home/tropius/TROPIUS/tmp/tropius.service" "/etc/systemd/service"
chmod +x "/home/tropius/TROPIUS/daemons/state.py"
echo "$password" | sudo mv "/home/tropius/TROPIUS/tmp/tropius_state.service" "/etc/systemd/service"
echo "$password" | sudo systemctl enable tropius
echo "$password" | sudo systemctl enable tropius_state
echo "$password" | sudo systemctl start tropius
echo "$password" | sudo systemctl start tropius_state
