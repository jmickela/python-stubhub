try: import simplejson as json
except ImportError: import json
import urllib

import requests

from .models import StubHubEventSearchResponse

STUBHUB_PRODUCTION = 'production'
STUBHUB_SANDBOX = 'sandbox'


def rest_method(url, method, headers, arguments, handler):
	if method == 'GET':
		ret = requests.get(url, params=arguments, headers=headers)

		if ret.status_code == 200:
			return handler(ret.json())
		elif ret.status_code == 503:
			# 503 errors may mean you are over your usage threshold, which is easy because the
			# basic level only gets 10 calls per hour.
			return None

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

	def rest_request(self, endpoint, method, params, response_class):
		# TODO: Basic sanity checks, response_key should be a string, response_class should be a class...

		if method.lower() == 'get':
			response = requests.get(self.url + endpoint, params=params, headers=self.headers)
			if response.status_code == 200:
				json = response.json()
				return response_class.from_dict(json)


	# streamline this! make something a little more generic
	def search_events(self, params):
		return self.rest_request(self.search_events_url, 'GET', params, StubHubEventSearchResponse)

	def search_inventory(self, event_id):
		ret = requests.get(self.url + self.search_inventory_url, params={'event_id': event_id}, headers=self.headers)

		if ret.status_code == 200:
			return None
		elif ret.status_code == 503:
			return None