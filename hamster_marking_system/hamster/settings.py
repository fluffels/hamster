"""
Django settings for hamster project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(a2#03%*j5l10&ik9%&&xsdaijn%0n!e*ky-fj7nfve%ww2fj!'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

#LDAP Settings

AUTH_LDAP_ALWAYS_UPDATE_USER = True #Change to false if login is slow

#Enables user informtion to be updated in database evertime user authenticates
AUTH_LDAP_MIRROR_GROUPS = True
#An alternative would be :
#AUTH_LDAP_FIND_GROUP_PERMS = True
#which requires ModelBackend to be installed, check https://pythonhosted.org/django-auth-ldap/permissions.html


AUTH_LDAP_BIND_DN = "ou=Computer Science,o=University of Pretoria,c=ZA"
AUTH_LDAP_BIND_PASSWORD = ""
AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=Computer Science,o=University of Pretoria,c=ZA",ldap.SCOPE_SUBTREE, "(uid=%(user)s")

# Set up the basic group parameters.
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=Groups,ou=Computer Science,o=University of Pretoria,c=ZA",
    ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)"
)
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType(name_attr="cn")

AUTH_LDAP_REQUIRE_GROUP = ["ou=Staff,ou=Computer Science,o=University of Pretoria,c=ZA", "ou=Students,ou=Computer Science,o=University of Pretoria,c=ZA"]

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail"
}

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": "ou=Students,ou=Computer Science,o=University of Pretoria,c=ZA",
    "is_staff": "ou=Staff,ou=Computer Science,o=University of Pretoria,c=ZA",
    "is_superuser": "ou=Admin,ou=Computer Science,o=University of Pretoria,c=ZA"
}

#AUTH_LDAP_PROFILE_FLAGS_BY_GROUP = {
#    "is_awesome": ["cn=awesome,ou=groups,dc=example,dc=com"]
#}



# Cache group memberships for an hour to minimize LDAP traffic
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600

AUTH_LDAP_SERVER_URI = "ldap://192.168.56.102:389/"

#End LDAP Settings

ALLOWED_HOSTS = ['http://hxvm1.cs.up.ac.za/']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'business_logic',
    'web_interface',
    'ldap_interface',
    'polymorphic',
    'mptt',
    'south',
    'numpy',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'hamster.urls'

WSGI_APPLICATION = 'hamster.wsgi.application'

# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = (
    'django_auth_ldap.backend.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hamster',
        'USER': 'postgres',
        'PASSWORD': 'bububu',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Johannesburg'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_FORMAT = '%Y-%m-%d'

DATETIME_INPUT_FORMATS = '%Y-%m-%d %H:%M:%S'

TIME_INPUT_FORMATS = '%H:%M:%S'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
