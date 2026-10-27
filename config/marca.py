"""
A voz do escritorio. Tudo que a IA escreve (roteiro, artigo, carrossel) le daqui.

Os campos marcados com [CONFERIR] sao chute provisorio feito sem o briefing: trocar pelo que o
escritorio usa de verdade. Enquanto estiverem assim, o texto sai com o marcador no lugar e
voce enxerga na hora o que ainda nao foi confirmado.
"""

ESCRITORIO = {
    'nome': 'Küster & Francisco Advocacia e Consultoria Jurídica',
    'nome_curto': 'Küster & Francisco',
    'cidade': 'Ituporanga/SC',
    'titular': 'Dr. Álvaro Küster',
    'oab_titular': 'OAB/SC 47.188',
    'oab_sociedade': 'OAB/SC 5.986',
    'instagram': '[CONFERIR]',
    'site': '[CONFERIR]',
    'whatsapp_publico': '[CONFERIR]',
}

# Assinatura que fecha artigo e post. Quem assina responde pelo conteudo perante a OAB.
ASSINATURA = f"{ESCRITORIO['titular']} — {ESCRITORIO['oab_titular']} — {ESCRITORIO['nome_curto']}"

VISUAL = {
    'cor_destaque': '#1F6FEB',   # [CONFERIR] azul provisorio: e a cor das legendas e dos callouts
    'cor_apoio': '#0B1B33',      # [CONFERIR]
    'fonte_video': 'Montserrat 900',
}

PUBLICO = {
    'quem': 'motorista profissional de carga (caminhoneiro), empregado de transportadora, e a '
            'familia dele',
    'rotina': 'patio de carga e descarga, espera, pernoite na estrada, diario de bordo, rastreador, '
              'tacografo, frete, pedagio, grupo da frota no WhatsApp',
    'dor': 'trabalha muito mais do que recebe, nao sabe o que pode cobrar e tem medo de "queimar o '
           'nome na praca" se processar a empresa',
    'nivel': 'linguagem simples. Termo tecnico so com a traducao do lado, entre parenteses.',
}

TOM = {
    'como_fala': 'direto, curto, de igual para igual. Frase curta. Sem juridiques, sem tom de '
                 'palanque, sem "prezado leitor".',
    'nunca': 'tom superior, drama, promessa de dinheiro, ataque a empresa com nome, piada com a '
             'categoria',
    'sempre': 'uma ideia por conteudo, um exemplo concreto da rotina do motorista, e o que fazer '
              'amanha de manha',
}

# ---------------------------------------------------------------------------
# Publicidade advocaticia - Provimento 205/2021 da OAB. Isto NAO e opcional.
# ---------------------------------------------------------------------------
REGRAS_OAB = """REGRAS DE PUBLICIDADE DA ADVOCACIA (Provimento 205/2021 da OAB) - obrigatorias:
- E informacao, nao anuncio. Pode ensinar o direito; nao pode vender o resultado.
- PROIBIDO prometer ou sugerir resultado ("voce vai receber", "ganho garantido", "indenizacao certa").
- PROIBIDO valor de honorario, promocao, desconto, parcelamento, "consulta gratis" como chamariz.
- PROIBIDO citar valor de condenacao obtida, nome de cliente, nome da empresa processada ou numero
  de processo.
- PROIBIDO mercantilizar: sorteio, brinde, gatilho de escassez ("ultimas vagas"), contagem regressiva.
- PROIBIDO depoimento de cliente e "caso de sucesso" identificavel.
- PROIBIDO captacao: falar com a pessoa como se o caso dela ja fosse uma causa ganha.
- A chamada para acao pode ser, no maximo, convite para se informar ou para procurar orientacao.
- Nunca inventar lei, artigo, sumula, tema repetitivo ou decisao. Na duvida, nao cita.
"""

# ---------------------------------------------------------------------------
# Pontos do nicho que a IA erra sozinha. Entram em todo prompt.
# ---------------------------------------------------------------------------
CONTEXTO_JURIDICO = """PONTOS DO NICHO QUE NAO PODEM SAIR ERRADOS:
- TEMPO DE ESPERA: o STF, na ADI 5322 (2023), derrubou os dispositivos da Lei 13.103/2015 que
  tiravam a espera da jornada. Hoje o tempo de espera INTEGRA a jornada de trabalho. NAO escrever
  que a espera e paga a 30% da hora normal - essa regra caiu. Se precisar entrar em detalhe de
  calculo, escrever [CONFERIR].
- A Lei 13.103/2015 continua valendo no resto (jornada, descanso, diario de bordo). O que caiu foi
  especificamente o tratamento da espera e do tempo de reserva.
- Direito de motorista empregado nao e o mesmo de motorista autonomo / agregado. Quando o conteudo
  falar de verba trabalhista, deixar claro que trata do motorista EMPREGADO.
- Muita verba depende de convencao coletiva da categoria e do estado. Nunca afirmar valor ou
  percentual de norma coletiva sem [CONFERIR].
- Prazo: a acao trabalhista tem prazo de 2 anos depois da saida da empresa, para cobrar os ultimos
  5 anos. Esse e o ponto mais util para o publico - pode e deve aparecer.
"""

CTA_PERMITIDOS = [
    'Ficou com duvida sobre a sua situacao? Procure um advogado de confianca.',
    'Salva esse video para nao esquecer o que anotar na proxima viagem.',
    'Manda para o motorista que precisa saber disso.',
    'Quer entender o seu caso? Chama no direct para falar com o escritorio.',
]
