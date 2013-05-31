#!/usr/bin/env python

import sys,yaml

def sel(name,logo,emulator):
    #show select game/cartbridge/whatever
    #call directory visualizer
    print "II"

def exit():
    sys.exit(0)


def main():
    choice = 99
    file = open("config.yaml","r")
    config = yaml.load(file)
    file.close()
    options = {0:sel,1:sel}
    for machine in config["machines"]:
        print machine
    options.update({99:exit})
    #options[choice]()
    print options


if __name__ == "__main__":
    main()
