from __future__ import absolute_import, unicode_literals

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c8e1@q_i!mn+ts%an19l-ld2jo6on=7(y=4^6hfusq=dw7*6!e'

GOOGLE_ANALYTICS_ID = 'UA-XXXXX-X'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
