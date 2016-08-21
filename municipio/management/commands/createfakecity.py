#!/usr/bin/python
# -*- coding: UTF-8 -*-

from django.core.management.base import BaseCommand, CommandError
from municipio.models import *

from datetime import date
import random

def get_tipo():
    tipos = ['comissionado', 'eletivo', 'efetivo', 'terceirizado']
    t = random.choice(tipos)
    return TipoFuncionario.objects.get_or_create(nome=t)[0]

def get_cargo():
    cargo = ['Assessor', 'Assistente de gabinete', 'ASG', 'Secretaria de presidencia']
    return random.choice(cargo)

class Command(BaseCommand):
    help = 'Creates random data for a city'

    def add_arguments(self, parser):
        parser.add_argument('nome_cidade', nargs=1, type=str)
        parser.add_argument('numero_funcionarios', nargs=1, type=int)

    def handle(self, *args, **options):
        estado = Estado.objects.get_or_create(nome=u'Paraíba', sigla=u'PB')[0]
        cidade = Cidade.objects.get_or_create(nome=options['nome_cidade'][0], estado=estado)[0]
        orgao_tuple = OrgaoPublico.objects.get_or_create(nome='Câmara Municipal', cidade=cidade)
        orgao = orgao_tuple[0]
        if orgao_tuple[1]:
            place = Imovel.objects.get_or_create(orgao=orgao, area_m2=150.0)
        folha = FolhaDePagamento.objects.get_or_create(data=date(2016,1,1), orgao=orgao)[0]
        for p in xrange(int(options['numero_funcionarios'][0])):
            pessoa = Pessoa.objects.get_or_create(nome='P %d da Silva', cpf=str(random.randint(10000000000, 99999999999)))[0]
            func = Funcionario.objects.get_or_create(folha=folha, pessoa=pessoa, salario=0.0, cargo=get_cargo(),
                                                     tipo=get_tipo(), codigo=0)
