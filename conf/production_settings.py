import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'dev.db'
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(__file__),'media')
ADMIN_MEDIA_PREFIX = '/admin-media/'


CACHE_BACKEND = "dummy:///"
