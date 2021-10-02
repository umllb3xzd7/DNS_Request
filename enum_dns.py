#!/usr/bin/env python3
import argparse
import logging
import os
import sys
import time

OUTFILE = os.path.abspath("{0}/logs/dns_{1}.log".format(os.path.dirname(os.path.realpath(__file__)), time.strftime("%d-%b-%Y", time.gmtime())))


def init(logfile):
	"""
	Configure stream handler for logging messages to the console and log file.
	"""
	# Setup logging to console
	root_logger = logging.getLogger('')
	for handler in root_logger.handlers[:]:
		root_logger.removeHandler(handler)

	logging.getLogger('').setLevel(logging.INFO)
	console_log_handler = logging.StreamHandler(sys.stdout)
	console_log_handler.setLevel('INFO')
	console_log_handler.setFormatter(logging.Formatter("%(message)s"))
	logging.getLogger('').addHandler(console_log_handler)
	logging.captureWarnings(True)

	# Setup logging to file
	main_file_handler = logging.FileHandler(logfile)
	main_file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S"))
	logging.getLogger('').addHandler(main_file_handler)
	main_file_handler.setLevel(logging.INFO)

	console_log_handler.setLevel('INFO')
	logging.getLogger('filelock').setLevel(logging.WARNING)


def main():
	parser = argparse.ArgumentParser(description='Enumerate DNS command line options', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-f', '--full', help='FullRecord', required=True)
	parser.add_argument('-s', '--subject', help='Subject', required=True)
	parser.add_argument('-d', '--domain', help='Domain', required=True)
	parser.add_argument('-r', '--record', help='Record', required=True)
	parser.add_argument('-v', '--value', help='Value', required=True)
	args = parser.parse_args()

	# Initialize logging
	init(OUTFILE)

	logging.info("FullRecord : {0}".format(args.full))
	logging.info("Subject    : {0}".format(args.subject))
	logging.info("Domain     : {0}".format(args.domain))
	logging.info("Record     : {0}".format(args.record))
	logging.info("Value      : {0}".format(args.value))

	# enum_dns.py -f {{FullRecord}} -s {{Subject}} -d {{Domain}} -r {{Record}} -v {{Value}}

	sys.exit(1)


if __name__ == '__main__':
	main()
