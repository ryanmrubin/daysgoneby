from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.calculate_days_gone),
    url(r'^multiple$', views.multiple_trips),
]
