#! /bin/bash

choice=2

_main () 
{


	cd /opt/selector
	clear

	joy2key -config CHAMELEON  > /dev/null 2>&1 &
	./emlaunch.py $choice
	choice=$?
	killall joy2key > /dev/null 2>&1

	case $choice in
#v0.1
		2) cd /roms/spectrum
		fuse
		  _main ;;
		3) stella
		  _main ;;
		4) scummvm
		  _main ;;
		5)
		cd /opt/liapple
		./linapple
		_main ;;
		6) cd /opt/Oricutron_src_v09 
		oricutron -m oric1 --fullscreen
		_main ;;
		7) advmenu
		_main ;;
		8) 
		dosbox
		_main ;;
		9) 
		cd /roms/c64
		x64
		_main ;;
		10) 
		cd /roms/vic20
		xvic
		_main ;;
		11) 
		x128
		_main ;;
		12) cd /opt/Oricutron_src_v09 
		oricutron -m atmos --fullscreen
		_main ;;
		13) cd /opt/sz81-2.1.7
		./sz81
		_main ;;
		14) 
		hatari
		_main ;;
		15) 
		cd /opt/caprice32-4.2.0-src
		/opt/selector/amstradfiles.sh "CAPRICE " "/roms/amstrad/disk/" "./cap32 " "/opt/selector/imatges/cpc464.png"
		_main ;;
#v0.3
		16) 
		./listfiles_sdl.sh "DGEN " "/roms/megadrive/" "/opt/dgen-sdl-1.32/dgen " "/opt/selector/imatges/megadrive.png"
		_main ;;

		17) 
		./listfiles_sdl.sh "OPENMSX CARTRIDGE" "/roms/msx/" "openmsx -cart" "/opt/selector/imatges/msx.png"
		_main ;;

		18) 
		cd /opt/atari800-2.2.1
		./atari800
		_main ;;
		19) 
		/opt/selector/listfiles_sdl.sh "RETROARCH SNES " "/roms/snes/" "retroarch -L /opt/ra_cores/pocketsnes-libretro/libretro.so " "/opt/selector/imatges/snes.png"
		_main ;;
		20) 
		/opt/selector/listfiles_sdl.sh "RETROARCH NES " "/roms/nes/" "retroarch -L /usr/lib/libretro-fceu.so " "/opt/selector/imatges/nes.png"
		_main ;;
		21)	
			/opt/selector/listfiles_sdl.sh "GNUBOY " "/roms/gameboy/" "/opt/gnuboy-1.0.3.orig/sdlgnuboy --scale=4 " "/opt/selector/imatges/gameboy.png"
			_main ;;



#v0.2
#		10) 
#		cd /opt/simcoupe
#		./simcoupe
#		_main ;;


#v0.1
		52)
		cd /opt/usp_0.0.43
		./unreal_speccy_portable
		  _main ;;
#v0.3
		57)	
			/opt/selector/listfiles_sdl.sh "RETROARCH MAME " "/roms/mame/rom/" "retroarch -L /usr/lib/libretro-imame4all.so " "/opt/selector/imatges/mamesm.png"
			_main ;;

		58)	
			cd /opt/rpix
			./rpix86 -a1 -d/roms/dos -f0 -w1920 -h1080
			_main ;;

		65)
                cd /opt/arnold
				/opt/selector/listfiles_sdl.sh "ARNOLD " "/roms/amstrad/disk/" "./arnold -drivea " "/opt/selector/imatges/cpc464.png"
                  _main ;;
		71) 
		/opt/selector/listfiles_sdl.sh "VISUALBOYADVANCE " "/roms/gameboy/" "VisualBoyAdvance --auto-frameskip " "/opt/selector/imatges/gameboy.png"
		_main ;;

#v0.2
		72)
		fbzx
		_main ;;


		100) 
		cd
		/bin/bash
		exit ;;

#v0.3
		199) 
		cd /opt/selector/tools
		./options_sdl.sh
		exit ;;

#v0.1
		0)
			clear 
			exit ;;
		1)
			#clear 
			exit ;;
	esac
}

if [[ $(who am i) =~ \([0-9\.]+\)$ ]]; then echo ; else _main; fi
#_main


