import logging

import lib.utilities as utilities

from .main import DNS


class GoDaddy(DNS):

	GD_ACTION_TEMPLATE = {
		'provider_name': 'godaddy',
		'godaddy': {
			'auth_key': '',
			'auth_secret': ''
		}
	}

	def run(self):
		self.provider = 'godaddy'
		self.init()

	def check_exists(self, record, subdomain, show=False):
		action_options = self.GD_ACTION_TEMPLATE.copy()

		action_options['action'] = 'list'
		action_options['type'] = record
		action_options['domain'] = self.base_domain
		action_options['name'] = subdomain

		response = self.send_request(action_options)
		if response is None or len(response) <= 0:
			return False

		if show is True:
			logging.info(response)

		if response[0]['content'] != self.content:
			return False

		return True

	def do_create(self, record, subdomain, content):
		# Check if record exists
		exists = self.check_exists(record, subdomain)
		if exists is True and record != 'TXT':
			return None

		# If TXT record, delete before creating
		elif exists is True and record == 'TXT':
			logging.info("{0} record already exists for {1}, removing".format(record, self.full_domain))

			txt_delete = self.do_delete(record, self.challenge_domain)
			if txt_delete is False:
				logging.error("Failed to delete old TXT record for {0}".format(self.challenge_domain))
				return False

			logging.info("Deleted old TXT record for {0}".format(self.challenge_domain))

		# Record does not exist, create it
		else:
			logging.info("{0} record does not exist for {1}, creating".format(record, subdomain))

		action_options = self.GD_ACTION_TEMPLATE.copy()
		action_options['action'] = 'create'
		action_options['type'] = record
		action_options['ttl'] = 600
		action_options['domain'] = self.base_domain
		action_options['name'] = subdomain
		action_options['content'] = content

		logging.info("Creating {0} record with {1} content".format(record, content))

		response = self.send_request(action_options)
		if response is not True:
			return False
		else:
			return True

	def do_delete(self, record, subdomain):
		# A record is restricted, DO NOT REMOVE
		if utilities.is_restricted(self.full_domain) is True and record == 'A':
			return None

		# Check if record exists
		exists = self.check_exists(record, subdomain)
		if exists is False:
			return None

		# A record exists, remove it
		logging.info("{0} record exists for {1}.{2}, removing".format(record, subdomain, self.base_domain))

		action_options = self.GD_ACTION_TEMPLATE.copy()
		action_options['action'] = 'delete'
		action_options['type'] = record
		action_options['domain'] = self.base_domain
		action_options['name'] = subdomain

		response = self.send_request(action_options)
		if response is not True:
			return False
		else:
			return True
