# jrdodson
'''Basic logging utilities with standardized log format
'''
import logging
import sys

log = logging.getLogger('')
log.setLevel(logging.INFO)
format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(format)
log.addHandler(handler)

def log_info(message):
	'''log method, e.g. 
		from logger import log_info
		log_info("Hello world!")
	'''
	log.info(message)

def log_warn(message):
	'''log method, e.g.
		from logger import log_warn
		log_warn("Warning: hello world")
	'''
	log.warn(message)
