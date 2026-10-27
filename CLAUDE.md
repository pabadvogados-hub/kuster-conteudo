# Küster & Francisco - Conteúdo e Vídeo

> Escritório: **Küster & Francisco Advocacia e Consultoria Jurídica**, Ituporanga/SC.
> Titular: **Dr. Álvaro Küster (OAB/SC 47.188)**. Nicho: motorista profissional (caminhoneiro).
> Este repositório é o **pacote de conteúdo**. O sistema jurídico fica em `kuster-francisco-advocacia`.

## Regra de ouro
- **Nada é publicado daqui.** Todo texto sai em `SAIDA/` como rascunho, para revisão humana.
- **Provimento 205/2021 da OAB** está no prompt de todo gerador (`config/marca.py` → `REGRAS_OAB`):
  sem promessa de resultado, sem valor, sem nome de cliente ou de empresa, sem gatilho de escassez.
- **Nunca inventar lei, artigo, súmula, tema ou decisão.** Sem certeza: `[CONFERIR]`.
- **Nenhum dado real de cliente neste repositório** - ele é público. Vídeo, áudio, legenda e
  rascunho estão no `.gitignore`.

## Mapa
| Pasta | Papel |
|---|---|
| `config/marca.py` | voz, público, cor e as regras da OAB. Tudo que a IA escreve lê daqui |
| `NUCLEO/` | `ambiente.py` (carrega o .env) e `ia.py` (chamadas ao Claude com schema) |
| `ROTEIROS/` | roteiros de vídeo vertical, 5 formatos |
| `ESTUDIO_VIDEO/` | Remotion + Whisper: corte, legenda queimada, callout, hook |
| `ARTIGOS/` | Google News RSS → pauta → artigo SEO |
| `CARROSSEL/` | 7 telas de Instagram |
| `SAIDA/` | o que foi gerado (não versionado) |

## Estúdio de vídeo
O editor é o `Short` (`ESTUDIO_VIDEO/src/Short/index.tsx`): recebe os trechos mantidos em
milissegundos **do vídeo original**, emenda, aplica fade de 2 quadros no áudio de cada emenda,
alterna o zoom a cada corte acima de 0,8 s, e sincroniza a legenda pelo `.json` do Whisper.
`calculateShortMetadata` recalcula os tempos das palavras para o vídeo já cortado.

Alterar o visual do vídeo = mexer em `Short/index.tsx`. Alterar o ritmo = mexer nos `ranges` do
`edit.json`, não no componente.

## O que NÃO fazer
- Não colocar chave de API em arquivo versionado: só em `config/.env`.
- Não commitar `.mp4`, `.mp3`, `.wav` nem o `.json` de legenda (tem a fala inteira transcrita).
- Não tirar o bloco `REGRAS_OAB` dos prompts.
- Não publicar nada com `[CONFERIR]` no texto.
