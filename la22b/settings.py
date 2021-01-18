import ast
import os
from pathlib import Path

import dj_database_url
import dotenv
from django.contrib.messages import constants as messages

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Application definition

INSTALLED_APPS = [
    'main.apps.MainConfig',            
    'results.apps.ResultsConfig',
    'student.apps.StudentConfig',
    'titles.apps.TitlesConfig',

    'django.contrib.admin',
    'django.contrib.postgres',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.humanize',

    'post_office',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'la22b.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'la22b.wsgi.application'
DUMMY_PRODUCTION = ast.literal_eval(os.environ.get('DUMMY_PRODUCTION', 'False'))

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

dotenv_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_file):
    SECRET_KEY = 'dmroa9$j*+tu^%begx5sie)s76)=*uru53=rix3e@+_or*f9u)'
    dotenv.load_dotenv(dotenv_file)
    PRODUCTION_SERVER = False
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]']
    DEBUG = True
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    DATABASES = {'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))}
    GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = BASE_DIR /'gdrive_config.json'

else:
    PRODUCTION_SERVER = True
    DEBUG = False
    ALLOWED_HOSTS =['*']
    GOOGLE_DRIVE_STORAGE_JSON_KEY_FILE = None
    DATABASES = {'default': dj_database_url.config(default=os.environ['DATABASE_URL'])}
    SECRET_KEY = os.environ['SECRET_KEY']

    MIDDLEWARE = [MIDDLEWARE[0]]+['whitenoise.middleware.WhiteNoiseMiddleware']+MIDDLEWARE[1:]
    INSTALLED_APPS=INSTALLED_APPS[0:-1]+['whitenoise.runserver_nostatic','gdstorage']+[INSTALLED_APPS[-1]]


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Calcutta'

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

MEDIA_URL = '/media/'

SESSION_COOKIE_AGE = 86400

#oververiding a message tag
MESSAGE_TAGS = {
    messages.ERROR : 'danger'
}

# # Deployment check
if PRODUCTION_SERVER:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_REFERRER_POLICY = "same-origin"


EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = os.environ['EMAIL_PORT']
EMAIL_USE_SSL = os.environ['EMAIL_USE_SSL']
EMAIL_BACKEND = 'post_office.EmailBackend'
DEFAULT_FROM_EMAIL  = os.environ['DEFAULT_FROM_EMAIL']

ADMINS = [('admin', EMAIL_HOST_USER),]

if DUMMY_PRODUCTION:
    INSTALLED_APPS=INSTALLED_APPS[0:-1]+['gdstorage',]+[INSTALLED_APPS[-1]]
else:
    MEDIA_ROOT = BASE_DIR / 'media'
    if not os.path.exists(MEDIA_ROOT): os.mkdir(MEDIA_ROOT)
