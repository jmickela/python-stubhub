from base64 import b64encode

try: import simplejson as json
except ImportError: import json
import urllib

import requests

from .exceptions import ThresholdLimitExceeded
from .models import StubHubEventSearchResponse


STUBHUB_PRODUCTION = 'production'
STUBHUB_SANDBOX = 'SANDBOX'


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
	login_url = '/login'

	def __init__(self, mode=STUBHUB_PRODUCTION, application_token=None):
		self.mode = mode
		self.application_token = application_token
		self.headers = {
			'Content-Type': 'application/json',
			'Accept': 'application/json',
			'Accept-Encoding': 'application/json',
			'Authorization': 'Bearer ' + application_token,
		}

		self.auth_info = None  # This gets set in login()

		if mode == STUBHUB_PRODUCTION:
			self.url = self.url_production
		elif mode == STUBHUB_SANDBOX:
			self.url = self.url_sandbox

	def login(self, key, secret, username, password, grant_type='password'):
		auth = b64encode('%s:%s' % (key, secret))
		headers = {
			'Authorization': 'Basic ' + auth,
		    'Content-Type': 'application/x-www-form-urlencoded'
		}

		data = {
			'grant_type': grant_type,
		    'scope': self.mode,
		    'username': username,
		    'password': password,
		}

		response = requests.post(self.url + self.login_url, headers=headers, data=data)
		self.auth_info = response.json()
		return True


	def rest_request(self, endpoint, method, params, response_class):
		# TODO: Basic sanity checks, response_key should be a string, response_class should be a class...
		if self.auth_info is not None:
			pass #set headers from auth info
		if method.lower() == 'get':
			response = requests.get(self.url + endpoint, params=params, headers=self.headers)
			if response.status_code == 200:
				json = response.json()
				return response_class.from_dict(json)
			elif response.status_code == 503:
				# TODO: do a text search to make sure it really is a thresholdlimitexceeded exception
				if response.content.find('Threshold') != -1:
					raise ThresholdLimitExceeded


	# streamline this! make something a little more generic
	def search_events(self, params):
		return self.rest_request(self.search_events_url, 'GET', params, StubHubEventSearchResponse)

	def search_inventory(self, event_id, start):
		params = {
			'eventid': event_id,
		}
		ret = requests.get(self.url + self.search_inventory_url, params=params, headers=self.headers)
		print ret.text
		if ret.status_code == 200:
			print ret.text;
		elif ret.status_code == 400:
			pass
			# not logged in
			# {"errors":{"error":[{"errorType":null,"errorDescription":null,"errorMessage":"A business exception [INS06] occurred: StubHub Business Error;  Incorrect syntax in query string; details include: Requested=SearchListingCriteria{requestorUserId=null, eventid='9176901', start='null', rows='null', sort='null', pricemin='null', pricemax='null', sectionidlist='null', zoneidlist='null', quantity='null', listingattributelist='null', listingattributecategorylist='null', deliverytypelist='null', sectionstats='null', zonestats='null', pricingsummary='null', sellerformat='null', deliverytypesummary='null', listingattributecategorysummary='null'}","errorParam":null,"errorTypeId":"null"}]},"eventId":null,"totalListings":null,"totalTickets":null,"minQuantity":null,"maxQuantity":null,"mapDisplayType":null,"listing":null,"section_stats":null,"zone_stats":null,"pricingSummary":null,"listingAttributeCategorySummary":null,"deliveryTypeSummary":null,"start":null,"rows":null}

			#not event id
			#{"errors":{"error":[{"errorType":null,"errorDescription":null,"errorMessage":"A business exception [INS03] occurred: StubHub Business Error;  Event ID required; details include","errorParam":null,"errorTypeId":"null"}]},"eventId":null,"totalListings":null,"totalTickets":null,"minQuantity":null,"maxQuantity":null,"mapDisplayType":null,"listing":null,"section_stats":null,"zone_stats":null,"pricingSummary":null,"listingAttributeCategorySummary":null,"deliveryTypeSummary":null,"start":null,"rows":null}
		elif ret.status_code == 404:
			pass
			#you ge this if the event has expired or it isn't found
			#{"errors":{"error":[{"errorType":null,"errorDescription":null,"errorMessage":"A business exception [INS04] occurred: StubHub Business Error;  Incorrect event ID, or event is invalid / expired; details include: Event has expired=eventId=9198987","errorParam":null,"errorTypeId":"null"}]},"eventId":null,"totalListings":null,"totalTickets":null,"minQuantity":null,"maxQuantity":null,"mapDisplayType":null,"listing":null,"section_stats":null,"zone_stats":null,"pricingSummary":null,"listingAttributeCategorySummary":null,"deliveryTypeSummary":null,"start":null,"rows":null}
		if ret.content.find('Threshold') != -1:
			raise ThresholdLimitExceeded