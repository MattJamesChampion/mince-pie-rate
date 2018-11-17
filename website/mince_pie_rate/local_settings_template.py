import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = ''

SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': '',
        'NAME': '',
    }
}

LANGUAGE_CODE = ''

TIME_ZONE = ''

STATIC_ROOT = ''

EMAIL_BACKEND = ''

DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'
AZURE_ACCOUNT_NAME = ""
AZURE_ACCOUNT_KEY = ""
AZURE_CONTAINER = "images"
MEDIA_URL = "https://mincepieratedev.blob.core.windows.net/images/"