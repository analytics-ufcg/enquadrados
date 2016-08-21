#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.core.management.base import BaseCommand, CommandError
from municipio.models import *

import csv
from datetime import datetime

def get_estado(sigla):
    return Estado.objects.get(sigla=sigla)

def get_cidade(cidade, estado):
    est = get_estado(estado)
    return Cidade.objects.get(nome=cidade, estado=est)

def get_orgao(cidade, nome='Câmara Municipal'):
    return OrgaoPublico.objects.get(cidade=cidade, nome=nome)

class Command(BaseCommand):
    help = 'Carrega dados csv de areas'

    def add_arguments(self, parser):
        parser.add_argument('arquivo', nargs=1, type=str)

    def handle(self, *args, **options):
        arquivo = options['arquivo'][0]
        with open(arquivo, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            reader.next()
            for row in reader:
                try:
                    print ' '.join(row[0].split()[1:])
                    cidade = get_cidade(' '.join(row[0].split()[1:]), 'PB')
                except Cidade.DoesNotExist:
                    print 'Skipped cidade', cidade
                    continue
                try:
                    orgao = get_orgao(cidade)
                except OrgaoPublico.DoesNotExist:
                    print 'Skipped orgao', cidade
                    continue
                area = float(row[2])
                Imovel.objects.get_or_create(orgao=orgao, area_m2=area, data=datetime(2016,8,1))
