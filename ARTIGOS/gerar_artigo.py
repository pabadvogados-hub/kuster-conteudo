"""
Escreve um artigo de blog / JusBrasil a partir de uma noticia recente, na voz do escritorio.

O artigo sai para REVISAO: nada e publicado por aqui. O que a IA nao tiver certeza vira [CONFERIR].
"""
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'NUCLEO'))
import ambiente  # noqa: E402  (carrega o .env)
import ia  # noqa: E402
from config.marca import ESCRITORIO, ASSINATURA, PUBLICO, TOM, REGRAS_OAB, CONTEXTO_JURIDICO  # noqa: E402

MODELO = os.getenv('MODELO_ARTIGOS', 'claude-opus-5')
MODELO_TRIAGEM = os.getenv('MODELO_TRIAGEM', 'claude-haiku-5-5')

SISTEMA = f"""Voce e o redator juridico do {ESCRITORIO['nome']} ({ESCRITORIO['cidade']}), escritorio
de direito do trabalho que atua pelo trabalhador, com foco em motorista profissional de carga.

O artigo tem tres objetivos, nesta ordem: orientar o motorista, ser achado no Google e dar
autoridade ao escritorio.

PUBLICO: {PUBLICO['quem']}. A rotina dele: {PUBLICO['rotina']}.
A dor dele: {PUBLICO['dor']}.
LINGUAGEM: {PUBLICO['nivel']}
TOM: {TOM['como_fala']} Nunca: {TOM['nunca']}.

{REGRAS_OAB}
{CONTEXTO_JURIDICO}

TECNICA JURIDICA
Precisao absoluta: CLT, Lei 13.103/2015 (Lei do Motorista), normas da ANTT, jurisprudencia do TST,
convencao coletiva da categoria. NUNCA inventar numero de lei, artigo, sumula, tema ou precedente.
Se nao tiver certeza do numero, escreva o direito sem o numero e marque [CONFERIR] ao lado.
Quando a noticia for decisao judicial, explique o efeito pratico, sem prometer o mesmo resultado
para quem le.

ESTRUTURA
1. Titulo H1 de 55 a 70 caracteres, com a palavra-chave no comeco.
2. Primeiro paragrafo: repete a palavra-chave e nomeia a dor do leitor.
3. De 2 a 4 subtitulos H2 com palavras-chave secundarias; H3 quando precisar detalhar.
4. Pelo menos uma lista com marcadores.
5. Um exemplo pratico da rotina do motorista (ficticio e generico, nunca caso real).
6. Um bloco "o que guardar" com a prova que o leitor consegue juntar sozinho.
7. Fechamento: convite para se informar, dentro do Provimento 205/2021.
8. Assinatura: "{ASSINATURA}".

TAMANHO: 1000 a 1500 palavras.

NAO FAZER: clickbait, promessa de resultado, valor de indenizacao, critica a juiz ou a empresa com
nome, jargao sem traducao, mais de 20% do texto em citacao literal de lei, disclaimer longo.
"""

SCHEMA = {
    'type': 'object',
    'properties': {
        'titulo': {'type': 'string'},
        'meta_description': {'type': 'string', 'description': 'ate 155 caracteres, com a palavra-chave'},
        'palavra_chave_principal': {'type': 'string'},
        'palavras_chave_secundarias': {'type': 'array', 'items': {'type': 'string'}},
        'corpo_markdown': {'type': 'string', 'description': "artigo completo em markdown, comecando por '# Titulo'"},
        'resumo': {'type': 'string', 'description': 'duas frases sobre o artigo'},
        'conferir_antes_de_publicar': {
            'type': 'array',
            'items': {'type': 'string'},
            'description': 'cada ponto que o advogado precisa checar (lei citada, prazo, percentual)',
        },
    },
    'required': ['titulo', 'meta_description', 'palavra_chave_principal',
                 'palavras_chave_secundarias', 'corpo_markdown', 'resumo',
                 'conferir_antes_de_publicar'],
    'additionalProperties': False,
}


def gerar_artigo(noticia: dict) -> dict:
    pedido = f"""Escreva o artigo a partir do tema abaixo.

Titulo da noticia: {noticia.get('titulo', '')}
Fonte: {noticia.get('fonte', '')}
Data: {noticia.get('data', '')}
Resumo: {noticia.get('descricao', '')}
Link: {noticia.get('link', '')}

Nao reproduza a noticia. Use como gancho para ensinar o motorista sobre o direito envolvido.
O texto precisa continuar util daqui a seis meses, mesmo aproveitando a atualidade de hoje."""

    artigo = ia.json_por_schema(MODELO, SISTEMA, pedido, SCHEMA, max_tokens=20000)
    artigo['_noticia'] = noticia
    artigo['_gerado_em'] = datetime.now().isoformat(timespec='seconds')
    artigo['_modelo'] = MODELO
    return artigo


def escolher_melhor_noticia(noticias: list, historico: list):
    """A IA escolhe qual noticia rende o melhor artigo, evitando tema ja publicado."""
    if not noticias:
        return None
    if len(noticias) == 1:
        return noticias[0]

    ja_feitos = '\n'.join(f"- {h.get('titulo', '')}" for h in historico[-30:]) or '(nenhum)'
    candidatos = '\n'.join(
        f"{i + 1}. [{n['fonte']}] {n['titulo']} ({n['data']})\n   {n['descricao'][:200]}"
        for i, n in enumerate(noticias[:25])
    )
    pedido = f"""Escolha a MELHOR noticia para virar artigo sobre direitos do motorista profissional.

Criterios, nesta ordem:
1. Trata de um direito concreto do motorista (nao politica, nao economia, nao acidente sem
   consequencia juridica).
2. Alguem digitaria isso no Google.
3. Nao repete tema ja publicado.

Ja publicados:
{ja_feitos}

Candidatos:
{candidatos}"""

    escolha = ia.json_por_schema(
        MODELO_TRIAGEM, 'Voce escolhe pautas juridicas. Responda so o numero escolhido.', pedido,
        {'type': 'object', 'properties': {'numero': {'type': 'integer'}, 'porque': {'type': 'string'}},
         'required': ['numero', 'porque'], 'additionalProperties': False},
        max_tokens=1000,
    )
    i = max(0, min(int(escolha.get('numero', 1)) - 1, len(noticias) - 1))
    noticias[i]['_escolhida_porque'] = escolha.get('porque', '')
    return noticias[i]
