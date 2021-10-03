#!/usr/bin/env python3
import argparse
import logging
import sys

import lib.utilities as utilities


# enum_dns.py -f {{FullRecord}} -s {{Subject}} -d {{Domain}} -r {{Record}} -v {{Value}}
def main():
	parser = argparse.ArgumentParser(description='Enumerate DNS command line options', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-f', '--full', help='FullRecord', required=True)
	parser.add_argument('-s', '--subject', help='Subject', required=True)
	parser.add_argument('-d', '--domain', help='Domain', required=True)
	parser.add_argument('-r', '--record', help='Record', required=True)
	parser.add_argument('-v', '--value', help='Value', required=True)
	args = parser.parse_args()

	# Initialize logging
	utilities.init(utilities.OUTFILE)

	logging.info("FullRecord : {0}".format(args.full))
	logging.info("Subject    : {0}".format(args.subject))
	logging.info("Domain     : {0}".format(args.domain))
	logging.info("Record     : {0}".format(args.record))
	logging.info("Value      : {0}".format(args.value))

	sys.exit(1)


if __name__ == '__main__':
	main()
