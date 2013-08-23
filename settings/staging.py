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

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

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

#==============================================================================
# Amazon S3 Account Settings
#==============================================================================

# This setting sets the path to the S3 storage class
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# Your Amazon Web Services storage bucket name, as a string.
AWS_STORAGE_BUCKET_NAME = 'residentadvisor'

# Your Amazon Web Services access key, as a string.
# Set it by issuing following command
# <code>
# heroku config:add AWS_ACCESS_KEY_ID=''
# </code>
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']

# Your Amazon Web Services secret access key, as a string.
# Set it by issuing following command
# <code>
# heroku config:add AWS_SECRET_ACCESS_KEY=''
# </code>
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# Set Static URL
S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = S3_URL
