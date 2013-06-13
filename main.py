#!/usr/bin/env python
import ConfigParser

def get_machines():
    c = ConfigParser.ConfigParser()
    c.readfp(open("config.cfg"))
    machines = []
    for s in c.sections():
        if s != "config":
            machines.append(dict(c.items(s)))
    return machines,dict(c.items("config"))

def main():
    machines,config = get_machines()
    print machines
    
    


if __name__ == "__main__":
    main()
