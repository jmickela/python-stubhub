

class StubHubModel(object):
	"""Base model for StubHub models
	Normally, models should be created using the from_dict method, which accepts the dict created from the raw
	json data. Since StubHub returns nested json special cases have to be added to prevent trying to add
	nested data to a parent class (add venue data to an event class).
	"""

	@classmethod
	def from_dict(cls, data):
		"""Turns a dict into either a single class or a collection of classes, depending on the contents of the dict.

		Args:
			data (dict): A dict created from json returned from a call to the StubHub api.
		"""
		instance = cls()
		for key, value in data.items():
			instance.__dict__[key] = value
		return instance

	def __init__(self):
		print 'in init'


class StubHubVenue(StubHubModel):
	id = None
	name = None
	venue_info_url = None
	venue_events_url = None
	latitude = None
	longitude = None
	timezone = None
	address1 = None
	address2 = None
	city = None
	state = None
	zip_code = None
	country = None
	venue_config_id = None  # what is this?


class StubHubTicketInfo(StubHubModel):
	min_price = None
	max_price = None
	total_tickets = None
	total_postings = None
	total_listings = None  # is this not the same as total postings?
	currency_code = None


class StubHubCategory(StubHubModel):
	id = None
	name = None
	url = None


class StubHubGrouping(StubHubModel):
	id = None
	name = None
	url = None


class StubHubPerformer(StubHubModel):
	id = None
	name = None
	url = None


class StubHubGeo(StubHubModel):
	id = None
	name = None


class StubHubEventAttribute(StubHubModel):
	name = None
	value = None

