import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = False

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'days',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'daysgoneby.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'daysgoneby.wsgi.application'

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
