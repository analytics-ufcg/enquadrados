#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import unicode_literals
from django.db import models

class Estado(models.Model):
    ESTADOS_BRASIL = (('PB', u'Paraíba'),)

    nome = models.CharField(max_length=16)
    sigla = models.CharField(max_length=2, choices=ESTADOS_BRASIL, unique=True)

    def __str__(self):
        return self.sigla

class Cidade(models.Model):
    estado = models.ForeignKey(Estado)
    nome = models.CharField(max_length=64)

class OrgaoPublico(models.Model):
    cidade = models.ForeignKey(Cidade)
    nome = models.CharField(max_length=128)

class EstatisticaFolhaDePagamento(models.Model):
    orgao = models.ForeignKey(OrgaoPublico)
    mes = models.IntegerField()
    ano = models.IntegerField()

    def get_funcionarios_count(self):
        return {f.tipo.nome: f.quantidade for f in QuantidadeTipoFuncionario.objects.filter(folha=self).all()}

class TipoFuncionario(models.Model):
    nome = models.CharField(max_length=128, unique=True)

class QuantidadeTipoFuncionario(models.Model):
    tipo = models.ForeignKey(TipoFuncionario)
    folha = models.ForeignKey(EstatisticaFolhaDePagamento)
    quantidade = models.IntegerField(default=0)

class Imovel(models.Model):
    orgao = models.ForeignKey(OrgaoPublico)
    area_m2 = models.DecimalField(max_digits=16, decimal_places=3)
    data = models.DateTimeField()
