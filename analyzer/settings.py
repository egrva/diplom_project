import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# SECURITY WARNING: Modify this secret key if using in production!
SECRET_KEY = "super_duper_secret_key"

DEFAULT_AUTO_FIELD='django.db.models.AutoField'

DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'NAME',
                'USER': 'USER',
                'PASSWORD': 'PASSWORD',
                'HOST': 'HOST',
                'PORT': 'PORT',
            }
        }
# CHANGE THE SECRET KEY IN YOUR CODE
INSTALLED_APPS = ("db",)