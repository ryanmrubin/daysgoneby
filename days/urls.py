from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.calculate_days_gone),
    url(r'(?i)^N-400$', views.N400View.as_view()),
]
