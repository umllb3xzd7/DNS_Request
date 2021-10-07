import logging
import time

from lexicon.client import Client
from lexicon.config import ConfigResolver

import lib.utilities as utilities


class DNS(object):

	def __init__(self, action, challenge_domain, content):
		self.action = action
		self.content = content

		self.provider = None

		# _acme-challenge.esxi.bar.com
		self.challenge_domain = challenge_domain
		self.challenge_subdomain = None
		self.full_domain = None
		self.base_domain = None
		self.subdomain = None

	def init(self):
		# esxi.bar.com
		self.full_domain = self.challenge_domain.replace('_acme-challenge.', '')

		# bar.com
		self.base_domain = '.'.join(self.challenge_domain.split('.')[-2:])

		# esxi
		self.subdomain = self.full_domain.replace(".{0}".format(self.base_domain), '')

		# _acme-challenge.esxi
		self.challenge_subdomain = "_acme-challenge.{0}".format(self.subdomain)

		# _acme-challenge
		if (self.challenge_domain == self.challenge_subdomain):
			self.challenge_subdomain = '_acme-challenge'

		# @
		if (self.base_domain == self.subdomain):
			self.subdomain = '@'

		logging.info("DNS provider          : {0}".format(self.provider))
		logging.info("Challenge domain      : {0}".format(self.challenge_domain))
		logging.info("Challenge Subdomain   : {0}".format(self.challenge_subdomain))
		logging.info("Full domain           : {0}".format(self.full_domain))
		logging.info("Base domain           : {0}".format(self.base_domain))
		logging.info("Subdomain             : {0}".format(self.subdomain))

		# Action is 'create'
		if self.action == 'create':
			result = self.handle_create()

		# Delete the domain record
		elif self.action == 'delete':
			result = self.handle_delete()

		# List the domain record
		elif self.action == 'list':
			self.handle_list()
			result = 0

		# Any other action
		else:
			logging.error("Unsupported action: {0}".format(self.action))
			result = 1

		if self.action == 'create' or self.action == 'delete':
			logging.info('Sleeping for 30 secs to allow for DNS propagation')
			time.sleep(30)

		logging.info('Done')

		return result

	def handle_create(self):
		# Create A record
		a_create = self.do_create('A', self.subdomain, utilities.BASE_IP)
		if a_create is False:
			logging.error("Failed to create A record for {0}".format(self.full_domain))
			return 1
		elif a_create is None:
			logging.info("A record already exists for {0}, not creating".format(self.full_domain))
		else:
			logging.info("Created new A record for {0}".format(self.full_domain))

		# Create TXT record
		txt_create = self.do_create('TXT', self.challenge_domain, self.content)
		if txt_create is False:
			logging.error("Failed to create TXT record for {0}".format(self.challenge_domain))
			return 1

		logging.info("Created new TXT record for {0}".format(self.challenge_domain))

		return 0

	def handle_delete(self):
		# Delete A record
		a_delete = self.do_delete('A', self.subdomain)
		if a_delete is False:
			logging.error("Failed to delete A record for {0}".format(self.full_domain))
		elif a_delete is None:
			logging.info("A record is a restricted domain ({0}), not removing".format(self.full_domain))
		else:
			logging.info("Deleted A record for {0}".format(self.full_domain))

		# Delete TXT record
		txt_delete = self.do_delete('TXT', self.challenge_subdomain)
		if txt_delete is False:
			logging.error("Failed to delete TXT record for {0}".format(self.challenge_domain))
		elif txt_delete is None:
			logging.info("TXT record does not exist for {0}.{1}, nothing to delete".format(self.challenge_subdomain, self.base_domain))
		else:
			logging.info("Deleted TXT record for {0}".format(self.challenge_domain))

		return 0

	def handle_list(self):
		# List A record
		a_list = self.check_exists('A', self.subdomain, show=True)
		if a_list is False:
			logging.info("A record does not exist for {0}".format(self.full_domain))
		else:
			logging.info("A record exists for {0}".format(self.full_domain))

		# List TXT record
		txt_list = self.check_exists('TXT', self.challenge_domain, show=True)
		if txt_list is False:
			logging.info("TXT record does not exist for {0}".format(self.challenge_domain))
		else:
			logging.info("TXT record exists for {0}".format(self.challenge_domain))

	def send_request(self, action):
		config = ConfigResolver()
		config.with_dict(dict_object=action)

		client = Client(config)

		try:
			response = client.execute()
		except Exception as error:
			logging.info("Exception: {0}".format(error))
			return None

		return response
