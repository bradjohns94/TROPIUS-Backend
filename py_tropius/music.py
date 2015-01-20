# right now this is just a doc file
# The base to any vlc command is going to go as follows:
#   curl -i -u :password http://<ip address>:<port>/requests/
# Afterwards there are 2 primary xml files in use:
#   playlist.xml
#   status.xml
# We will use playlist.xml to get xml data so we can get the ids of
# songs that vlc has in its media library.
# From here we have the base url and the xml file. If we are running
# a status command the command is as follows:
#   curl -i -u :password http://<ip address>:<port>/requests/status.xml?command="command&[options]"
# status xml is to use actual commands. Known commands go as follows:
# The following is a list of commands I know that TROPIUS should use:
#   pl_play
#       pl_play&id=<id recieved from playlist.xml>
#   pl_pause
#   pl_stop
#   pl_next
#   pl_previous
#   pl_random
