#! /bin/bash

mydir=$(pwd)


cd $mydir

CHOICE=$(../menusel.py select_audio.conf)


if [ "$CHOICE" == "" ]; then
	echo Cancel
	exit
fi

rm set_audio.sh
echo \#! /bin/sh > set_audio.sh
echo "amixer cset numid=3 $CHOICE " >> set_audio.sh
chmod +x set_audio.sh

./set_audio.sh


