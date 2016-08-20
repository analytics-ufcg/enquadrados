#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import unicode_literals
from django.db import models

class Estado(models.Model):
    ESTADOS_BRASIL = (('PB', u'Paraíba'),)

    nome = models.CharField(max_length=16)
    sigla = models.CharField(max_length=2, choices=ESTADOS_BRASIL, unique=True)

class Cidade(models.Model):
    estado = models.ForeignKey(Estado)
    nome = models.CharField(max_length=64)

class Pessoa(models.Model):
    nome = models.CharField(max_length=128)
    cpf = models.CharField(max_length=15, unique=True)

class OrgaoPublico(models.Model):
    cidade = models.ForeignKey(Cidade)

class FolhaDePagamento(models.Model):
    orgao = models.ForeignKey(OrgaoPublico)
    data = models.DateField()

class TipoFuncionario(models.Model):
    nome = models.CharField(max_length=128, unique=True)

class Funcionario(models.Model):
    folha = models.ForeignKey(FolhaDePagamento)
    pessoa = models.ForeignKey(Pessoa)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    cargo = models.CharField(max_length=128)
    tipo = models.ForeignKey(TipoFuncionario)
    codigo = models.CharField(max_length=64)
    
class Imovel(models.Model):
    orgao = models.ForeignKey(OrgaoPublico)
    area_m2 = models.DecimalField(max_digits=16, decimal_places=3)
