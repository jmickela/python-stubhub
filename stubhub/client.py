from base64 import b64encode
from gettext import gettext as _

try: import simplejson as json
except ImportError: import json
import urllib

import requests

from .exceptions import ThresholdLimitExceeded, ConnectionError
from .models import StubHubEventSearchResponse, StubHubEventSectionSearchResponse


class StubHub(object):
	STUBHUB_PRODUCTION = 'PRODUCTION'
	STUBHUB_SANDBOX = 'SANDBOX'
	mode = STUBHUB_SANDBOX
	url_production = "https://api.stubhub.com"
	url_sandbox = "https://api.stubhubsandbox.com"

	search_inventory_url = "/search/inventory/v1"
	search_events_url = "/search/catalog/events/v2"
	login_url = '/login'
	search_inventory_section_summary_url = '/search/inventory/v1/sectionsummary'

	user_guid = None

	def __init__(self, application_token, mode=None):
		if mode is not None:
			self.mode = mode
		else:
			self.mode = StubHub.STUBHUB_SANDBOX


		if application_token is None:
			raise(AttributeError(_('You must supply an application token.')))
		self.application_token = application_token
		self.headers = {
			'Content-Type': 'application/json',
			'Accept': 'application/json',
			'Accept-Encoding': 'application/json',
			'Authorization': 'Bearer ' + application_token,
		}

		self.auth_info = None  # This gets set in login()

		if self.mode == self.STUBHUB_PRODUCTION:
			self.url = self.url_production
		elif self.mode == self.STUBHUB_SANDBOX:
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
		self.headers['x-stubhub-user-guid'] = response.headers['x-stubhub-user-guid']
		# replease the auth token?
		self.headers['Authentication'] = 'Bearer ' + self.auth_info['access_token']
		return True


	def rest_request(self, endpoint, method, params, response_class):
		# TODO: Basic sanity checks, response_key should be a string, response_class should be a class...
		if self.auth_info is not None:
			pass #set headers from auth info?

		response = None

		if method.lower() == 'get':
			exception = None

			try:
				response = requests.get(self.url + endpoint, params=params, headers=self.headers)
			except requests.exceptions.ConnectionError as e:
				exception = ConnectionError(_('Connection Failed: Make sure you are online and try again.'))

			if exception is not None:
				raise exception

			if response.status_code == 200:
				json = response.json()
				return response_class.from_dict(json)
			elif response.status_code == 401 and response.content.find('Invalid Credentials'):
				raise AttributeError(_('Invalid Credentials'))  # TODO: change to more appropriate exception type
			elif response.status_code == 404 and response.content.find('INS04'):
				raise AttributeError(_('Event not found or expired.'))
			elif response.status_code == 400 and response.content.find('INS06'):
				raise AttributeError(_('Invalid Query String/General Error'))
			elif response.status_code == 503:
				# TODO: do a text search to make sure it really is a thresholdlimitexceeded exception
				# What the hell...they use two different error messages for the same thing!!
				if response.content.find('Threshold') != -1 or response.content.find('Throttled') != -1:
					raise ThresholdLimitExceeded


	# streamline this! make something a little more generic
	def search_events(self, params):
		return self.rest_request(self.search_events_url, 'GET', params, StubHubEventSearchResponse)

	def search_inventory(self, eventid):
		""" FIXME: This absolutely refuses to work. The error isn't the same every time even when the input is. I'm
			wondering if this endpoint even works period.
		"""
		params = {
			'eventID': eventid,
		}

		ret = requests.get(self.url + self.search_inventory_url, params=params, headers=self.headers)
		print ret.text
		if ret.status_code == 200:
			print ret.text
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

	def search_inventory_section_summary(self, eventid):
		""" Returns information about seating sections at the event. There may not be any.

		WARNING: This information doesn't seem to be available in the sandbox environment, or at least isn't available
		all the time. If you're testing in sandbox and this code isn't working as intended, it's likely because
		you aren't getting data consistent with what you would get from the production environment.

		:param eventid: The ID of the event you're getting sections for.
		:return: a StubHubEventSectionSearchResponse object
		"""
		if eventid is None:
			raise(AttributeError(_('You must supply an event id.')))

		#  In some places the docs say to use eventid, they're wrong.
		params = {
		    'eventID': eventid,
		}

		return self.rest_request(self.search_inventory_section_summary_url, 'GET', params, StubHubEventSectionSearchResponse)
