from django.conf.urls import url, include
from municipio import views

urlpatterns = [
    url(r'^', views.cidades_list, name='cidades-list'),
]
