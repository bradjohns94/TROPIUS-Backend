#!/bin/bash

echo "Enter the IP address of the TROPIUS device: "
read ip

# Run the root install script
echo "root" | ssh root@$ip 'bash -s' < root_install.sh
# Send TROPIUS code files to the device
scp -r "../" tropius@$ip:
# Run the user isntall script
echo "tropius" | ssh tropius@$ip 'bash -s' < user_install.sh
