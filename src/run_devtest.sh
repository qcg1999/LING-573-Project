#!/bin/bash

if [ $# -ge 1 ]; then
	SCHEMA=$1
else
    #SCHEMA=./test/UpdateSumm09_test_topics_D0934.xml
	#SCHEMA=/dropbox/18-19/573/Data/Documents/training/2009/UpdateSumm09_test_topics.xml #training
	SCHEMA=/dropbox/18-19/573/Data/Documents/devtest/GuidedSumm10_test_topics.xml	#devtest
	#SCHEMA=/dropbox/18-19/573/Data/Documents/evaltest/GuidedSumm11_test_topics.xml	#evaltest
fi
# generate summary
export PYTHON_CMD=/opt/python-3.6.3/bin/python3.6
#export PYTHON_CMD=python3
OUT_DIR="../outputs/D4_devtest"   # choose one: D4, D4_devtest, D4_evaltest
MODE=dev			 # choose one: train, dev, eval 
$PYTHON_CMD main.py --schema $SCHEMA --mode $MODE --output_dir $OUT_DIR
if [ $? -ne 0 ]; then
	exit -1
fi

### generate rouge config file
CONFIG="rouge_run_D4_devtest.xml"   #change
SOURCE_DIR="../outputs/D4_devtest"  #change
$PYTHON_CMD rouge_config_generator.py --config $CONFIG --source_dir $SOURCE_DIR 
if [ $? -ne 0 ]; then
	exit -1
fi

### generate rouge evaluation
export ROUGE_CMD=/dropbox/18-19/573/code/ROUGE/ROUGE-1.5.5.pl
export ROUGE_DATA_DIR=/dropbox/18-19/573/code/ROUGE/data
export ROUGE_CONFIG=../config/rouge_run_D4_devtest.xml   #change 
export ROUGE_OUT=../results/D4_devtest_rouge_scores.out  #change 

$ROUGE_CMD -e $ROUGE_DATA_DIR -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d $ROUGE_CONFIG > $ROUGE_OUT

#eof

