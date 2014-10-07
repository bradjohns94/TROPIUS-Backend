TROPIUS
Territorial Remote Operated Pi Utility System
Created by: Bradley Johns

Introduction:
=============
TROPIUS is a Raspberry Pi operated home automation system
This README is for the Raspberry Pi Backend, if you are looking for
the Android front end see the TROPIUS-Frontend repository.

The TROPIUS backend is divided into two main components:
    py_tropius -- a directory of utility files, including, but not limited to
                  database operation scripts, installation scripts, and
                  utility scripts to carry out the TROPIUS operations

    api        -- A RESTFUL api implemented using the python Flask utility which
                  links the frontend to the py_tropius scripts.

TROPIUS is still in its earliest stages, in fact this README was made for the initial
commit in which all the system can currently do is dump database entries and execute
a wake on lan script via curl commands over port 8073.


Installation:
=============
Although TROPIUS is designed to be easily implementable, this feature has virtually
no work put into it as of yet, thusly, most of the installation must be done manually
at the moment.
    What you'll need:
        A Raspberry Pi Device, preferrably running Arch Linux
        Python 2.7.8 or later
        The Python Flask and psycopg2 libraries
        A postgerSQL database named "TROPIUS" on the Raspberry Pi

To initially install tropius, execute the install.py script located in the py_tropius
folder. This will create the host and device tables in the database, and add the
TROPIUS device itself. All additions to the database are reccomended to be added
using the device or host.add commands.

NOTE: At this point you might be asking, what is the difference between a device and a host?
The answer to this, at least from the TROPIUS perspective, is that a device is anything that
TROPIUS connects to. Any additions to the TROPIUS database should be first listed as a
device and then added to its specific subtable. A host, on the otherhand, is an end computer,
more namely a desktop which is suceptable to shell commands or wake-on-lan packets.


Developer Notes:
================
Oh hi there, I'm glad you decided to come down and read this part. I'm writing this note
during the initial commit because I'm stupid ambitious in the project, but I just want to
have this forward in here for future commits.

Tropius is designed to be not only easily implemented, but also easily modifiable. Making
a home automation system to be used in other people's setups is nice and all, but its a
little bit pointless if there are not extensions for what people are actually running.
For example, I don't happen to own an automated thermostat. That'd be a great thing to
implement, but right now I really have no purpose to work on it. That being said, if you
happen to setup a TROPIUS system, and you have enough development knowledge to make an
extension that works with your automated thermostat please go right ahead.

My only real request for third party (odd term for addons to my side project) addons is
that, if you manage to get them to work, please send them to me at BradJohns94@gmail.com
so I can add them to this git repository. I am really quite fond of the concept of TROPIUS
and anything I can add to make it more usable for other people would be fantastic. So if
you, for some reason, decide to implement my kind of janky automation system and feel like
making it better, please let me know. I'd like to thank you personally.
