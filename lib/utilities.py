import logging
import os
import sys
import time
import yaml

CONFIG = os.path.abspath("{0}/../config.yml".format(os.path.dirname(os.path.realpath(__file__))))
OUTFILE = os.path.abspath("{0}/../logs/dns_{1}.log".format(os.path.dirname(os.path.realpath(__file__)), time.strftime("%d-%b-%Y", time.gmtime())))


def parse_config(item, subkey=None):
	"""
	Parse yaml configuration file.
	"""
	with open(os.path.abspath(CONFIG), 'r') as f:
		config_data = yaml.safe_load(f)

	if subkey is None:
		config_item = config_data[item]
	else:
		config_item = config_data[item][subkey]

	return config_item


NO_REMOVE = parse_config('general', 'restricted')
NAMECHEAP_DOMAINS = parse_config('namecheap', 'domains')
BASE_IP = parse_config('general', 'base_ip')


def get_provider(domain):
	for d in NAMECHEAP_DOMAINS:
		if d.lower() in domain:
			return 'namecheap'

	return 'godaddy'


def is_restricted(domain):
	for d in NO_REMOVE:
		if d.lower() == domain.lower():
			return True

	return False


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