data = """{"numFound":281,"events":[{"id":9199069,"status":"Active","locale":"en_US","title":"They Might Be Giants Tickets","description":"They Might Be Giants Echoplex Tickets - Buy and sell They Might Be Giants Los Angeles Tickets for May 1 at Echoplex in Los Angeles, CA on StubHub!","eventInfoUrl":"http://www.stubhub.com/they-might-be-giants-los-angeles-echoplex-5-1-2015-9199069","dateLocal":"2015-05-01T20:00:00-0700","dateUTC":"2015-05-02T03:00:00+0000","venue":{"id":124302,"name":"Echoplex","venueInfoUrl":"http://www.stubhub.com/venue/echoplex","venueEventsUrl":"http://www.stubhub.com/echoplex-tickets","latitude":34.07732,"longitude":-118.26084,"timezone":"PST","address1":"1154 Glendale Blvd","city":"Los Angeles","state":"CA","zipCode":"90026","country":"US","venueConfigId":257136},"ticketInfo":{"minPrice":0.0,"maxPrice":0.0,"totalTickets":0.0,"totalPostings":0,"totalListings":0,"currencyCode":"USD"},"bookOfBusinessId":1,"hideEventDate":"0","hideEventTime":0,"categories":[{"id":1,"name":"Concert tickets","url":"concert-tickets"}],"groupings":[{"id":63914,"name":"Artists T - Z","url":"artists-t-z"}],"performers":[{"id":608,"name":"They Might Be Giants Tickets","url":"they-might-be-giants-tickets"}],"geos":[{"id":0,"name":"By Geography"},{"id":196976,"name":"United States"},{"id":4,"name":"California"},{"id":10,"name":"Los Angeles Metro"},{"id":124302,"name":"Echoplex"}],"attributes":[{"name":"act_primary","value":"They Might Be Giants"},{"name":"act_secondary","value":"secondary_field"}]},{"id":9199014,"status":"Active","locale":"en_US","title":"They Might be Giants Tickets","description":"They Might be Giants Stubbs BarBQ Tickets - Buy and sell They Might be Giants Austin Tickets for May 14 at Stubbs BarBQ in Austin, TX on StubHub!","eventInfoUrl":"http://www.stubhub.com/they-might-be-giants-austin-stubbs-barbq-5-14-2015-9199014","dateLocal":"2015-05-14T20:00:00-0500","dateUTC":"2015-05-15T01:00:00+0000","venue":{"id":37078,"name":"Stubbs BarBQ","venueInfoUrl":"http://www.stubhub.com/venue/stubbs-restaraunt","venueEventsUrl":"http://www.stubhub.com/stubbs-restaraunt-event-tickets","latitude":30.26857,"longitude":-97.736084,"timezone":"CST","address1":"801 Red River","city":"Austin","state":"TX","zipCode":"78701","country":"US","venueConfigId":1226007},"ticketInfo":{"minPrice":63.87,"maxPrice":72.0,"totalTickets":8.0,"totalPostings":3,"totalListings":3,"currencyCode":"USD"},"bookOfBusinessId":1,"hideEventDate":"0","hideEventTime":0,"categories":[{"id":1,"name":"Concert tickets","url":"concert-tickets"}],"groupings":[{"id":63914,"name":"Artists T - Z","url":"artists-t-z"}],"performers":[{"id":608,"name":"They Might Be Giants Tickets","url":"they-might-be-giants-tickets"}],"geos":[{"id":0,"name":"By Geography"},{"id":196976,"name":"United States"},{"id":671,"name":"Texas"},{"id":707,"name":"Austin / San Antonio"},{"id":37078,"name":"Stubbs BarBQ"}],"attributes":[{"name":"act_primary","value":"They Might be Giants"}]},{"id":9195518,"status":"Active","locale":"en_US","title":"They Might Be Giants Tickets","description":"They Might Be Giants Barrymore Theatre - Wisconsin Tickets - Buy and sell They Might Be Giants Madison Tickets for April 19 at Barrymore Theatre - Wisconsin in Madison, WI on StubHub!","eventInfoUrl":"http://www.stubhub.com/they-might-be-giants-madison-barrymore-theatre---wisconsin-4-19-2015-9195518","dateLocal":"2015-04-19T19:30:00-0500","dateUTC":"2015-04-20T00:30:00+0000","venue":{"id":65682,"name":"Barrymore Theatre - Wisconsin","venueInfoUrl":"http://www.stubhub.com/venue/barrymore-theatre-wisconsin","venueEventsUrl":"http://www.stubhub.com/barrymore-theatre-wisconsin-tickets","latitude":43.09312,"longitude":-89.352264,"timezone":"CST","address1":"2090 Atwood Ave.","city":"Madison","state":"WI","zipCode":"53704","country":"US","venueConfigId":171633},"ticketInfo":{"minPrice":0.0,"maxPrice":0.0,"totalTickets":0.0,"totalPostings":0,"totalListings":0,"currencyCode":"USD"},"bookOfBusinessId":1,"hideEventDate":"0","hideEventTime":0,"categories":[{"id":1,"name":"Concert tickets","url":"concert-tickets"}],"groupings":[{"id":63914,"name":"Artists T - Z","url":"artists-t-z"}],"performers":[{"id":608,"name":"They Might Be Giants Tickets","url":"they-might-be-giants-tickets"}],"geos":[{"id":0,"name":"By Geography"},{"id":196976,"name":"United States"},{"id":690,"name":"Wisconsin"},{"id":691,"name":"Milwaukee"},{"id":65682,"name":"Barrymore Theatre - Wisconsin"}],"attributes":[{"name":"act_primary","value":"They Might Be Giants"}]},{"id":9195519,"status":"Active","locale":"en_US","title":"They Might Be Giants Tickets","description":"They Might Be Giants Beachland Tavern and Ballroom Cleveland Tickets - Buy and sell They Might Be Giants Cleveland Tickets for April 21 at Beachland Tavern and Ballroom Cleveland in Cleveland, OH on StubHub!","eventInfoUrl":"http://www.stubhub.com/they-might-be-giants-cleveland-beachland-tavern-and-ballroom-cleveland-4-21-2015-9195519","dateLocal":"2015-04-21T20:00:00-0400","dateUTC":"2015-04-22T00:00:00+0000","venue":{"id":20966,"name":"Beachland Tavern and Ballroom Cleveland","venueInfoUrl":"http://www.stubhub.com/venue/beachland-tavern","venueEventsUrl":"http://www.stubhub.com/beachland-tavern-tickets","latitude":41.571247,"longitude":-81.57047,"timezone":"EST","address1":"15711 Waterloo RD","city":"Cleveland","state":"OH","zipCode":"44110","country":"US","venueConfigId":24292},"ticketInfo":{"minPrice":0.0,"maxPrice":0.0,"totalTickets":0.0,"totalPostings":0,"totalListings":0,"currencyCode":"USD"},"bookOfBusinessId":1,"hideEventDate":"0","hideEventTime":0,"categories":[{"id":1,"name":"Concert tickets","url":"concert-tickets"}],"groupings":[{"id":63914,"name":"Artists T - Z","url":"artists-t-z"}],"performers":[{"id":608,"name":"They Might Be Giants Tickets","url":"they-might-be-giants-tickets"}],"geos":[{"id":0,"name":"By Geography"},{"id":196976,"name":"United States"},{"id":686,"name":"Ohio"},{"id":3261,"name":"Cleveland"},{"id":20966,"name":"Beachland Tavern and Ballroom Cleveland"}],"attributes":[{"name":"act_primary","value":"They Might Be Giants"}]},{"id":9195523,"status":"Active","locale":"en_US","title":"They Might Be Giants Tickets","description":"They Might Be Giants Knitting Factory Boise Tickets - Buy and sell They Might Be Giants Boise Tickets for May 6 at Knitting Factory Boise in Boise, ID on StubHub!","eventInfoUrl":"http://www.stubhub.com/they-might-be-giants-boise-knitting-factory-boise-5-6-2015-9195523","dateLocal":"2015-05-06T20:00:00-0600","dateUTC":"2015-05-07T02:00:00+0000","venue":{"id":137507,"name":"Knitting Factory Boise","venueInfoUrl":"http://www.stubhub.com/venue/knitting-factory-boise","venueEventsUrl":"http://www.stubhub.com/knitting-factory-boise-tickets","latitude":43.613384,"longitude":-116.207344,"timezone":"MST","address1":"416 South 9th Street","address2":"Enter off of the alley Between 8th and 9th","city":"Boise","state":"ID","zipCode":"83702","country":"US","venueConfigId":1227579},"ticketInfo":{"minPrice":36.7,"maxPrice":57.75,"totalTickets":38.0,"totalPostings":7,"totalListings":7,"currencyCode":"USD"},"bookOfBusinessId":1,"hideEventDate":"0","hideEventTime":0,"categories":[{"id":1,"name":"Concert tickets","url":"concert-tickets"}],"groupings":[{"id":63914,"name":"Artists T - Z","url":"artists-t-z"}],"performers":[{"id":608,"name":"They Might Be Giants Tickets","url":"they-might-be-giants-tickets"}],"geos":[{"id":0,"name":"By Geography"},{"id":196976,"name":"United States"},{"id":714,"name":"Idaho"},{"id":4921,"name":"Boise"},{"id":137507,"name":"Knitting Factory Boise"}],"attributes":[{"name":"act_primary","value":"They Might Be Giants"}]},{"id":9195524,"status":"Active","locale":"en_US","title":"They Might Be Giants Tickets","description":"They Might Be Giants Fillmore San Francisco Tickets - Buy and sell They Might Be Giants San Francisco Tickets for May 9 at Fillmore San Francisco in San Francisco, CA on StubHub!","eventInfoUrl":"http://www.stubhub.com/they-might-be-giants-san-francisco-fillmore-san-francisco-5-9-2015-9195524","dateLocal":"2015-05-09T21:00:00-0700","dateUTC":"2015-05-10T04:00:00+0000","venue":{"id":92,"name":"Fillmore San Francisco","venueInfoUrl":"http://www.stubhub.com/venue/fillmore-san-francisco","venueEventsUrl":"http://www.stubhub.com/fillmore-san-francisco-event-tickets","latitude":37.78424,"longitude":-122.4333,"timezone":"PST","address1":"1805 Geary Blvd.","city":"San Francisco","state":"CA","zipCode":"94115","country":"US","venueConfigId":39898},"ticketInfo":{"minPrice":61.99,"maxPrice":106.0,"totalTickets":69.0,"totalPostings":17,"totalListings":17,"currencyCode":"USD"},"bookOfBusinessId":1,"hideEventDate":"0","hideEventTime":0,"categories":[{"id":1,"name":"Concert tickets","url":"concert-tickets"}],"groupings":[{"id":63914,"name":"Artists T - Z","url":"artists-t-z"}],"performers":[{"id":608,"name":"They Might Be Giants Tickets","url":"they-might-be-giants-tickets"}],"geos":[{"id":0,"name":"By Geography"},{"id":196976,"name":"United States"},{"id":4,"name":"California"},{"id":81,"name":"SF Bay Area"},{"id":92,"name":"Fillmore San Francisco"}],"attributes":[{"name":"act_primary","value":"They Might Be Giants"}]},{"id":9195517,"status":"Active","locale":"en_US","title":"They Might Be Giants Tickets","description":"They Might Be Giants Mr. Smalls Theatre Tickets - Buy and sell They Might Be Giants Millvale Tickets for April 16 at Mr. Smalls Theatre in Millvale, PA on StubHub!","eventInfoUrl":"http://www.stubhub.com/they-might-be-giants-millvale-mr--smalls-theatre-4-16-2015-9195517","dateLocal":"2015-04-16T21:00:00-0400","dateUTC":"2015-04-17T01:00:00+0000","venue":{"id":12705,"name":"Mr. Smalls Theatre","venueInfoUrl":"http://www.stubhub.com/venue/mr-smalls-theatre","venueEventsUrl":"http://www.stubhub.com/mr-smalls-theatre-event-tickets","latitude":40.48127,"longitude":-79.97268,"timezone":"EST","address1":"400 Lincoln Avenue","city":"Millvale","state":"PA","zipCode":"15209","country":"US","venueConfigId":14472},"ticketInfo":{"minPrice":0.0,"maxPrice":0.0,"totalTickets":0.0,"totalPostings":0,"totalListings":0,"currencyCode":"USD"},"bookOfBusinessId":1,"hideEventDate":"0","hideEventTime":0,"categories":[{"id":1,"name":"Concert tickets","url":"concert-tickets"}],"groupings":[{"id":63914,"name":"Artists T - Z","url":"artists-t-z"}],"performers":[{"id":608,"name":"They Might Be Giants Tickets","url":"they-might-be-giants-tickets"}],"geos":[{"id":0,"name":"By Geography"},{"id":196976,"name":"United States"},{"id":521,"name":"Pennsylvania"},{"id":681,"name":"Pittsburgh"},{"id":12705,"name":"Mr. Smalls Theatre"}],"attributes":[{"name":"act_primary","value":"They Might Be Giants"}]},{"id":9195521,"status":"Active","locale":"en_US","title":"They Might Be Giants Tickets","description":"They Might Be Giants Theatre of Living Arts Tickets - Buy and sell They Might Be Giants Philadelphia Tickets for April 25 at Theatre of Living Arts in Philadelphia, PA on StubHub!","eventInfoUrl":"http://www.stubhub.com/they-might-be-giants-philadelphia-theatre-of-living-arts-4-25-2015-9195521","dateLocal":"2015-04-25T21:15:00-0400","dateUTC":"2015-04-26T01:15:00+0000","venue":{"id":130103,"name":"Theatre of Living Arts","venueInfoUrl":"http://www.stubhub.com/venue/theatre-of-living-arts","venueEventsUrl":"http://www.stubhub.com/theatre-of-living-arts-tickets","latitude":39.941303,"longitude":-75.14868,"timezone":"EST","address1":"334 South St.","city":"Philadelphia","state":"PA","zipCode":"19147","country":"US","venueConfigId":512071},"ticketInfo":{"minPrice":0.0,"maxPrice":0.0,"totalTickets":0.0,"totalPostings":0,"totalListings":0,"currencyCode":"USD"},"bookOfBusinessId":1,"hideEventDate":"0","hideEventTime":0,"categories":[{"id":1,"name":"Concert tickets","url":"concert-tickets"}],"groupings":[{"id":63914,"name":"Artists T - Z","url":"artists-t-z"}],"performers":[{"id":608,"name":"They Might Be Giants Tickets","url":"they-might-be-giants-tickets"}],"geos":[{"id":0,"name":"By Geography"},{"id":196976,"name":"United States"},{"id":521,"name":"Pennsylvania"},{"id":522,"name":"Philadelphia"},{"id":130103,"name":"Theatre of Living Arts"}],"attributes":[{"name":"act_primary","value":"They Might Be Giants"}]}]}"""

