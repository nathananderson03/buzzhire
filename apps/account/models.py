from django.contrib.auth.models import User


SITE_ADMIN_GROUP_NAME = 'site admin'


# Add the is_admin property to User instances
def _is_admin(self):
    "Whether to treat the user as a site admin."
    return self.is_superuser or self.groups.filter(name=SITE_ADMIN_GROUP_NAME).exists()
User.is_admin = property(_is_admin)
