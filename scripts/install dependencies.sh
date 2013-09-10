#!/bin/bash

os=$(uname)

unix_install () {
	echo "Downloading..."
	wget http://www.pygame.org/ftp/pygame-1.9.1release.zip >/dev/null 2>&1

	echo "Unpacking..."
	unzip -q pygame-1.9.1release.zip

	echo "Installing..."
	cd pygame-1.9.1release
	sudo python ./setup.py install
	cd ..

	echo "Cleaning..."
	rm -r pygame-1.9.1release
	rm pygame-1.9.1release.zip

	echo "Successfully installed for $os!"
}

if [ $os = 'Linux' ]; then
	echo "The dependencies will be installed for Linux"
	unix_install
elif [ $os = 'Darwin' ]; then
	echo "The dependencies will be installed for Mac OS X"
	unix_install
else
	echo "Your platform ($os) is not supported!"
fi