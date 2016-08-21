from django.conf.urls import url, include
from municipio import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/summary$', views.cidade_summary, name='cidade-summary'),
    url(r'^$', views.cidades_list, name='cidades-list'),
    url(r'^summary$', views.cidades_summary, name='cidades-summary'),

    url(r'^ranking/funcionario/absoluto/$', views.cidades_ranking_tipo_funcionario_absoluto, name='cidades-ranking-absoluto'),
    url(r'^ranking/funcionario/percentual/$', views.cidades_ranking_tipo_funcionario_percentual, name='cidades-ranking-percentual'),
    url(r'^ranking/funcionario/area/$', views.cidades_ranking_area, name='cidades-ranking-area'),
]
