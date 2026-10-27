# Küster & Francisco — Conteúdo e Vídeo

Pacote de produção de conteúdo do escritório: **roteiro → gravação → edição → post**, para o
nicho de motorista profissional (caminhoneiro).

São quatro peças que funcionam separadas:

| Pasta | O que faz | Comando |
|---|---|---|
| `ROTEIROS/` | 5 roteiros de vídeo vertical por rodada, um de cada formato | `python ROTEIROS/main.py dia` |
| `ESTUDIO_VIDEO/` | corta, legenda e monta o vídeo a partir de um arquivo de texto | `node editar.mjs <corte>` |
| `ARTIGOS/` | artigo de blog/JusBrasil a partir das notícias da semana | `python ARTIGOS/main.py novo` |
| `CARROSSEL/` | as 7 telas de um carrossel de Instagram | `python CARROSSEL/main.py "tema"` |

Instalação e uso no dia a dia: **[docs/COMECE_AQUI.md](docs/COMECE_AQUI.md)**.

## O estúdio de vídeo, em uma frase

Você escreve num `edit.json` quais pedaços da gravação ficam, e o computador monta o vídeo com
legenda sincronizada palavra por palavra, palavra-chave na cor da marca, zoom alternado a cada
corte, callouts e barra de progresso. Refazer uma versão custa um comando.
Detalhes: [docs/COMO_EDITAR_UM_SHORT.md](docs/COMO_EDITAR_UM_SHORT.md).

Feito com [Remotion](https://remotion.dev) (vídeo) e [Whisper](https://github.com/ggerganov/whisper.cpp)
(legenda, roda na própria máquina, sem custo e sem subir o vídeo para lugar nenhum).

## Regras que estão no código, não só no papel

- **Nada é publicado automaticamente.** Tudo cai em `SAIDA/` como rascunho, com checklist de
  conferência. Quem assina responde.
- **Provimento 205/2021 da OAB** entra no prompt de todo texto gerado: nada de promessa de
  resultado, valor, nome de cliente ou de empresa. Ver [docs/PUBLICIDADE_OAB.md](docs/PUBLICIDADE_OAB.md).
- **A IA não inventa lei.** Onde falta certeza, sai `[CONFERIR]` — para o advogado ver na hora.
- **Nada de dado de cliente neste repositório.** Ele é público: serve para instalar o pacote em
  qualquer máquina do escritório. Vídeo, áudio, legenda e rascunho ficam fora do Git.

## Estado

Montado em 27/10/2026, antes do briefing. Roda hoje. O que falta para sair com a identidade do
escritório (cor, Instagram, voz) está em [docs/O_QUE_FALTA.md](docs/O_QUE_FALTA.md).

Sistema jurídico do escritório (triagem, contratação, peças, controladoria, financeiro):
[kuster-francisco-advocacia](https://github.com/pabadvogados-hub/kuster-francisco-advocacia).
