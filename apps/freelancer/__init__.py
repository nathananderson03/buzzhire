"""The freelancer app is responsible for handling things specific to freelancer
accounts, particularly any freelancer-specific profile information.

Most importantly it defines the Freelancer model, which is then extended into
more specific freelancer cases (e.g. Driver) by service apps.
"""

default_app_config = 'apps.freelancer.config.FreelancerConfig'