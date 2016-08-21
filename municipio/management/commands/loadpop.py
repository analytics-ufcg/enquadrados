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

class Command(BaseCommand):
    help = 'Carrega dados csv de pib'

    def add_arguments(self, parser):
        parser.add_argument('arquivo', nargs=1, type=str)
        parser.add_argument('ano', nargs=1, type=int)

    def handle(self, *args, **options):
        arquivo = options['arquivo'][0]
        ano = options['ano'][0]
        with open(arquivo, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            reader.next()
            for row in reader:
                try:
                    cidade = get_cidade(row[1], 'PB')
                except Cidade.DoesNotExist:
                    print 'Skipped cidade', cidade
                    continue
                pop = int(row[4].replace('.', ''))
                if not Populacao.objects.filter(cidade=cidade, ano=ano).exists():
                    Populacao.objects.get_or_create(cidade=cidade, ano=ano, numero=pop)
