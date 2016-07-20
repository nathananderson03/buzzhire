from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.conf import settings
from django.core import validators
from django.core.urlresolvers import reverse


class Lead(models.Model):
    """A lead is an expression of interest created by a potential client.
    
    Note: this model was used for the prelaunch website to capture interest.
    It is not currently used in the new site and could possibly be
    decommissioned.
    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    more_information = models.TextField(
        help_text="If you like, tell us a little more about what "
            "you're looking for.",
        blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)


def _is_client(self):
    """Custom method on User model.
    Returns whether or not the user account is a client account,
    i.e. has a client profile.
    ."""
    return Client.objects.filter(user=self).exists()
User.is_client = property(_is_client)


def _client(self):
    """Custom method on User model.
    Returns the Client for the user.  If it doesn't, raises
    Client.DoesNotExist.
    """
    return self.client_set.get()
User.client = property(_client)


class Client(models.Model):
    """A client is a person who wishes to book a freelancer.
    """
    # A link to a user account
    user = models.ForeignKey(settings.AUTH_USER_MODEL, unique=True)

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    mobile = models.CharField(max_length=13, validators=[
            validators.RegexValidator(r'^07[0-9 ]*$',
                           'Please enter a valid UK mobile phone number in '
                           'the form 07xxx xxx xxx')])
    company_name = models.CharField(max_length=50, blank=True,
                                    help_text='The name of your company')
    @property
    def reference_number(self):
        "Returns a reference number for this client."
        return 'CL%s' % str(self.pk).zfill(7)

    def get_full_name(self):
        "Returns the full name of the client."
        return '%s %s' % (self.first_name,
                          self.last_name)

    def __unicode__(self):
        # Show the company name by default, falling back to their own name
        if self.company_name:
            return self.company_name
        else:
            return self.get_full_name()

    def get_absolute_url(self):
        return reverse('admin:client_client_change', args=(self.pk,))

    class Meta:
        ordering = 'last_name',