class StubHubEvent(object):
	@classmethod
	def from_dict(cls, data):
		"""Turns a dict into either an event, creating other classes as needed.

		Args:
			data (dict): A dict created from json returned from a call to the StubHub api.
		"""
		instance = cls()
		for key, value in data.items():
			if type(value) is dict or type(value) is list:
				# dicts and lists should be other data types
				# TODO: This can probably be generalized a bit
				if key == 'venue':
					instance.__dict__[key] = StubHubVenue.from_dict(value)
				elif key == 'ticketInfo':
					instance.__dict__[key] = StubHubTicketInfo.from_dict(value)
				elif key == 'categories':
					instance.categories = []
					for category in value:
						instance.categories.append(StubHubCategory.from_dict(category))
				elif key == 'groupings':
					instance.groupings = []
					for grouping in value:
						instance.groupings.append(StubHubGrouping.from_dict(grouping))
				elif key == 'performers':
					instance.performers = []
					for performer in value:
						instance.performers.append(StubHubPerformer.from_dict(performer))
				elif key == 'geos':
					instance.geos = []
					for geo in value:
						instance.geos.append(StubHubGeo.from_dict(geo))
				elif key == 'attributes':
					instance.attributes = []
					for attribute in value:
						instance.attributes.append(StubHubEventAttribute.from_dict(attribute))

				else:
					# Catch anything I don't have a special case for.
					instance.__dict__[key] = value
			else:
				instance.__dict__[key] = value
		return instance


class StubHubEventSearchResponse(object):
	@classmethod
	def from_dict(cls, data):
		"""Turns a dict into either an event, creating other classes as needed.

		Args:
			data (dict): A dict created from json returned from a call to the StubHub api.
		"""
		instance = cls()
		for key, value in data.items():
			if type(value) is dict or type(value) is list:
				# dicts and lists should be other data types
				# TODO: This can probably be generalized a bit
				if key == 'events':
					instance.events = []
					for event in value:
						instance.events.append(StubHubEvent.from_dict(event))
				else:
					# Catch anything I don't have a special case for.
					instance.__dict__[key] = value
			else:
				instance.__dict__[key] = value
		return instance