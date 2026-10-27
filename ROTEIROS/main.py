"""
Roteiros de video vertical (Reels / Shorts / TikTok) para o escritorio gravar.

    python ROTEIROS/main.py dia                      5 roteiros, um de cada formato
    python ROTEIROS/main.py dia --quantos 3          so os 3 primeiros formatos
    python ROTEIROS/main.py tema "hora de espera"    1 roteiro sobre um tema seu
    python ROTEIROS/main.py tema "..." --formato mito
    python ROTEIROS/main.py formatos                 lista os formatos disponiveis

Cada rodada salva em SAIDA/roteiros/AAAA-MM-DD.md (para ler e gravar) e .json (para o estudio).
Nada e publicado: o roteiro sai para o advogado ler, ajustar e gravar.
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

MODELO = os.getenv('MODELO_ROTEIROS', 'claude-sonnet-5')

# ---------------------------------------------------------------------------
# Os 5 formatos. Nao e "persona de influenciador": e o jeito de montar o video.
# ---------------------------------------------------------------------------
FORMATOS = {
    'direito': {
        'nome': 'O direito que voce nao sabia que tinha',
        'como': 'Abre com o direito dito de forma crua ("isso aqui a empresa te deve"), explica em '
                'uma frase de onde ele vem, da um exemplo da rotina e fecha com o que fazer. '
                'Nenhum numero de valor, nenhuma promessa.',
    },
    'mito': {
        'nome': 'Mito x verdade',
        'como': 'Comeca pela frase errada que todo mundo repete no patio, diz que esta errada e '
                'mostra o que a lei diz. A virada vem no meio: "o que quase ninguem sabe e...".',
    },
    'prova': {
        'nome': 'Como se prova',
        'como': 'Foco em prova, nao em direito: o que guardar, onde conseguir, como anotar. Sai '
                'com uma lista curta de 3 a 5 itens que o motorista consegue fazer hoje.',
    },
    'bastidor': {
        'nome': 'Bastidor do processo',
        'como': 'Tira o medo: explica uma etapa do processo trabalhista em linguagem de motorista '
                '(quanto tempo leva, o que acontece na audiencia, se precisa faltar servico). '
                'Nunca fala de valor nem de chance de ganhar.',
    },
    'pergunta': {
        'nome': 'Pergunta de motorista',
        'como': 'Abre com uma pergunta real que aparece no direct, generica e sem identificar '
                'ninguem, e responde em 40 segundos. Se a resposta depender do caso, dizer isso.',
    },
}

TEMAS_BASE = [
    'hora de espera no patio de carga e descarga',
    'jornada e horas extras do motorista empregado',
    'descanso entre jornadas e as 35 horas de viagem longa',
    'desconto indevido no salario (avaria, combustivel, multa, carga)',
    'parte do salario paga "por fora" e comissao nao registrada',
    'adicional de periculosidade do motorista que roda com dois tanques',
    'diario de bordo, rastreador e tacografo como prova da jornada',
    'registro do contrato na carteira e tempo trabalhado sem registro',
    'prazo para entrar com a acao depois que saiu da empresa',
    'o que guardar antes de pedir demissao ou ser mandado embora',
]

SCHEMA = {
    'type': 'object',
    'properties': {
        'roteiros': {
            'type': 'array',
            'items': {
                'type': 'object',
                'properties': {
                    'formato': {'type': 'string'},
                    'tema': {'type': 'string'},
                    'titulo': {'type': 'string', 'description': 'nome do arquivo do corte, curto e em minusculo com hifen'},
                    'gancho': {'type': 'string', 'description': 'os 3 primeiros segundos, 1 ou 2 frases'},
                    'corpo': {'type': 'string', 'description': 'o que falar, 40 a 60 segundos'},
                    'cta': {'type': 'string'},
                    'texto_na_tela': {
                        'type': 'array',
                        'items': {'type': 'string'},
                        'description': '2 a 4 palavras ou expressoes curtas para aparecer escritas na tela',
                    },
                    'legenda_do_post': {'type': 'string'},
                    'checar_antes_de_gravar': {'type': 'string', 'description': 'o que o advogado precisa conferir'},
                },
                'required': ['formato', 'tema', 'titulo', 'gancho', 'corpo', 'cta',
                             'texto_na_tela', 'legenda_do_post', 'checar_antes_de_gravar'],
                'additionalProperties': False,
            },
        }
    },
    'required': ['roteiros'],
    'additionalProperties': False,
}

SISTEMA = f"""Voce escreve roteiros de video vertical curto para um escritorio de advocacia
trabalhista gravar. Quem grava e o proprio advogado, de cara, falando em primeira pessoa.

ESCRITORIO: {ESCRITORIO['nome_curto']}, {ESCRITORIO['cidade']}. Atua pelo trabalhador.
PUBLICO: {PUBLICO['quem']}.
A ROTINA DELE: {PUBLICO['rotina']}.
A DOR DELE: {PUBLICO['dor']}.
LINGUAGEM: {PUBLICO['nivel']}

COMO O ESCRITORIO FALA: {TOM['como_fala']}
NUNCA: {TOM['nunca']}
SEMPRE: {TOM['sempre']}

{REGRAS_OAB}
{CONTEXTO_JURIDICO}

REGRAS DE ROTEIRO:
1. Portugues do Brasil falado, nao escrito. Frase curta. Nada de "prezado", "outrossim", "venho
   por meio deste".
