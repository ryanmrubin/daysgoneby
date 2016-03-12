import os
from django.core.wsgi import get_wsgi_application
from dj_static import Cling
from whitenoise.django import DjangoWhiteNoise


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "daysgoneby.settings.dev")

application = Cling(get_wsgi_application())
application = DjangoWhiteNoise(application)
