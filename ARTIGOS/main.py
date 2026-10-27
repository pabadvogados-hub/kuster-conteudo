"""
Artigo de blog / JusBrasil a partir das noticias da semana.

    python ARTIGOS/main.py noticias            so mostra o que apareceu nos ultimos 7 dias
    python ARTIGOS/main.py novo                escolhe a melhor noticia e escreve o artigo
    python ARTIGOS/main.py novo --dias 14
    python ARTIGOS/main.py novo --tema "hora de espera no patio"    ignora as noticias
    python ARTIGOS/main.py historico           o que ja foi escrito

O artigo sai em SAIDA/artigos/AAAA-MM-DD-titulo.md, para revisao e publicacao manual.
Nada e publicado automaticamente.
"""
import os
import re
import sys
import json
import argparse
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'NUCLEO'))
import ambiente  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from buscar_noticias import buscar_noticias_caminhoneiro  # noqa: E402
from gerar_artigo import gerar_artigo, escolher_melhor_noticia  # noqa: E402

HISTORICO = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'historico.json')


def _ler_historico():
    try:
        with open(HISTORICO, encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def _gravar_historico(artigo):
    hist = _ler_historico()
    hist.append({
        'titulo': artigo['titulo'],
        'palavra_chave': artigo['palavra_chave_principal'],
        'data': datetime.now().strftime('%d/%m/%Y'),
        'noticia': artigo.get('_noticia', {}).get('titulo', ''),
    })
    with open(HISTORICO, 'w', encoding='utf-8') as f:
        json.dump(hist, f, ensure_ascii=False, indent=2)


def _nome_arquivo(titulo):
    base = re.sub(r'[^a-z0-9]+', '-', titulo.lower()).strip('-')[:60]
    return f"{datetime.now():%Y-%m-%d}-{base}"


def _salvar(artigo):
    pasta = ambiente.pasta_saida('artigos')
    nome = _nome_arquivo(artigo['titulo'])
    caminho = os.path.join(pasta, f'{nome}.md')

    conferir = '\n'.join(f'- [ ] {c}' for c in artigo.get('conferir_antes_de_publicar', []))
    origem = artigo.get('_noticia', {})
    cabecalho = (
        f"<!--\nRASCUNHO PARA REVISAO - nao publicar sem conferir os pontos abaixo.\n\n"
        f"Palavra-chave: {artigo['palavra_chave_principal']}\n"
        f"Secundarias: {', '.join(artigo.get('palavras_chave_secundarias', []))}\n"
        f"Meta description: {artigo['meta_description']}\n"
        f"Gancho: {origem.get('titulo', '(tema livre)')} ({origem.get('fonte', '')} "
        f"{origem.get('data', '')})\n"
        f"{origem.get('link', '')}\n\n"
        f"CONFERIR ANTES DE PUBLICAR:\n{conferir}\n-->\n\n"
    )
    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(cabecalho + artigo['corpo_markdown'].strip() + '\n')
    return caminho


def main():
    p = argparse.ArgumentParser(description='Artigos do escritorio')
    sub = p.add_subparsers(dest='comando', required=True)

    n = sub.add_parser('noticias', help='so lista as noticias da janela')
    n.add_argument('--dias', type=int, default=7)

    a = sub.add_parser('novo', help='escreve um artigo')
    a.add_argument('--dias', type=int, default=7)
    a.add_argument('--tema', help='escreve sobre este tema, sem olhar as noticias')

    sub.add_parser('historico', help='artigos ja escritos')

    args = p.parse_args()

    if args.comando == 'historico':
        hist = _ler_historico()
        if not hist:
            print('Nenhum artigo escrito ainda.')
            return
        for h in hist:
            print(f"{h['data']}  {h['titulo']}\n          palavra-chave: {h['palavra_chave']}")
        return

    if args.comando == 'noticias':
        for i, x in enumerate(buscar_noticias_caminhoneiro(dias=args.dias), 1):
            print(f"{i:2}. [{x['fonte']}] {x['titulo']}  ({x['data']})")
        return

    if args.tema:
        noticia = {'titulo': args.tema, 'fonte': 'tema definido pelo escritorio',
                   'data': datetime.now().strftime('%d/%m/%Y'), 'descricao': '', 'link': ''}
    else:
        print('Buscando noticias...')
        noticias = buscar_noticias_caminhoneiro(dias=args.dias)
        if not noticias:
            print('Nenhuma noticia na janela. Use --dias 14 ou --tema "assunto".')
            return
        noticia = escolher_melhor_noticia(noticias, _ler_historico())
        print(f"\nPauta escolhida: {noticia['titulo']}")
        if noticia.get('_escolhida_porque'):
            print(f"Porque: {noticia['_escolhida_porque']}")

    print('\nEscrevendo o artigo...')
    artigo = gerar_artigo(noticia)
    caminho = _salvar(artigo)
    _gravar_historico(artigo)

    print(f"\nTitulo: {artigo['titulo']}")
    print(f"Resumo: {artigo['resumo']}")
    print('\nConferir antes de publicar:')
    for c in artigo.get('conferir_antes_de_publicar', []):
        print(f'  - {c}')
    print(f'\nRascunho salvo em:\n  {caminho}')


if __name__ == '__main__':
    main()
