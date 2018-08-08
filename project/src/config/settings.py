from unipath import Path

from decouple import config

BASE_DIR = Path(__file__).ancestor(3)
SRC_DIR = BASE_DIR.child('src')


DEBUG = config('DEBUG', cast=bool)
SECRET_KEY = config('SECRET_KEY')
PRODUCTION = config('PRODUCTION', default=False)

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
    'sorl.thumbnail',
    'src.actions',
    'src.mce_filebrowser',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR.child("static")]
STATICFILES_STORAGE = config('STATICFILES_STORAGE', default='whitenoise.django.GzipManifestStaticFilesStorage')
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.child('media')
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 10  # 10 MB


if PRODUCTION:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_HOST = config('AWS_S3_HOST')
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME')
    AWS_S3_SIGNATURE_VERSION = 's3v4'

    S3_URL = '{}.s3.amazonaws.com/'.format(AWS_STORAGE_BUCKET_NAME)
    MEDIA_URL = S3_URL

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


# Admin config
SUIT_CONFIG = {
    'ADMIN_NAME': '(OUTRA) 33ª Bienal de São Paulo',
}

# TinyMCE
TINYMCE_JS_URL = STATIC_URL + 'js/tiny_mce/tiny_mce.js'
TINYMCE_JS_ROOT = STATICFILES_DIRS[0].child('js', 'tiny_mce')
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,paste,searchreplace",
    'theme': "advanced",
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    'height': 600,
    'width': 600,
    "theme_advanced_buttons1": "fontsizeselect,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,styleselect,formatselect",
    'theme_advanced_buttons2': "bullist,numlist,|,outdent,indent,|,undo,redo,|,link,unlink,anchor,image,cleanup,help,code",
    'theme_advanced_buttons3': "hr,removeformat,visualaid,|,sub,sup,|,charmap",
}
TINYMCE_COMPRESSOR = True

import django_heroku
django_heroku.settings(locals())
