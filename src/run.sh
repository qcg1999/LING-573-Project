#!/bin/bash

export PYTHON_CMD=python

### train mode
$PYTHON_CMD main.py --schema $1 --mode "train"



