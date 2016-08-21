#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import unicode_literals
from django.db import models

def get_last_ano_mes():
    e = EstatisticaFolhaDePagamento.objects.order_by('-ano', '-mes')
    if len(e):
        return e[0].ano, e[0].mes
    return None, None

class Estado(models.Model):
    ESTADOS_BRASIL = (('PB', u'Paraíba'),)

    nome = models.CharField(max_length=16)
    sigla = models.CharField(max_length=2, choices=ESTADOS_BRASIL, unique=True)

    def __str__(self):
        return self.sigla

class Cidade(models.Model):
    estado = models.ForeignKey(Estado)
    nome = models.CharField(max_length=64)

    def get_dados_basicos(self):
        return {'nome': self.nome, 'estado': self.estado.sigla, 'id': self.id}

    def get_summary(self):
        return self.get_dados_basicos()

    def get_folha_todos_os_orgaos(self, ano, mes):
        data = self.get_dados_basicos()
        data['mes'] = mes
        data['ano'] = ano
        data_orgaos = []
        for org in self.orgaopublico_set.all():
            try:
                folha = EstatisticaFolhaDePagamento.objects.get(orgao=org, ano=ano, mes=mes)
                data_orgaos.append({'orgao': org.nome,
                                    'quantidades': folha.get_funcionarios_count()})
            except EstatisticaFolhaDePagamento.DoesNotExist:
                pass
        data['orgaos'] = data_orgaos
        return data

class OrgaoPublico(models.Model):
    cidade = models.ForeignKey(Cidade)
    nome = models.CharField(max_length=128)

    def get_summary(self):
        summary = {'id': self.id}
        summary['cidade'] = self.cidade.get_summary()
        summary['nome'] = self.nome
        return summary

    def get_area(self):
        #TODO considerar a data da construcao
        return sum([x.area_m2 for x in Imovel.objects.filter(orgao=self).all()])

class EstatisticaFolhaDePagamento(models.Model):
    orgao = models.ForeignKey(OrgaoPublico)
    mes = models.IntegerField()
    ano = models.IntegerField()

    def get_funcionarios_count(self):
        return {f.tipo.nome: f.quantidade for f in QuantidadeTipoFuncionario.objects.filter(folha=self).all()}

    def get_funcionarios_total(self):
        return sum([f.quantidade for f in QuantidadeTipoFuncionario.objects.filter(folha=self).all()])
    def get_funcionarios_tipo(self, nome):
        try:
            return QuantidadeTipoFuncionario.objects.get(folha=self, tipo__nome=nome).quantidade
        except QuantidadeTipoFuncionario.DoesNotExist:
            return 0

    def get_summary(self):
        summary = self.orgao.get_summary()
        quantidade_funcionarios = {}
        for f in QuantidadeTipoFuncionario.objects.filter(folha=self).all():
            quantidade_funcionarios[f.tipo.nome] = f.quantidade
        summary['quantidade_funcionarios'] = quantidade_funcionarios
        return summary


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
