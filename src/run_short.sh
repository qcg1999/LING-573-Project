#!/bin/bash

if [ $# -ge 1 ]; then
	SCHEMA=$1
else
#	SCHEMA=./test/UpdateSumm09_test_topics_short.xml
	SCHEMA=./test/UpdateSumm09_test_topics_D0934.xml
fi

#for f in $(find ../outputs/D4/. -maxdepth 1 -type f -name '*' -print) 
#do 
#	rm -f $f 
#done

# generate summary
export PYTHON_CMD=python3
### env setup
$PYTHON_CMD main.py --schema $SCHEMA --mode "train"
if [ $? -ne 0 ]; then
	exit -1
fi

### generate rouge config file
$PYTHON_CMD rouge_config_generator.py
if [ $? -ne 0 ]; then
	exit -1
fi

### generate rouge evaluation
export ROUGE_CMD=/dropbox/18-19/573/code/ROUGE/ROUGE-1.5.5.pl
export ROUGE_DATA_DIR=/dropbox/18-19/573/code/ROUGE/data
export ROUGE_CONFIG=../config/rouge_run_D4.xml
export ROUGE_OUT=../results/D4_rouge_scores.out

$ROUGE_CMD -e $ROUGE_DATA_DIR -a -n 2 -x -m -c 95 -r 1000 -f A -p 0.5 -t 0 -l 100 -s -d $ROUGE_CONFIG > $ROUGE_OUT

#eof
