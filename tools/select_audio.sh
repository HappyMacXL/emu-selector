#! /bin/bash

cmd=(dialog --keep-tite --menu "ChameleonPI audio menu:" 22 76 16)

options=(0 "Auto audio"
	 1 "3.5mm socket"
	 2 "HDMI" )

choices=$("${cmd[@]}" "${options[@]}" 2>&1 >/dev/tty)

retval=$?

case $retval in
	 1) exit ;;
	 255) exit ;;
esac

echo \#! /bin/sh > set_audio.sh
echo amixer cset numid=3 $choices >> set_audio.sh
chmod +x set_audio.sh

./set_audio.sh


