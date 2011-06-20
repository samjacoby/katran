# -*- coding: utf-8 -*-
import os
import logging
import logging.handlers

gettext = lambda s: s

PROJECT_DIR = os.path.abspath(os.path.dirname(__file__))


DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Set up logging
LOG_DIR = '%s/log/' % PROJECT_DIR
LOG_NAME = 'katran.log'
# Access time, filename/function#line-number message
log_formatter = logging.Formatter("[%(asctime)s %(filename)s/%(funcName)s#%(lineno)d] %(message)s")

ADMINS = (
     ('Sam Jacoby', 'sam@shackmanpress.com'),
)

MANAGERS = ADMINS

LANGUAGES = [('en', 'en')]
DEFAULT_LANGUAGE = 0

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(PROJECT_DIR, 'mycms.db'),
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'static')
MEDIA_URL = '/static/'

#STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
#STATIC_URL = '/static/'
# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '0r6%7gip5tmez*vygfv+u14h@4lbt^8e2^26o#5_f_#b7%cm)u'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.media.PlaceholderMediaMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'cms.context_processors.media',
)

CMS_TEMPLATES = (
    ('index.html', 'Base Index Template'),
#    ('entries/index.html', 'Entries Index Template'),
#    ('entries/book_detail.html', 'Book Detail Template'),
#    ('entries/typography_detail.html', 'Typography Detail Template'),

)

CMS_MENU_TITLE_OVERWRITE = True

CMS_PLACEHOLDER_CONF = {
        'list_display_content': {
            'plugins': ('TextPlugin', 'PicturePlugin'),
            'name': gettext('Index Display Entry')
            },
        'main_content': {
            'plugins': ('TextPlugin', 'PicturePlugin'),
            'name': gettext('Main Entry Content')
            },
        'sidebar_content': {
            'plugins': ('TextPlugin', 'PicturePlugin'),
            'name': gettext('Sidebar Content')
            },
        'secondary_content': {
            'plugins': ('TextPlugin', 'PicturePlugin'),
            'name': gettext('Secondary Entry Content')
            },
        }

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
    os.path.join(PROJECT_DIR, 'dashboard', 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'cms',
    'menus',
    'mptt',
    'appmedia',
    'south',
    'cms.plugins.text',
    'cms.plugins.picture',
    'cms.plugins.teaser',
    'cms.plugins.link',
    'cms.plugins.file',
    'cms.plugins.snippet',
    'cms.plugins.googlemap',
    'entries',
    'stamps',
    'entries.plugins',
    'sorl.thumbnail',
    'dashboard'
)

# Add log setup after local imports
LOG_FILE = os.path.join(LOG_DIR, LOG_NAME)
try:
    if not os.path.exists(os.path.dirname(LOG_FILE)):
        os.mkdir(os.path.dirname(LOG_FILE))
    try:
        handler = logging.handlers.TimedRotatingFileHandler(filename=LOG_FILE, when='midnight')
    except IOError:
        import sys
        handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(log_formatter)
    log = logging.getLogger('')
    if DEBUG:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.WARN)
    log.addHandler(handler)
except OSError:
    # Will occur during fab
    pass

