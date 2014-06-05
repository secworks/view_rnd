view_rnd
========
A simple program for viewing random values as an image.

# Introduction #
This program accepts an infile and generates a PNG image based on the
bytes in the given infile. Each bite is treated as a pixel with the
grayness level based on the byte value. That is, 0x00 will be black and
0xff will be white.


# Purpose #
The purpose of the program is to provide a fast and easy way for a human
to assess if a sequence of possibly random values are random, or if
there are patterns in the sequence.

This does not replace any other real tests, for example [the Dieharder
test suite](http://www.phy.duke.edu/~rgb/General/dieharder.php). Or for
that matter simply trying to compress the sequence using a good lossless
compression program.

But the human brain is relly good at finding patterns in images and this
program make it easy to use this ability to at least give a rough
feeling for the quality of randomness in the sequence of values.

The dimensions of the image (X and Y size) will impact how
the generated image looks from row to row. This program will naively
treat the image as a square with equal dimension. This also means that
for sequences that with a non integer square root, some values at the
end of the sequence will be discarded. But hey, this is just for a rough
estimate remember.


# Usage #
The program can directly show the generated image (if given the -s
flag), or save the generated image to a file.

There is also a test mode where the program instead generates an image
based on random values from the Python random number generator. In order
to have something to compare with, there is also a crappy pseudo random
number generator that can be used to generate an image.

The crappy generator is enables with the -c or --crap flag. The
generator is the one specified in the book Numerical Recipies in C.


# Implementation details #
The program is written in Python 2.X.

The program depends on the [Python Imaging Library (PIL)](). It
**Should** work with the Pillow fork of PIL, but this has not been
tested (yet).

