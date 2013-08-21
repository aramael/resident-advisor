import dj_database_url
import os
from settings.common import *

#==============================================================================
# Generic Django Project Settings
#==============================================================================

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': dj_database_url.config()
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.herokuapp.com']

# Make this unique, and don't share it with anybody.
# Set it by issuing following command
# <code>
# heroku config:add SECRET_KEY=''
# </code>
SECRET_KEY = os.environ['SECRET_KEY']

#==============================================================================
# Twilio Account Settings
#==============================================================================

# Make this unique, and don't share it with anybody.
# Set it by issuing following command
# <code>
# heroku config:add TWILIO_ACCOUNT=''
# </code>
TWILIO_ACCOUNT = os.environ['TWILIO_ACCOUNT']


# Make this unique, and don't share it with anybody.
# Set it by issuing following command
# <code>
# heroku config:add TWILIO_TOKEN=''
# </code>
TWILIO_TOKEN = os.environ['TWILIO_TOKEN']