from django.conf.urls import url, include
from days import urls as days_urls


urlpatterns = [
    url(r'', include(days_urls)),
]
