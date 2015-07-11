#!/bin/bash

# Gather inputs
# TODO we should probably verify valid IPs
echo "Tropius IP [default=192.168.1.200/24]: "
read tropius_ip
if [ -z $tropius_ip ]; then
    tropius_ip="192.168.1.200/24"
fi

echo "Default Gateway [default=192.168.1.1]: "
read gateway
if [ -z $gateway ]; then
    gateway="192.168.1.1"
fi

echo "DNS Server [default=192.168.1.1]: "
read dns
if [ -z $dns ]; then
    dns="192.168.1.1"
fi

echo "TROPIUS IP = $tropius_ip, Gateway = $gateway, DNS = $dns"
echo "Is this correct? [default=yes]: "
read confirm
if [ -z $confirm ]; then
    confirm="yes"
fi

# Determine which disk to install to
echo "Which device would you like to install to: [default=/dev/sdb]"
read disk
if [ -z $disk ]; then
    disk="/dev/sdb"
fi
echo "Are you sure you want to procede? Saying yes will completely wipe $disk."
read confirm
if ![ "$confirm" == "yes" -o "$confirm" == "y" ]; then
    exit
fi

# Use fdisk to partition the sd card
echo "Partitioning disk..."
echo -e "o\nn\np\n1\n\n+100M\nt\nc\nn\np\n2\n\n\nw\n" | fdisk $disk > /dev/null 2>&1
if [ "$?" -ne 0 ]; then
    echo "Error partitioning disk, installation failed."
    exit
fi

# Create and mount the FAT filesystem
echo "Mounting FAT filesystem..."
mkfs.vfat ${disk}1 > /dev/null 2>&1
if [ "$?" -ne 0 ]; then
    echo "Failed to format ${disk}1, installation failed."
    exit
fi
if ![ -e "boot" ]; then
    mkdir "boot" > /dev/null 2>&1
fi
mount ${disk}1 "boot" > /dev/null 2>&1
if [ "$?" -ne 0 ]; then
    echo "Error mounting ${disk}1, installation failed."
    exit
fi

# Create and mount the ext4 filesystem
echo "Mounting ext4 filesystem..."
mkfs.ext4 ${disk}2 > /dev/null 2>&1
if [ "$?" -ne 0 ]; then
    echo "Failed to format ${disk}2, installation failed."
    exit
fi
if ![ -e "root" ]; then
    mkdir "root" > /dev/null 2>&1
fi
mount ${disk}2 "root" > /dev/null 2>&1
if [ "$?" -ne 0 ]; then
    echo "Error mounting ${disk}2, installation failed."
    exit
fi

# Download/extract the root fs
echo "Fetching arch package..."
wget http://archlinuxarm.org/os/ArchLinuxARM-rpi-latest.tar.gz > /dev/null 2>&1
if [ "$?" -ne 0 ]; then
    echo "Failed to download package, installation failed."
    exit
fi
echo "Extracting package..."
# TODO bsdtar is kinda sketch...
bsdtar -xpf ArchLinuxARM-rpi-latest.tar.gz -C root > /dev/null 2>&1
if [ "$?" -ne 0 ]; then
    echo "Failed to extract package, installation failed."
    exit
fi
sync

# Move boot files to the first partition
echo "Moving over boot files..."
mv "root/boot/*" "boot" > /dev/null 2>&1
if [ "$?" -ne 0 ]; then
    echo "Failed to move over boot files, installation failed."
    exit
fi

# Create eth0.network file
echo "Creating systemd network file..."
filename="eth0.network"
if [ "$confirm" == "yes" -o "$confirm" == "y" ]; then
    touch $filename > /dev/null 2>&1
    if [ "$?" -eq 0 ]; then
        echo -e "[Match]" >> $filename
        echo -e "Name=eth0\n" >> $filename
        echo -e "[Network]" >> $filename
        echo -e "DNS=$dns\n" >> $filename
        echo -e "[Address]" >> $filename
        echo -e "Address=$tropius_ip\n" >> $filename
        echo -e "[Route]" >> $filename
        echo -e "Gateway=$gateway" >> $filename
    else
        echo "Could not create eth0.network file, installation failed."
        exit
    fi
fi
mv $filename "root/etc/systemd/network/eth0.network" > /dev/null 2>&1
if [ "$?" -ne 0 ]; then
    echo "Faild to move over eth0.nework file, installation failed."
fi

# Generate ssh keys and load them onto the install
if ![ -e "~/.ssh/id_rsa" ]; then
    echo "Generating ssh keys..."
    ssh-keygen -t rsa -N "" -f my.key > /dev/null 2>&1
    if [ "$?" -ne 0 ]; then
        echo "Failed to create ssh keys, installation failed."
        exit
    fi
fi
echo "Moving ssh key to home directory..."
mkdir "root/home/.ssh" > /dev/null 2>&1
cp "~/.ssh/id_rsa.pub" "root/home/.ssh/authorized_keys"

# Move boot files to the boot partition
echo "Finishing disk configuration..."
mv "root/boot/*" "boot"
if [ "$?" -ne 0 ]; then
    echo "Failed to move boot files, installation failed."
    exit
fi
umount boot root
if [ "$?" -ne 0 ]; then
    echo "Failed to unmount disk, installation failed"
    exit
fi

echo "Eject the SD card and load it into the Raspberry Pi, then press ENTER"
read confirm

# Run ping attempts 50 times or until we get a connection
attempts=50
success=1
echo "Waiting for TROPIUS instance to be live..."
while [[ "$success" -ne 0 ]] && [[ "$attempts" -gt 0 ]]; do
    ping -c 1 ${tropius_ip::(-3)} > /dev/null 2>&1
    success=$?
    let "attempts--"
    sleep 1
done
if [[ "$success" -ne 0 ]]; then
    echo "Failed to connect to TROPIUS, installation failed."
    exit
fi

# Configure the root account
if [ -e "root_install.sh" ]; then
    echo "Configuring root account..."
    ssh root@$tropius_ip 'bash -s' < root_install.sh > /dev/null 2>&1
else
    echo "Could not find root configuration script, installation failed."
    exit
fi

# Configure the user account
if [ -e "user_install.sh" ]; then
    echo "Configuring user account..."
    ssh tropius@$tropius_ip 'bash -s' < user_install.sh > /dev/null 2>&1
else
    echo "Could not find user configuration script, installation failed."
    exit
fi
