Oh hey there! This is the tmp folder!

I really don't know a good way of distributing these files since they're not
actually supposed to be anywhere in the TROPIUS code base and should immediately
be moved to /etc/systemd/system on the install, so tmp seemed like a good place
to me. So... yeah, in case you were curious these are the fancy magic files that
tell arch that programs like state.py and app.py are daemons and should be
executed on startup.
