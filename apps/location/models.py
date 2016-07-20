from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from .utils import GeoLocation, GeoLocationMatchException


class Postcode(models.Model):
    """A postcode is a model that represents a particular postcode,
    with a geographical point."""

    # The postcode, without spaces - easier to use as a key
    compressed_postcode = models.CharField(max_length=8, db_index=True)
    # Human-friendly version of the postcode
    postcode = models.CharField(max_length=8, blank=True)
    point = models.PointField()

    objects = models.GeoManager()

    @property
    def latitude(self):
        return self.point.y

    @property
    def longitude(self):
        return self.point.x

    def save(self, *args, **kwargs):
        # Set the point based on the postcode
        if not self.point:
            try:
                geolocation = GeoLocation(self.compressed_postcode)
            except GeoLocationMatchException as e:
                # This is most likely to happen if the quota is exceeded
                raise ValidationError(
                    "Sorry, there was a problem matching that location. "
                    "Please try saving the location again, or adjusting "
                    "the postcode.")
            else:
                self.point = geolocation.point
                self.postcode = geolocation.postcode

        # Ensure we validate the model before saving
        self.full_clean()
        return super(Postcode, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.postcode

    class Meta:
         ordering = ['postcode']