2. O gancho segura nos 3 primeiros segundos: uma afirmacao que gera tensao. Nunca "fala galera",
   nunca apresentacao, nunca "hoje eu vou falar sobre".
3. Uma ideia por video, bem desenvolvida, com uma virada no meio.
4. Exemplo concreto da rotina do motorista, nunca um caso real identificavel.
5. NUNCA inventar lei, artigo, sumula, tema repetitivo ou decisao. So citar o que e certo
   (CLT, Lei 13.103/2015). Na duvida, falar do direito sem o numero da lei.
6. Se algo depender de conferencia do advogado (um prazo, um percentual, uma norma coletiva),
   escrever [CONFERIR] no roteiro e repetir em "checar_antes_de_gravar".
7. O CTA e convite para se informar, nunca promessa. Use um destes, ou algo no mesmo nivel:
   {' | '.join(CTA_PERMITIDOS)}
8. Sem emoji, sem hashtag no corpo do roteiro, sem markdown.
"""


def _pedido(itens):
    linhas = []
    for formato, tema in itens:
        f = FORMATOS[formato]
        linhas.append(f"- formato \"{formato}\" ({f['nome']}) | tema: {tema}\n  como montar: {f['como']}")
    return (
        f"Escreva {len(itens)} roteiro(s), um para cada linha abaixo.\n\n"
        + '\n'.join(linhas)
        + "\n\nCada roteiro independente do outro. Se forem varios, que sejam diferentes em "
          "estrutura, nao so em assunto.\nNo campo 'formato' devolva a chave exata (ex.: \"mito\")."
    )


def gerar(itens):
    dados = ia.json_por_schema(MODELO, SISTEMA, _pedido(itens), SCHEMA, max_tokens=16000)
    return dados['roteiros']


def _markdown(roteiros, titulo):
    linhas = [f'# {titulo}', '',
              f'_{ESCRITORIO["nome_curto"]} - roteiros para gravar. Revise antes de ir para a camera._', '']
    for i, r in enumerate(roteiros, 1):
        f = FORMATOS.get(r.get('formato', ''), {}).get('nome', r.get('formato', ''))
        linhas += [
            f'## {i}. {r.get("titulo", "")}', '',
            f'**Formato:** {f}  ', f'**Tema:** {r.get("tema", "")}', '',
            '### Gancho (3 primeiros segundos)', r.get('gancho', ''), '',
            '### Corpo', r.get('corpo', ''), '',
            '### Fechamento', r.get('cta', ''), '',
            '### Texto na tela', *[f'- {t}' for t in r.get('texto_na_tela', [])], '',
            '### Legenda do post', r.get('legenda_do_post', ''), '',
            f'> **Conferir antes de gravar:** {r.get("checar_antes_de_gravar", "")}', '',
            '---', '',
        ]
    linhas += ['Nome do arquivo ao gravar: `ESTUDIO_VIDEO/public/<titulo>.mp4`.',
               'Depois: `npm run legendar` e `node editar.mjs <titulo>`.', '']
    return '\n'.join(linhas)


def _salvar(roteiros, nome):
    pasta = ambiente.pasta_saida('roteiros')
    md = os.path.join(pasta, f'{nome}.md')
    js = os.path.join(pasta, f'{nome}.json')
    with open(md, 'w', encoding='utf-8') as f:
        f.write(_markdown(roteiros, nome))
    with open(js, 'w', encoding='utf-8') as f:
        json.dump(roteiros, f, ensure_ascii=False, indent=2)
    return md, js


def _mostrar(roteiros):
    for r in roteiros:
        print()
        print('=' * 72)
        print(f"{r.get('titulo', '')}  [{r.get('formato', '')}]")
        print('=' * 72)
        print(f"GANCHO: {r.get('gancho', '')}\n")
        print(r.get('corpo', ''))
        print(f"\nFECHA: {r.get('cta', '')}")
        print(f"TELA:  {', '.join(r.get('texto_na_tela', []))}")
        print(f"CONFERIR: {r.get('checar_antes_de_gravar', '')}")


def main():
    p = argparse.ArgumentParser(description='Roteiros de video curto do escritorio')
    sub = p.add_subparsers(dest='comando', required=True)

    d = sub.add_parser('dia', help='um roteiro de cada formato')
    d.add_argument('--quantos', type=int, default=5)

    t = sub.add_parser('tema', help='um roteiro sobre um tema seu')
    t.add_argument('assunto')
    t.add_argument('--formato', default='direito', choices=list(FORMATOS))

    sub.add_parser('formatos', help='lista os formatos')

    a = p.parse_args()

    if a.comando == 'formatos':
        for chave, f in FORMATOS.items():
            print(f"\n{chave}  -  {f['nome']}\n  {f['como']}")
        return

    if a.comando == 'dia':
        chaves = list(FORMATOS)[:max(1, min(a.quantos, len(FORMATOS)))]
        giro = date.today().toordinal()
        itens = [(c, TEMAS_BASE[(giro + i) % len(TEMAS_BASE)]) for i, c in enumerate(chaves)]
        nome = date.today().isoformat()
    else:
        itens = [(a.formato, a.assunto)]
        nome = f"{date.today().isoformat()}-{a.formato}"

    print(f'Gerando {len(itens)} roteiro(s) com {MODELO}...')
    roteiros = gerar(itens)
    _mostrar(roteiros)
    md, js = _salvar(roteiros, nome)
    print(f'\nSalvo em:\n  {md}\n  {js}')


if __name__ == '__main__':
    main()
