

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

class StubHubSectionSummary(StubHubModel):
    pass

class StubHubVenue(StubHubModel):
    # TODO: Fix properties to match stubhub names!
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


class StubHubSection(StubHubModel):
    pass




class StubHubEventSectionSearchResponse(StubHubModel):
    errors = None
    eventId = None  # docs say eventid, actual request is eventID, returns eventId...NICE!
    eventDescription = None
    section = None
    currencyCode = None
    isVenueScrubbed = None
    isViewFromSectionEnabled = None
    smallViewFromSectionUrl = None
    mediumViewFromSectionUrl = None
    largeViewFromSectionUrl = None



class StubHubEventSearchResponse(object):
    def __init__(self):
        self.numFound = None
        self.events = None

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

class StubHubInventoryListing(StubHubModel):
    def __init__(self):
        self.currentPrice = None
        self.deliveryFee = None
        self.deliveryTypeList = None
        self.dirtyTicketInd = None
        self.faceValue = None
        self.listingAttributeCategoryList = None
        self.listingAttributeList = None
        self.listingId = None
        self.quantity = None
        self.row = None  # comes as a unicode string, not an int
        self.score = None
        self.seatNumbers = None
        self.sectionId = None
        self.sectionName = None
        self.sellerOwnInd = None
        self.sellerSectionName = None
        self.serviceFee = None
        self.splitOption = None
        self.splitVector = None
        self.ticketClass = None
        self.ticketSplit = None
        self.totalCost = None
        self.zoneId = None
        self.zoneName = None

    def __unicode__(self):
        return "%s for %s" % (self.row, self.currentPrice)


class StubHubInventorySearchResponse(StubHubModel):
    def __init__(self):
        self.listing = None

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
                if key == 'listing':
                    instance.listing = []
                    for listing in value:
                        instance.listing.append(StubHubInventoryListing.from_dict(listing))
                else:
                    # Catch anything I don't have a special case for.
                    instance.__dict__[key] = value
            else:
                instance.__dict__[key] = value
        return instance