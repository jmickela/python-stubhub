import unittest
import responses

from stubhub.client import StubHub
from stubhub.models import StubHubModel

""" WARNING:
Testing actual responses can be difficult since the basic access tier is only allowed 10 requests an hour.
This means that this client has NO TESTS that test actual API interaction, only recorded responses for various
inputs. Should StubHub modify their sandbox so that you have a much higher usage threshold this can be changed.
"""

#  search response, 281 found, 1 actual result
search_events_json_response = '''{"numFound":281,"events":[{"id":9198987,"status":"Active","locale":"en_US","title":"They Might be Giants Tickets","description":"They Might be Giants The Neptune Tickets - Buy and sell They Might be Giants Seattle Tickets for May 7 at The Neptune in Seattle, WA on StubHub!","eventInfoUrl":"http://www.stubhub.com/they-might-be-giants-seattle-the-neptune-5-7-2015-9198987","dateLocal":"2015-05-07T20:00:00-0700","dateUTC":"2015-05-08T03:00:00+0000","venue":{"id":191876,"name":"The Neptune","venueInfoUrl":"http://www.stubhub.com/venue/the-neptune","venueEventsUrl":"http://www.stubhub.com/the-neptune-tickets","latitude":47.66126,"longitude":-122.314156,"timezone":"PST","address1":"1303 Northeast 45th Street","city":"Seattle","state":"WA","zipCode":"98105","country":"US","venueConfigId":1227725},"ticketInfo":{"minPrice":63.54,"maxPrice":95.55,"totalTickets":25.0,"totalPostings":7,"totalListings":7,"currencyCode":"USD"},"bookOfBusinessId":1,"hideEventDate":"0","hideEventTime":0,"categories":[{"id":1,"name":"Concert tickets","url":"concert-tickets"}],"groupings":[{"id":63914,"name":"Artists T - Z","url":"artists-t-z"}],"performers":[{"id":608,"name":"They Might Be Giants Tickets","url":"they-might-be-giants-tickets"}],"geos":[{"id":0,"name":"By Geography"},{"id":196976,"name":"United States"},{"id":692,"name":"Washington"},{"id":693,"name":"Seattle"},{"id":191876,"name":"The Neptune"}],"attributes":[{"name":"act_primary","value":"They Might be Giants"}]}]}'''
inventory_search_404_json = '''{"errors":{"error":[{"errorType":null,"errorDescription":null,"errorMessage":"A business exception [INS04] occurred: StubHub Business Error;  Incorrect event ID, or event is invalid / expired; details include: Event has expired=eventId=9150536","errorParam":null,"errorTypeId":"null"}]},"eventId":null,"totalListings":null,"totalTickets":null,"minQuantity":null,"maxQuantity":null,"mapDisplayType":null,"listing":null,"section_stats":null,"zone_stats":null,"pricingSummary":null,"listingAttributeCategorySummary":null,"deliveryTypeSummary":null,"start":null,"rows":null}'''
inventory_search_400_error_json = '''{"errors":{"error":[{"errorType":null,"errorDescription":null,"errorMessage":"A business exception [INS06] occurred: StubHub Business Error;  Incorrect syntax in query string; details include: Requested=SearchListingCriteria{requestorUserId=null, eventid='9177000', start='null', rows='null', sort='null', pricemin='null', pricemax='null', sectionidlist='null', zoneidlist='null', quantity='null', listingattributelist='null', listingattributecategorylist='null', deliverytypelist='null', sectionstats='null', zonestats='null', pricingsummary='null', sellerformat='null', deliverytypesummary='null', listingattributecategorysummary='null', allSectionZoneStats='null'}","errorParam":null,"errorTypeId":"null"}]},"eventId":null,"totalListings":null,"totalTickets":null,"minQuantity":null,"maxQuantity":null,"mapDisplayType":null,"listing":null,"section_stats":null,"zone_stats":null,"pricingSummary":null,"listingAttributeCategorySummary":null,"deliveryTypeSummary":null,"start":null,"rows":null}'''

