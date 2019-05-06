#!/bin/bash

## This script fetches just the merged ICO file from the GitHub site
## and saves it to a local dir for downstream processes

ICO='https://raw.githubusercontent.com/ICO-ontology/ICO/master/ico.owl'
OUTPUT='../ontology/ico.owl'

# get ICO file
curl $ICO --output $OUTPUT
