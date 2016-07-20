from django.conf import settings
from django.contrib.gis import geos
from .postcodes import PostCodeClient


class GeoLocationMatchException(Exception):
    """Exception for raising when there's an issue matching a location
    from user input."""
    pass


class GeoLocation(object):
    """A location on the planet.  Initialised using a user-submitted
    postcode string,
    which it will attempt to process.  Raises a GeoLocationMatchException
    on failure.
    
    Once instantiated, will have two attributes:
    
        postcode: the human readable string of the matched postcode
        point: a GEOSGeometry object of the location
    """

    def __init__(self, postcode_string):

        client = PostCodeClient()
        response = client.getLookupPostCode(postcode_string)
        if response.get('status') == 200:
            # Build useful attributes on the object
            # Get the postcode, correctly formatted
            self.postcode = response['result']['postcode']
            # Get the point field from the longitude and latitude
            self.point = geos.fromstr("POINT(%s %s)" % (
                                            response['result']['longitude'],
                                            response['result']['latitude']))
        else:
            # Postcode not found
            raise GeoLocationMatchException

    def __repr__(self):
        return "<GeoLocation: %s>" % self.postcode