# siss
siss_404_error_json = '''{"errors":{"error":[{"errorType":null,"errorDescription":null,"errorMessage":"A business exception [INS04] occurred: StubHub Business Error;  Incorrect event ID, or event is invalid / expired; details include: Event is not active=eventId=9098987","errorParam":null,"errorTypeId":"null"}]},"eventId":null,"eventDescription":null,"section":null,"currencyCode":null,"isVenueScrubbed":null,"isViewFromSectionEnabled":null,"smallViewFromSectionUrl":null,"mediumViewFromSectionUrl":null,"largeViewFromSectionUrl":null}'''
siss_400_error_json = '''{"errors":{"error":[{"errorType":null,"errorDescription":null,"errorMessage":"A business exception [ISS06] occurred: StubHub Business Error;  Incorrect syntax in query string; details include: Requested=ListingSectionSummaryCriteria{eventid='9177000', pricemin='null', pricemax='null', sectionidlist='null', quantity='null', listingattributelist='null', listingattributecategorylist='null', deliverytypelist='null', sort='null'}","errorParam":null,"errorTypeId":"null"}]},"eventId":null,"eventDescription":null,"section":null,"currencyCode":null,"isVenueScrubbed":null,"isViewFromSectionEnabled":null,"smallViewFromSectionUrl":null,"mediumViewFromSectionUrl":null,"largeViewFromSectionUrl":null}'''

siss_200_event_id = 9177000
siss_200_json = '''{"errors":null,"eventId":9177000,"eventDescription":"Colorado Rockies at Los Angeles Dodgers Tickets (Friday Night Fireworks)","section":[],"currencyCode":"USD","isVenueScrubbed":true,"isViewFromSectionEnabled":true,"smallViewFromSectionUrl":"cache11.stubhubstatic.com/sectionviews/venues/744/config/154129/195x106","mediumViewFromSectionUrl":"cache11.stubhubstatic.com/sectionviews/venues/744/config/154129/500x271","largeViewFromSectionUrl":"cache11.stubhubstatic.com/sectionviews/venues/744/config/154129/1000x542"}'''


class StubHubClientTest(unittest.TestCase):
	def test_client_no_token(self):
		with self.assertRaises(AttributeError) as context:
			StubHub(None)
		self.assertTrue('You must supply an application token.' in context.exception)

	def test_sandbox_mode_url(self):
		client = StubHub(application_token="some token", mode=StubHub.STUBHUB_SANDBOX)
		self.assertEqual(client.url, client.url_sandbox)

	def test_production_mode_url(self):
		client = StubHub(application_token="some token", mode=StubHub.STUBHUB_PRODUCTION)
		self.assertEqual(client.url, client.url_production)

	def test_default_mode(self):
		client = StubHub(application_token="some token")
		self.assertEqual(client.url, client.url_sandbox)

	@responses.activate
	def test_search_result(self):
		client = StubHub(application_token='some token')

		responses.add(responses.GET, client.url + client.search_events_url,
				body=search_events_json_response, status=200,
				content_type='application/json')

		response = client.search_events({'test': 'search'})
		self.assertEqual(response.numFound, 281)
		self.assertEqual(response.events[0].title, "They Might be Giants Tickets")
		self.assertEqual(response.events[0].id, 9198987)

class StubHubSearchTest(unittest.TestCase):
	client = None

	def setUp(self):
		self.client = StubHub(application_token="some token")

	# siss = Search Inventory Section Summary
	@responses.activate
	def test_siss_no_eventid(self):
		""" Make sure an exception is thrown if no even id is given.
		:return: boolean Whether the test passed or failed
		"""
		# this shouldn't be used, but in the event that the exception isn't throw I don't want to hit the real API
		responses.add(responses.GET, self.client.url + self.client.search_events_url,
				body=search_events_json_response, status=200,
				content_type='application/json')

		with self.assertRaises(AttributeError) as context:
			self.client.search_inventory_section_summary(None)
		self.assertTrue('You must supply an event id.' in context.exception)
	@responses.activate
	def test_siss_past_eventid(self):
		#  If you pass in an event id of an old even it should throw an exception
		responses.add(responses.GET, self.client.url + self.client.search_events_url,
				body=search_events_json_response, status=200,
				content_type='application/json')

unittest.main()