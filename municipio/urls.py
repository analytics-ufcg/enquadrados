from django.conf.urls import url, include
from municipio import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/summary$', views.cidades_summary, name='cidades-summary'),
    url(r'^$', views.cidades_list, name='cidades-list'),
]
