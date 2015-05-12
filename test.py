import unittest
import responses

from stubhub.client import StubHub
from stubhub.models import StubHubModel

#  search response
search_json_response = '''{"numFound":281,"events":[{"id":9198987,"status":"Active","locale":"en_US","title":"They Might be Giants Tickets","description":"They Might be Giants The Neptune Tickets - Buy and sell They Might be Giants Seattle Tickets for May 7 at The Neptune in Seattle, WA on StubHub!","eventInfoUrl":"http://www.stubhub.com/they-might-be-giants-seattle-the-neptune-5-7-2015-9198987","dateLocal":"2015-05-07T20:00:00-0700","dateUTC":"2015-05-08T03:00:00+0000","venue":{"id":191876,"name":"The Neptune","venueInfoUrl":"http://www.stubhub.com/venue/the-neptune","venueEventsUrl":"http://www.stubhub.com/the-neptune-tickets","latitude":47.66126,"longitude":-122.314156,"timezone":"PST","address1":"1303 Northeast 45th Street","city":"Seattle","state":"WA","zipCode":"98105","country":"US","venueConfigId":1227725},"ticketInfo":{"minPrice":63.54,"maxPrice":95.55,"totalTickets":25.0,"totalPostings":7,"totalListings":7,"currencyCode":"USD"},"bookOfBusinessId":1,"hideEventDate":"0","hideEventTime":0,"categories":[{"id":1,"name":"Concert tickets","url":"concert-tickets"}],"groupings":[{"id":63914,"name":"Artists T - Z","url":"artists-t-z"}],"performers":[{"id":608,"name":"They Might Be Giants Tickets","url":"they-might-be-giants-tickets"}],"geos":[{"id":0,"name":"By Geography"},{"id":196976,"name":"United States"},{"id":692,"name":"Washington"},{"id":693,"name":"Seattle"},{"id":191876,"name":"The Neptune"}],"attributes":[{"name":"act_primary","value":"They Might be Giants"}]}]}'''

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

unittest.main()