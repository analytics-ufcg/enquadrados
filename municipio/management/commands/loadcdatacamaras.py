#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.core.management.base import BaseCommand, CommandError
from municipio.models import *

import csv

def get_estado(sigla):
    return Estado.objects.get(sigla=sigla)

def get_cidade(cidade, estado):
    est = get_estado(estado)
    return Cidade.objects.get_or_create(nome=cidade, estado=est)[0]

def get_orgao(cidade, nome):
    return OrgaoPublico.objects.get_or_create(cidade=cidade, nome=nome)[0]

def get_tipo_funcionario(nome):
    return TipoFuncionario.objects.get_or_create(nome=nome)[0]

def get_folha(orgao, ano, mes):
    return EstatisticaFolhaDePagamento.objects.get_or_create(orgao=orgao, ano=ano, mes=mes)[0]

def inc_quantidade(folha, tipo):
    q = QuantidadeTipoFuncionario.objects.get_or_create(folha=folha, tipo=tipo)[0]
    q.quantidade += 1
    q.save()

def create_cidades(cidades):
    for c in cidades:
        get_cidade(c, 'PB')

def create_funcs(funcs):
    for f in funcs:
        get_tipo_funcionario(f)

class Command(BaseCommand):
    help = 'Carrega dados csv da camara'

    def add_arguments(self, parser):
        parser.add_argument('arquivo', nargs=1, type=str)

    def add_data(self, row):
        pb = Estado.objects.get(sigla='PB')
        cidade = Cidade.objects.get(nome=row[1], estado=pb)
        orgao = get_orgao(cidade, row[2])
        tipofunc = TipoFuncionario.objects.get(nome=row[4])
        mes = int(row[7])
        ano = int(row[8])
        folha = get_folha(orgao, ano, mes)
        quantidade = inc_quantidade(folha, tipofunc)

    def handle(self, *args, **options):
        arquivo = options['arquivo'][0]
        with open(arquivo, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            reader.next()
            cidades = set([])
            tipo_funcs = set([])
            for row in reader:
                cidades.add(row[1])
                tipo_funcs.add(row[4])
            create_cidades(cidades)
            create_funcs(tipo_funcs)

        with open(arquivo, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            reader.next()

            i = 0
            for row in reader:
                i += 1
                print i
                self.add_data(row)
