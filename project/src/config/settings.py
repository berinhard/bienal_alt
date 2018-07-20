from unipath import Path

from decouple import config

BASE_DIR = Path(__file__).ancestor(3)
SRC_DIR = BASE_DIR.child('src')


DEBUG = config('DEBUG', cast=bool)
SECRET_KEY = config('SECRET_KEY')

ALLOWED_HOSTS = ['bienal-alt.herokuapp.com']


INSTALLED_APPS = [
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'tinymce',
    'storages',
    'src.actions',
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


ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.child('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'src.actions.context_processors.list_questions',
            ],
        },
    },
]

STATICFILES_DIRS = [BASE_DIR.child("static")]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR.child('db.sqlite3'),
    }
}

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


LANGUAGE_CODE = 'pt-BR	'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'


# Admin config
SUIT_CONFIG = {
    'ADMIN_NAME': 'Bienal Alt',
}

# TinyMCE
#TINYMCE_JS_URL = 'https://cdnjs.cloudflare.com/ajax/libs/tinymce/4.7.13/jquery.tinymce.min.js'
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,paste,searchreplace,colorpicker,textcolor",
    'theme': "advanced",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    'height': 600,
    'width': 600,
    'toolbar': "forecolor backcolor"
}
TINYMCE_COMPRESSOR = True

import django_heroku
django_heroku.settings(locals())
