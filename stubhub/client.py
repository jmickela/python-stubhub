try: import simplejson as json
except ImportError: import json
import urllib

import requests

STUBHUB_PRODUCTION = 'production'
STUBHUB_SANDBOX = 'sandbox'
from .models import StubHubEvent

class StubHub():
	url_production = "https://api.stubhub.com"
	url_sandbox = "https://api.stubhubsandbox.com"

	search_inventory_url = "/search/inventory/v1"
	search_events_url = "/search/catalog/events/v2"

	def __init__(self, mode=STUBHUB_PRODUCTION, application_token=None):
		self.mode = mode
		self.application_token = application_token
		self.headers = {
			'Content-Type': 'application/json',
			'Accept': 'application/json',
			'Accept-Encoding': 'application/json',
			'Authorization': 'Bearer ' + application_token,
		}

		if mode == STUBHUB_PRODUCTION:
			self.url = self.url_production
		elif mode == STUBHUB_SANDBOX:
			self.url = self.url_sandbox

	# streamline this! make something a little more generic
	def search_inventory(self, search_terms):
		qs = urllib.urlencode(search_terms)
		ret = requests.get("%s%s?%s" % (self.url, self.search_events_url, qs), headers=self.headers)
		print ret.text
		if ret.status_code == 200:
			data = json.loads(ret.text)
			events = []
			for event in data['events']:
				events.append(StubHubEvent(event))
			return events
		elif ret.status_code == 503:
			# 503 errors may mean you are over your usage threshold, which is easy because the
			# basic level only gets 10 calls per hour.
			return None