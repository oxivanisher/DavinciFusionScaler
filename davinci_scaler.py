#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import logging
import os

level = logging.INFO
if os.environ.get("DEBUG", "true").lower() == "true":
    level = logging.DEBUG

logging.basicConfig(
    format="%(asctime)s %(levelname)-7s %(message)s",
    datefmt="%Y-%d-%m %H:%M:%S",
    level=level,
)

@click.command()
@click.option('--input_file', prompt='Input filename', help='The settings file to be read')
@click.option('--output_file', prompt='Output filename', help='The settings file to be written')
@click.option('--multiplier', prompt='Multiplier', help='The multiplier to be applied to the .settings file',
              type=float)
def scale(input_file, output_file, multiplier):
    """This program scales keyframes in Davinci Resolve .settings files."""

    logging.info("Loading file %s" % input_file)
    with open(input_file) as f:
        content = f.readlines()
    # remove whitespaces at the end of the line (\n)
    content = [x.rstrip() for x in content]

    keyframes_line_found = False
    indentation = 0
    line_number = 0
    converted_keyframes = 0
    output = []
    for line in content:
        line_number += 1
        if "KeyFrames = {" in line:
            logging.info("Found keyframe start line in %s" % line_number)
            keyframes_line_found = True
            indentation = len(line) - len(line.lstrip())
        elif line == "%s}" % ("\t" * indentation):
            logging.info("Found keyframe end line in %s" % line_number)
            keyframes_line_found = False
            indentation = 0
        elif keyframes_line_found:
            indentation_string = "\t" * (indentation + 1)
            clean_line = line[len(indentation_string):]

            # some sanity checks to be sure
            if not line.startswith(indentation_string):
                logging.error("Not enough indentation found in line %s. Something is fishy!" % line_number)
                raise
            if not clean_line.startswith('['):
                logging.error("Line %s not starting with a KeyFrame definition [. Something is fishy!" % line_number)
                raise
            keyframe = line[(indentation + 2):line.find(']')]
            converted_keyframe = float(keyframe) * multiplier
            converted_keyframes += 1
            logging.info("Converted keyframe %s to %s" % (str(keyframe), str(converted_keyframe).replace('.0', '')))
            line = line.replace("[%s]" % keyframe, "[%s]" % str(converted_keyframe).replace('.0', ''), 1)

        output.append(line)

    logging.info("Writing %s lines with %s converted keyframes to output file %s" % (line_number, converted_keyframes,
                                                                                     output_file))
    with open(output_file, 'w') as f:
        for line in output:
            f.write("%s\n" % line)


if __name__ == '__main__':
    scale()
