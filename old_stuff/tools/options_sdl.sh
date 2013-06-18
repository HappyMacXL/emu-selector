#! /bin/bash

mydir=$(pwd)


while :
do
	cd $mydir

	CHOICE=$(../menusel.py options.conf)

	if [ "$CHOICE" == "" ]; then
		echo Cancel
		exit
	fi

	clear

	case $CHOICE in
		0)
			echo exit
			exit
			;;
		99)
			echo exit
			exit
			;;
		1)
			cd
			/bin/bash
			;;

	esac

done
