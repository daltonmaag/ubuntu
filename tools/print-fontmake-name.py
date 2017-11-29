#!/bin/env python3
#
# Takes an .ufo file directory and prints the name fontmake 1.3.0 constructs for
# the output binary. Used in the Makefile to find the file that a fontmake run
# produced. Remove when fontmake grows an --output parameter.

import argparse
from ufoLib import UFOReader


# An empty object that UFOReader can attach attributes to.
class InfoObject(object):
    pass


parser = argparse.ArgumentParser()
parser.add_argument(
    "ufo", type=str, help="The path to the UFO whose name you want to print.")
args = parser.parse_args()

ufo = UFOReader(args.ufo)
info = InfoObject()
ufo.readInfo(info)

name = '{}-{}'.format(info.familyName.replace(' ', ''),
                      info.styleName.replace(' ', ''))

print(name)
