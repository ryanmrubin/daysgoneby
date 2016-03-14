from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.calculate_days_gone),
    url(r'^N-400/$', views.n400_home, name='n400_home'),
    url(r'^N-400/dates/$', views.n400_date_entry, name='n400_date_entry'),
]
