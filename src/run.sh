#!/bin/bash

export PYTHON_CMD=python3

### env setup
$PYTHON_CMD -m venv .env
source .env/bin/activate
.env/bin/$PYTHON_CMD -m pip install --upgrade pip && .env/bin/$PYTHON_CMD -m pip install --upgrade setuptools && 
.env/bin/$PYTHON_CMD -m pip install -r requirements.txt 
.env/bin/$PYTHON_CMD -m spacy download en

### train mode
.env/bin/$PYTHON_CMD src/main.py --schema $1 --mode "train"

### generate rouge config file
.env/bin/$PYTHON_CMD src/rouge_config_generator.py

### generate rouge evaluation
export ROUGE_CMD=/dropbox/18-19/573/code/ROUGE/ROUGE-1.5.5.pl
export ROUGE_DATA_DIR=/dropbox/18-19/573/code/ROUGE/data
export ROUGE_CONFIG=config/rouge_run_D2.xml
export ROUGE_OUT=results/D2_rouge_scores.out

$ROUGE_CMD -e $ROUGE_DATA_DIR -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d $ROUGE_CONFIG > $ROUGE_OUT

#eof



