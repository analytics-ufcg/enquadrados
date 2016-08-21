from django.shortcuts import render
from django.http import JsonResponse, Http404
from django.db.models import Count, Sum, F, FloatField
from django.shortcuts import get_object_or_404
from municipio.models import *

def parse_ano_mes(request):
    mes, ano = request.GET.get('mes', None), request.GET.get('ano', None)
    if not mes or not ano:
        ano, mes = get_last_ano_mes()
    if not mes or not ano:
        raise Http404
    return ano, mes

def cidades_list(request):
    data = [c.get_dados_basicos() for c in Cidade.objects.all()]
    return JsonResponse(data, safe=False)

def cidades_summary(request):
    cidades = {}
    ano, mes = parse_ano_mes(request)
    for c in Cidade.objects.all():
        cidades[c.id] = c.get_folha_todos_os_orgaos(ano, mes)
    return JsonResponse({'cidades' : cidades})

def cidade_summary(request, pk):
    cidade = get_object_or_404(Cidade, id=pk)
    ano, mes = parse_ano_mes(request)
    data = cidade.get_folha_todos_os_orgaos(ano, mes)
    data['populacao'] = cidade.get_populacao(ano)
    for orgdata in data['orgaos']:
        org = OrgaoPublico.objects.get(id=orgdata['orgao_id'])
        orgdata['area'] = org.get_area()
    return JsonResponse(data)

def orgao_historico(request, pk):
    orgao = get_object_or_404(OrgaoPublico, id=pk)
    folhas = EstatisticaFolhaDePagamento.objects.filter(orgao=orgao).order_by('ano', 'mes')
    
    data = []
    for f in folhas:
        fdata = {}
        fdata['mes'] = f.mes
        fdata['ano'] = f.ano
        summary = f.get_summary()
        total = sum(summary['quantidade_funcionarios'].values())
        fdata.update(summary)
        fdata['total_funcionarios'] = total
        data.append(fdata)
    return JsonResponse({'historico' : data})

def cidades_ranking_tipo_funcionario_absoluto(request):
    ano, mes = parse_ano_mes(request)
    nome_tipo = request.GET.get('nome_tipo', None)
    rev = request.GET.get('reverse', None)
    if rev is None:
        rev = True
    elif len(rev) and rev == '1':
        rev = False

    if nome_tipo:
        quantidades = QuantidadeTipoFuncionario.objects.filter(folha__ano=ano,
                      folha__mes=mes, tipo__nome=nome_tipo).distinct().order_by(
                      ('-quantidade' if rev else 'quantidade'))[:10]
        return JsonResponse({'folhas': [q.folha.get_summary() for q in quantidades]})
    else:
        folhas = EstatisticaFolhaDePagamento.objects.filter(ano=ano, mes=mes).annotate(quantidade=(Sum('quantidadetipofuncionario__quantidade'))).order_by('-quantidade' if rev else 'quantidade')[:10]
        return JsonResponse({'folhas': [f.get_summary() for f in folhas]})
    
def cidades_ranking_tipo_funcionario_percentual(request):
    ano, mes = parse_ano_mes(request)
    nome_tipo = request.GET.get('nome_tipo', None)
    if not nome_tipo:
        raise Http404
    rev = request.GET.get('reverse', None)
    if rev is None:
        rev = True
    elif len(rev) and rev == '1':
        rev = False
    else:
        rev = True

    folhas = EstatisticaFolhaDePagamento.objects.filter(ano=ano, mes=mes)
    folhas = [{'folha': f, 'quantidade': f.get_funcionarios_total(),
               'quantidade_tipo': f.get_funcionarios_tipo(nome_tipo)} for f in folhas]
    folhas = [f for f in folhas if f['quantidade'] != 0]
    folhas = sorted(folhas, key=lambda x: float(x['quantidade_tipo'])/x['quantidade'], reverse=rev)
    return JsonResponse({'folhas': [q['folha'].get_summary() for q in folhas[:10]]})
    
def cidades_ranking_area(request):
    ano, mes = parse_ano_mes(request)
    rev = request.GET.get('reverse', None)
    if rev is None:
        rev = True
    elif len(rev) and rev == '1':
        rev = False
    else:
        rev = True

    folhas = EstatisticaFolhaDePagamento.objects.filter(ano=ano, mes=mes)
    folhas = [{'folha': f, 'quantidade': f.get_funcionarios_total(),
               'area': f.orgao.get_area()} for f in folhas]
    folhas = [f for f in folhas if f['quantidade'] != 0 and f['area'] != 0]
    folhas = sorted(folhas, key=lambda x: float(x['quantidade'])/float(x['area']), reverse=rev)
    return JsonResponse({'folhas': [q['folha'].get_summary() for q in folhas[:10]]})
    
def cidades_ranking_populacao(request):
    ano, mes = parse_ano_mes(request)
    rev = request.GET.get('reverse', None)
    if rev is None:
        rev = True
    elif len(rev) and rev == '1':
        rev = False
    else:
        rev = True
    pop_min = int(request.GET.get('pop_min', 0))

    folhas = EstatisticaFolhaDePagamento.objects.filter(ano=ano, mes=mes)
    folhas = [{'folha': f, 'quantidade': f.get_funcionarios_total(),
               'populacao': f.orgao.cidade.get_populacao(ano)} for f in folhas]
    folhas = [f for f in folhas if f['quantidade'] != 0 and f['populacao'] != None and f['populacao'] > pop_min]
    folhas = sorted(folhas, key=lambda x: float(x['quantidade'])/float(x['populacao']), reverse=rev)
    return JsonResponse({'folhas': [q['folha'].get_summary_com_populacao() for q in folhas[:10]]})
    
