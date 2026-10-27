# O que falta para o conteúdo sair com a cara do escritório

Este pacote foi montado em **27/10/2026**, antes do briefing, como o repositório do sistema
(`kuster-francisco-advocacia`). Funciona hoje, do jeito que está. Os itens abaixo são o que falta
para parar de sair `[CONFERIR]`.

## 1. Marca (`config/marca.py`)

| O que | Onde entra |
|---|---|
| Cor do escritório (hexadecimal) | legenda, callout e barra do vídeo; hoje é um azul provisório `#1F6FEB` |
| Instagram, site e WhatsApp público | rodapé dos artigos e fechamento dos posts |
| Confirmar a assinatura: só o Dr. Álvaro assina, ou cada advogado assina o que escreve | artigos e posts |

Trocada a cor em `config/marca.py`, troque também em `ESTUDIO_VIDEO/src/Root.tsx` e no `accent`
de cada `edit.json`.

## 2. Voz (o que mais muda o resultado)

Três conteúdos que o escritório já publicou e gostou — post, vídeo ou texto, tanto faz. Com eles
dá para afinar o `TOM` e os exemplos em `config/marca.py` e o texto deixa de ter cara de IA.

Se nunca publicou nada, está valendo o padrão: direto, frase curta, de igual para igual.

## 3. Decisões

1. **Quem grava.** O rodízio de 5 formatos presume um rosto fixo (o Dr. Álvaro). Se for revezar
   com a Dra. Bruna, dá para separar os formatos por pessoa.
2. **Frequência.** Hoje o comando é manual. Se o escritório quiser no automático (5 roteiros toda
   segunda, por exemplo), é uma tarefa agendada no Windows — 10 minutos para montar.
3. **Onde publica.** Instagram e TikTok estão contemplados pelo formato vertical. Blog próprio ou
   JusBrasil muda só o destino do artigo.
4. **Temas proibidos.** Tese que o escritório não gosta de usar, assunto que não quer tocar:
   mande a lista que ela entra no prompt.

## 4. O que ainda não foi feito, e dá para fazer

- Publicação automática no Instagram (precisa de conta profissional + Meta Business).
- Corte sugerido pela IA: ela lê a transcrição e propõe os `ranges` do `edit.json`. Hoje os tempos
  são anotados na mão (dá uns 10 minutos por vídeo).
- B-roll automático (imagem de apoio entrando a cada 3 s). Depende de um banco de imagens do
  escritório.
- Medição: o que rendeu mais lead. Depende de acesso ao Meta Ads, que já está previsto no outro
  repositório.
