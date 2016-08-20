from municipio.models import *
from rest_framework import serializers

class CidadeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cidade
        fields = ('nome', 'estado')
