import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings.installations")
os.environ.setdefault("DJANGO_CONFIGURATION", "Local")

from configurations.wsgi import get_wsgi_application
application = get_wsgi_application()
