from django.shortcuts import render
from rest_framework import viewsets
from municipio.serializers import CidadeSerializer
from municipio.models import Cidade


class CidadeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows cidades to be viewed
    """
    queryset = Cidade.objects.all().order_by('estado__sigla', 'nome')
    serializer_class = CidadeSerializer
