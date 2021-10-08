#!/usr/bin/env python3
import argparse
import logging
import os
import sys
import time

import lib.utilities as utilities

from lib.namecheap import Namecheap
from lib.godaddy import GoDaddy


def main():
	parser = argparse.ArgumentParser(description='Add or remove DNS entry for DNS name providers', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('action', help='Action to perform', choices=['create', 'list', 'update', 'delete'])
	parser.add_argument('-d', '--domain', help='Domain (ex: bar.com)', required=True)
	parser.add_argument('-c', '--content', help='Record content', required=False)
	args = parser.parse_args()

	# Initialize logging
	utilities.init(utilities.OUTFILE)

	if (args.action != 'list' and args.content is None):
		print("[-] Error: Please provide an arguments for -c/--content")
		return

	provider = utilities.get_provider(args.domain)
	if provider == 'namecheap':
		dns = Namecheap(args.action, args.domain, args.content)
	else:
		dns = GoDaddy(args.action, args.domain, args.content)

	result = dns.run()
	sys.exit(result)


if __name__ == '__main__':
	main()
