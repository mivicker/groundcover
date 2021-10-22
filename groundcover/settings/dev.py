from .base import *
from dotenv import load_dotenv

load_dotenv()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
