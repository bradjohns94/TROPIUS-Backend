#!/bin/bash
spawn ssh tropius@192.168.8.200
expect "password:"
send "tropius\r"
echo "$?"
