#!/usr/bin/env python
import os
from utils.logger import *
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import re   #regular expression

#TRAIN_DATA_DIR = "C:/Users/Charlie/Documents/_UW/_Ling573_Summarization_Systems/Data/models/training/2009"
TRAIN_DATA_DIR = "/dropbox/18-19/573/Data/models/training/2009"
CONFIG_FILE_NAME = "rouge_run_D2.xml"

def get_model_file_names(eval_id):
    #matched = [i for i in os.listdir(TRAIN_DATA_DIR) if re.search(eval_id, i)]
    matched = []
    for i in os.listdir(TRAIN_DATA_DIR):
        if re.search(eval_id, i):
            #log_info("found training file {0}".format(i))
            matched.append(i)
        
    return matched
        

def create_config(src_dir, out_dir):
    #reads file names from src_dir, and generate a config file in out_dir
    log_info("creating ROUGE config file " + out_dir + "/" + CONFIG_FILE_NAME)
    
    #check existence of src_dir
    if not os.path.exists(src_dir):
        log_warn("directory {0} does not exist".format(src_dir))
        return
    
    #create out_dir folder if not existing
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    #create config file
    f_out = open(out_dir + "/" + CONFIG_FILE_NAME, "w")
    
    #form a list of lines
    lines = []
    
    #start spitting elements
    lines.append("<ROUGE_EVAL version=\"1.5.5\">")
    
    #iterate all files in src_dir
    p_id = 1
    for fn in os.listdir(src_dir):
        eval_id = fn[0:-2]
        #p_id += 1
        p_txt = fn
        lines.append("<EVAL ID=\"{0}\">".format(eval_id))
        lines.append("<PEER-ROOT>" )
        lines.append("../outputs/D2")
        lines.append("</PEER-ROOT>")
        lines.append("<MODEL-ROOT>")
        lines.append(TRAIN_DATA_DIR)
        lines.append("</MODEL-ROOT>")
        lines.append("<INPUT-FORMAT TYPE=\"SPL\">")
        lines.append("</INPUT-FORMAT>")
        lines.append("<PEERS>")
        lines.append("<P ID=\"{0}\">{1}</P>".format(p_id, p_txt))
        lines.append("</PEERS>")
        lines.append("<MODELS>")
        
        for m in get_model_file_names(eval_id):
            lines.append("<M ID=\"{0}\">{1}</M>".format(m[-1:], m))
            
        lines.append("</MODELS>")
        lines.append("</EVAL>")

        #break
        
    lines.append("</ROUGE_EVAL>")    
    
    for line in lines:
        f_out.write(line + "\n")

    log_info("ROUGE config file created: " + out_dir + "/" + CONFIG_FILE_NAME)
        
    
def main():

    create_config(src_dir ="../outputs/D2", out_dir="../config")
    
if __name__ == "__main__":
    main()

#EOF
