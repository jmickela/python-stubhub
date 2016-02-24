from base64 import b64encode
from gettext import gettext as _
from datetime import datetime, timedelta

try: import simplejson as json
except ImportError: import json

import urllib

import requests

from .exceptions import ThresholdLimitExceeded, ConnectionError, EventNotFound
from .models import StubHubEventSearchResponse, StubHubEventSectionSearchResponse, \
    StubHubInventorySearchResponse, StubHubEvent


class StubHub(object):
    STUBHUB_PRODUCTION = 'PRODUCTION'
    STUBHUB_SANDBOX = 'SANDBOX'

    url_production = "https://api.stubhub.com"
    url_sandbox = "https://api.stubhubsandbox.com"

    search_inventory_url = "/search/inventory/v1"
    search_events_url = "/search/catalog/events/v2"
    event_information_url = '/catalog/events/v2'
    login_url = '/login'
    search_inventory_section_summary_url = '/search/inventory/v1/sectionsummary'

    def __init__(self, application_token, mode=None):
        user_guid = None

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
                raise EventNotFound(_('Event not found or expired.'))
            elif response.status_code == 400 and response.content.find('INS06'):
                raise AttributeError(_('Invalid Query String/General Error'))
            elif response.status_code == 400 and response.content.find('CAS15'):
                raise AttributeError(_('Invalid date'))
            elif response.status_code == 503:
                # TODO: do a text search to make sure it really is a thresholdlimitexceeded exception
                # What the hell...they use two different error messages for the same thing!!
                if response.content.find('Threshold') != -1 or response.content.find('Throttled') != -1:
                    raise ThresholdLimitExceeded

    def search_events(self, params):
        """
        This is ALL messed up. The docs claim that you MUST use this format for dates: yyyy-mm-ddThh:mm
        they go on to claim that you can submit single dates instead of a range but their example uses the
        format yyyy-mm-dd, but this does not work, nor does supplying a single date in the 'correct' format.
        Also, if you don't supply a date many of your results will be from past dates, which will produce
        errors in virtually all other contexts (searching for tickets...)

        End result is that if the date param isn't supplied add one in that starts at the current time and
        goes for one year.

        :param params: Dictionary of values to be passed to StubHub
        :return StubHubEventSearchResponse object: a object of search results.
        """
        if not 'date' in params:
            now = datetime.now()
            next = now + timedelta(days=365)
            params['date'] = "%s TO %s" % (now.strftime("%Y-%m-%dT%H:%M"), next.strftime("%Y-%m-%dT%H:%M"))
        return self.rest_request(self.search_events_url, 'GET', params, StubHubEventSearchResponse)

    def search_inventory(self, eventid, params):
        """ Searches the inventory for matching tickets, currently uses params from the docs, should switch to a builder
        model in the future so the end user doesn't need to read the StubHub "docs".

        Note: providing a sort option is *extremely* buggy on the StubHub end. It will only work around 20% of the time.
        sort=row+asc DOES work, well, sometimes.

        Note: Providing a sectionidlist is *extremely* buggy. Sometimes it works, sometimes it doesn't.

        working options for params:
        sort: [row|...] [asc|desc]
        pricemin: (ex: '10')
        pricemax: (ex: '45')
        quantity: (ex: '2')
        sectionidlist: List of section id numbers (not names) (ex: ['273916', '273917'])


        """

        params['eventId'] = eventid
        return self.rest_request(self.search_inventory_url, 'GET', params, StubHubInventorySearchResponse)

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

    def get_event_details(self, eventid):
        if eventid is None:
            raise(AttributeError(_('You must supply an event id.')))

        return self.rest_request(self.event_information_url + "/%d" % eventid, 'GET', None, StubHubEvent)