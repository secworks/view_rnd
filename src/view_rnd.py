#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#=======================================================================
#
# view_rnd.py
# -------------
# Accepts a file with random data (bytes) and generates a picture
# with the pixels representing the contents of the file.
#
# Note: This program requires the Python Imaging Library (PIL).
#
#
# Author: Joachim Strombergson
# Copyright (c) 2014, Secworks Sweden AB
# 
# Redistribution and use in source and binary forms, with or 
# without modification, are permitted provided that the following 
# conditions are met: 
# 
# 1. Redistributions of source code must retain the above copyright 
#    notice, this list of conditions and the following disclaimer. 
# 
# 2. Redistributions in binary form must reproduce the above copyright 
#    notice, this list of conditions and the following disclaimer in 
#    the documentation and/or other materials provided with the 
#    distribution. 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS 
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE 
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, 
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, 
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, 
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#=======================================================================

#-------------------------------------------------------------------
# Imports.
#-------------------------------------------------------------------
from PIL import Image
import math
import random
import argparse


#-------------------------------------------------------------------
# Symbolic constants.
#-------------------------------------------------------------------
VERSION = '0.1 Beta'
GEN_DIM = 1024


#-------------------------------------------------------------------
# gen_crappy_random_bytes()
#
# Generator of crappy random values. Used to test the
# image generator to show how what bad random values
# will look like.
#
# The actual generator is the Linear Congruential generator from
# Numerical Recipies in C.
#-------------------------------------------------------------------
def gen_crappy_random_bytes(num_bytes, verbose):
    if verbose:
        print "Generating %d crappy random values." % num_bytes

    values =  []
    INT32MAX = (2**32 - 1)
    state = random.randint(0, INT32MAX)
    for i in range(num_bytes):
        state = (state * 1664525 + 1013904223) % INT32MAX
        values.append(state & 0xff)
    return values


#-------------------------------------------------------------------
# gen_random_bytes()
#
# Generate an array with the given number of random bytes.
# Used for testing only.
#-------------------------------------------------------------------
def gen_random_bytes(num_bytes, verbose):
    if verbose:
        print "Generating %d random values." % num_bytes

    values = [random.randint(0,255) for i in range(num_bytes)]
    return values


#-------------------------------------------------------------------
# load_file()
#
# Load the contents of a file with the given filename and
# convert the contents to a list of values.
#-------------------------------------------------------------------
def load_file(filename, verbose):
    if verbose:
        print "Trying to read data from the file %s" % filename

    with open(filename, 'rb') as my_file:
        file_data = my_file.read()

    values = [ord(i) for i in list(file_data)]
    return values


#-------------------------------------------------------------------
# gen_image()
#
# Generates an image based on the given arguments.
#-------------------------------------------------------------------
def gen_image(args):
    verbose = args.verbose

    if verbose:
        if args.infile:
            print "Will be generating an image based on the file %s" % args.infile
        else:
            print "Will generate an image based on values from the Python random number generator."

    # Either load data or generate data.
    if args.infile:
        my_values = load_file(args.infile, verbose)
    else:
        if args.crap:
            if args.dimension:
                my_values = gen_crappy_random_bytes(args.dimension * args.dimension, verbose)
            else:
                my_values = gen_crappy_random_bytes(GEN_DIM * GEN_DIM, verbose)
        else:
            if args.dimension:
                my_values = gen_random_bytes(args.dimension * args.dimension, verbose)
            else:
                my_values = gen_random_bytes(GEN_DIM * GEN_DIM, verbose)


    dimension = int(math.sqrt(len(my_values)))
    if verbose:
        print "The generated image will have the dimension %d x %d pixels." % (dimension, dimension)


    # Create the actual image. Note that we truncate to get an exakt size
    my_pixels = [(my_values[i], my_values[i], my_values[i]) for i in range(dimension * dimension)]

    im = Image.new("RGB", (dimension, dimension))
    im.putdata(my_pixels)

    if args.show:
       im.show()
    else:
        if args.outfile:
            im.save(args.outfile+'.png', 'png')
        else:
            if args.infile:
                im.save(args.infile+'.png', 'png')
            else:
                im.save('no_name_generated_rnd.png', 'png')


#-------------------------------------------------------------------
# main()
#
# Create argparser, parse arguments and exit when no
# real operations is specified.
#-------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile',
                        help='The file with random values used to generate the image.')

    parser.add_argument('-o', '--outfile',
                        help='The file the generated image will be written to. If no name is given INFILE.png will be used.')

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Enable verbose processing.')

    parser.add_argument('-t', '--test', action='store_true',
                        help='Perform test generation using the Python random generator.')

    parser.add_argument('-c', '--crap', action='store_true',
                        help='Perform test generation using the crappy random generator from Numerical Recipies in C instead of the Python generator.')

    parser.add_argument('-d', '--dimension', type=int,
                        help='Give the dimension of the generated image. Default is 1024 pixels.')

    parser.add_argument('-s', '--show', action='store_true',
                        help='Show the image generated instead of saving it.')

    parser.add_argument('--version', action='version', version=VERSION)

    args = parser.parse_args()

    if args.infile==None and not args.test:
        print "Error: No input file given and not in test mode."
        exit(1)

    gen_image(args)

    
#-------------------------------------------------------------------
# __name__
#
# Python name mangling thingy to run if called stand alone.
#-------------------------------------------------------------------
if __name__ == '__main__':
    main()

#=======================================================================
# EOF view_rnd.py
#=======================================================================
