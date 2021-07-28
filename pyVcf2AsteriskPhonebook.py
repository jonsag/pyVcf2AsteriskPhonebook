#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Encoding: UTF-8

# import modules
import getopt, os, sys

# import modules from file modules.py
from modules import (onError, usage, 
                     readVcard)

# handle options and arguments passed to script
try:
    myopts, args = getopt.getopt(sys.argv[1:],
                                 'i:wo:vh',
                                 ['infile=', 'write', 'outfile=', 'verbose', 'help'])

except getopt.GetoptError as e:
    onError(1, str(e))

# if no options passed, then exit
if len(sys.argv) == 1:  # no options passed
    onError(2, "No options given")

inFile = ""
writeDB = False
outFile = ""
verbose = False
    
# interpret options and arguments
for option, argument in myopts:
    if option in ('-i', '--infile'):
        inFile = argument
    elif option in ('-w', '--write'):
        writeDB = True
    elif option in ('-o', '--outfile'):
        outFile = argument
    elif option in ('-v', '--verbose'):  # verbose output
        verbose = True
    elif option in ('-h', '--help'):  # display help text
        usage(0)
       
if not inFile:
    onError(3, "No infile")
else:
    if not os.path.isfile(inFile):
        onError(5, "%s is not a file" % inFile)
    else:
     f = open(inFile, "r") # open inFile
     firstLine = f.readline().strip()
     if not "BEGIN:VCARD" in firstLine:
         onError(6, "This is not a vcard file")

if writeDB and outfile:
    onError(7, "Choose ONE of -w (--write) and -o (--outfile")
         
readVcard(inFile, writeDB, outFile, verbose)
