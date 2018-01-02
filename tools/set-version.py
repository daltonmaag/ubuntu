#!/bin/env python3
#
# Sets the version number in the UFO metadata and inserts a special version
# glyph that helps with debugging when getting user reports.
#
# See http://silnrsi.github.io/FDBP/en-US/Versioning.html for version semantics.

import defcon
import glob
import argparse
import re
import sys

mapping = { '.': 'period', '0': 'zero', '1': 'one', '2': 'two', '3': 'three',
'4': 'four', '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine' }

parser = argparse.ArgumentParser()
parser.add_argument("version", type=str,
                    help="The version number to set (format: \d.\d\d\d)")
args = parser.parse_args()

if not re.compile("\d\.\d\d\d").match(args.version):
    print("Version argument must have the format \d.\d\d\d!")
    sys.exit(1)

versionFigures = [mapping[x] for x in args.version]
majorVersion, minorVersion = args.version.split(".")

for ufo in glob.glob("source/*.ufo"):
    print(ufo)
    font = defcon.Font(ufo)

    # Set metadata
    font.info.versionMajor = int(majorVersion)
    font.info.versionMinor = int(minorVersion)
    font.info.openTypeNameVersion = "Version " + args.version
    font.info.openTypeNameUniqueID = "{} {} Version {}".format(font.info.familyName, font.info.styleName, args.version)

    # Insert version glyph
    versionGlyph = defcon.Glyph()
    versionGlyph.unicode = 0xEFFD
    advanceWidth = 0

    if not "Mono" in ufo:
        for figure in versionFigures:
            c = defcon.Component()
            c.baseGlyph = figure
            c.transformation = (1, 0, 0, 1, advanceWidth, 0)
            advanceWidth += font[figure].width
            versionGlyph.appendComponent(c)
    else:
        c1 = defcon.Component()
        c1.baseGlyph = versionFigures[0] + ".sups"
        c1.transformation = (1, 0, 0, 1, -150, 0)
        versionGlyph.appendComponent(c1)
        c2 = defcon.Component()
        c2.baseGlyph = versionFigures[2] + ".sups"
        c2.transformation = (1, 0, 0, 1, 150, 0)
        versionGlyph.appendComponent(c2)
        c3 = defcon.Component()
        c3.baseGlyph = versionFigures[3] + ".sinf"
        c3.transformation = (1, 0, 0, 1, -150, 0)
        versionGlyph.appendComponent(c3)
        c4 = defcon.Component()
        c4.baseGlyph = versionFigures[4] + ".sinf"
        c4.transformation = (1, 0, 0, 1, 150, 0)
        versionGlyph.appendComponent(c4)
        advanceWidth = 500

    versionGlyph.width = advanceWidth

    font.insertGlyph(versionGlyph, "uniEFFD")
    font.save(ufo)
