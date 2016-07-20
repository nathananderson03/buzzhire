"""The main app is used for general site-wide logic that requires a knowledge
of any of the other apps.  Among other things, it defines the home page.

It is at the other end of INSTALLED_APPS to the core app, so it can import any
other app, but no other app should import from it.
"""
