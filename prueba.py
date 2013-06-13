#!/usr/bin/python

 
def zero(int=123):
    print "You typed zero %d.\n" %int
 
def sqr():
    print "n is a perfect square\n"
 
def even():
    print "n is an even number\n"
 
def prime():
    print "n is a prime number\n"

options = {0 : zero,
                1 : sqr,
                4 : sqr,
                9 : sqr,
                2 : even,
                3 : prime,
                5 : prime,
                7 : prime,
}
zero(212)
options[0](1234123)
