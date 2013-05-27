#!/bin/bash

TITOL=$1
CARPETA=$2
EXECUTABLE=$3
IMATGE=$4

while :
do
	clear

	FILE=$(/opt/selector/filesel.py "CHAMELEONPI" "$TITOL"  "$CARPETA" "$IMATGE" )

	echo $FILE

	if [ -e "$FILE" ] 
	then
		$EXECUTABLE "$FILE"
		CARPETA=$(dirname "$FILE")
	else
		exit
	fi

done
