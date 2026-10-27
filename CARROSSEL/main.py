"""
Carrossel de Instagram (7 telas) sobre um tema, na voz do escritorio.

    python CARROSSEL/main.py "hora de espera no patio"
    python CARROSSEL/main.py "desconto indevido no salario" --telas 5

Sai o TEXTO de cada tela, pronto para jogar no template do Canva, mais a legenda do post.
A arte nao e gerada aqui: o texto e que da trabalho, o template e sempre o mesmo.
"""
import os
import sys
import json
import argparse
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'NUCLEO'))
import ambiente  # noqa: E402
import ia  # noqa: E402
from config.marca import ESCRITORIO, PUBLICO, TOM, REGRAS_OAB, CONTEXTO_JURIDICO, CTA_PERMITIDOS  # noqa: E402

MODELO = os.getenv('MODELO_CARROSSEL', 'claude-sonnet-5')

SISTEMA = f"""Voce escreve carrossel de Instagram para o {ESCRITORIO['nome_curto']}
({ESCRITORIO['cidade']}), escritorio trabalhista que atua pelo motorista profissional.

PUBLICO: {PUBLICO['quem']}. Rotina: {PUBLICO['rotina']}. Dor: {PUBLICO['dor']}.
LINGUAGEM: {PUBLICO['nivel']}
TOM: {TOM['como_fala']} Nunca: {TOM['nunca']}.

{REGRAS_OAB}
{CONTEXTO_JURIDICO}

COMO ESCREVER CADA TELA
- Titulo: no maximo 5 palavras, em caixa alta, com UMA palavra de destaque marcada entre
  asteriscos (ex.: "espera NAO e *descanso*"). O design pinta a palavra marcada.
- Texto: no maximo 2 frases curtas. Quem le esta no celular, de pe, no patio.
- Tela 1 e o gancho: uma afirmacao que incomoda. Nunca "voce sabia que".
- A tela do meio tem a virada: o que quase ninguem sabe.
- A ultima tela e o convite, dentro do Provimento 205/2021. Use algo no nivel de:
  {' | '.join(CTA_PERMITIDOS)}
- Nunca inventar lei, artigo, sumula ou decisao. O que precisar de conferencia vira [CONFERIR].
- Sem emoji, sem hashtag no texto das telas (hashtag so na legenda, no maximo 5).
"""

SCHEMA = {
    'type': 'object',
    'properties': {
        'tema': {'type': 'string'},
        'telas': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'numero': {'type': 'integer'},
                    'papel': {'type': 'string', 'description': 'gancho, problema, virada, exemplo, prova, convite'},
                    'titulo': {'type': 'string'},
                    'texto': {'type': 'string'},
                },
                'required': ['numero', 'papel', 'titulo', 'texto'],
                'additionalProperties': False,
            },
        },
        'legenda': {'type': 'string'},
        'hashtags': {'type': 'array', 'items': {'type': 'string'}},
        'conferir': {'type': 'array', 'items': {'type': 'string'}},
    },
    'required': ['tema', 'telas', 'legenda', 'hashtags', 'conferir'],
    'additionalProperties': False,
}


def gerar(tema, telas):
    pedido = (f'Tema: {tema}\n\nEscreva um carrossel de {telas} telas, numeradas de 1 a {telas}. '
              f'A tela 1 e o gancho e a tela {telas} e o convite.')
    return ia.json_por_schema(MODELO, SISTEMA, pedido, SCHEMA, max_tokens=8000)


def main():
    p = argparse.ArgumentParser(description='Carrossel de Instagram do escritorio')
    p.add_argument('tema')
    p.add_argument('--telas', type=int, default=7)
    a = p.parse_args()

    print(f'Escrevendo carrossel de {a.telas} telas sobre "{a.tema}"...\n')
    c = gerar(a.tema, a.telas)

    linhas = [f"# Carrossel - {c['tema']}", '', f'_{ESCRITORIO["nome_curto"]} - revisar antes de postar._', '']
    for t in c['telas']:
        print(f"TELA {t['numero']} ({t['papel']})")
        print(f"  {t['titulo']}")
        print(f"  {t['texto']}\n")
        linhas += [f"## Tela {t['numero']} - {t['papel']}", '', f"**{t['titulo']}**", '', t['texto'], '']
    linhas += ['## Legenda do post', '', c['legenda'], '',
               ' '.join(f'#{h.lstrip("#")}' for h in c['hashtags']), '',
               '## Conferir antes de postar', '', *[f'- [ ] {x}' for x in c['conferir']], '']

    print('LEGENDA:\n' + c['legenda'])
    print('\nCONFERIR: ' + '; '.join(c['conferir']))

    pasta = ambiente.pasta_saida('carrosseis')
    base = f"{date.today().isoformat()}-" + ''.join(ch if ch.isalnum() else '-' for ch in a.tema.lower())[:40].strip('-')
    with open(os.path.join(pasta, base + '.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(linhas))
    with open(os.path.join(pasta, base + '.json'), 'w', encoding='utf-8') as f:
        json.dump(c, f, ensure_ascii=False, indent=2)
    print(f"\nSalvo em: {os.path.join(pasta, base + '.md')}")


if __name__ == '__main__':
    main()
