# Como editar um vídeo vertical

A edição aqui não é feita arrastando clipe na linha do tempo. Você escreve **o que fica** num
arquivo de texto (`edit.json`) e o computador monta o vídeo: corte, legenda queimada, palavra
destacada na cor da marca, zoom alternado, barra de progresso e o cartão do gancho.

Vantagem prática: refazer uma versão custa um comando. Mudou de ideia sobre um corte? Muda dois
números e roda de novo.

---

## O caminho inteiro, uma vez

```
cd ESTUDIO_VIDEO
npm install                       (só na primeira vez)
```

1. **Grave** o take (celular na vertical serve) e salve em `ESTUDIO_VIDEO/public/espera.mp4`.
2. **Legende**: `npm run legendar` — gera `public/espera.json` com cada palavra e o tempo dela.
   Na primeira vez ele baixa o Whisper (uns 500 MB). Roda na sua máquina, sem custo e sem mandar
   o vídeo para lugar nenhum.
3. **Decida os cortes**: copie `edits/EXEMPLO/` para `edits/espera/` e preencha o `edit.json`.
4. **Monte**: `node editar.mjs espera` → sai `edits/espera/final.mp4`.

Para ver antes de renderizar, com tudo ao vivo: `npm run estudio` (abre no navegador, composição
`Short`). Horizontal para YouTube: `node editar.mjs espera --largo`.

---

## O `edit.json`, campo a campo

```json
{
  "video": "espera.mp4",
  "captions": "espera.json",
  "accent": "#1F6FEB",
  "ranges": [
    { "fromMs": 0,     "toMs": 8400 },
    { "fromMs": 9100,  "toMs": 21600 }
  ],
  "hook": { "text": "Hora de *espera* não é descanso", "seconds": 2.8 },
  "callouts": [ { "text": "Lei 13.103", "atMs": 11200 } ],
  "showCaptions": true
}
```

| Campo | O que é |
|---|---|
| `video` | o arquivo bruto, dentro de `public/` |
| `captions` | o `.json` de palavras que o `npm run legendar` criou |
| `accent` | a cor da marca. Pinta a palavra que está sendo dita, o callout e a barra |
| `ranges` | **o coração**: os pedaços que ficam, em milissegundos **do vídeo original**, na ordem |
| `hook` | cartão branco nos primeiros segundos. `*palavra*` sai realçada na cor da marca |
| `callouts` | palavra gigante que aparece por 1,2 s. `atMs` é o tempo **no vídeo original** |
| `showCaptions` | `false` só em vídeo longo, que vai levar legenda do YouTube em vez de queimada |

Dois detalhes que poupam dor de cabeça:

- `fromMs`/`toMs` e `atMs` são sempre tempos **da gravação crua**, não do vídeo já cortado. Você
  assiste o bruto uma vez, anota os tempos e pronto — não precisa recalcular nada quando mexer
  num corte.
- Um callout que cair dentro de um pedaço cortado simplesmente não aparece. Não quebra nada.

O que o sistema faz sozinho: emenda os trechos, aplica fade de 2 quadros no áudio de cada emenda
(corte sem "clique"), alterna o enquadramento a cada corte acima de 0,8 s (efeito de duas câmeras
com uma só), sincroniza a legenda palavra por palavra e desenha a barra de progresso.

---

## O ritmo (o que faz o vídeo segurar)

Destrinchado de vídeos que seguram bem (Fireship, Ali Abdaal, Doutor Fran, Primo Studio):

- **Corte a cada 2 a 4 segundos.** Isso é o que prende, não efeito. Na prática: tire toda respiração,
  todo "é...", todo começo de frase repetido. Um take de 90 s vira 45 s e fica melhor.
- **Os 3 primeiros segundos decidem.** Comece pela afirmação que incomoda. Nada de "fala pessoal",
  nada de apresentação, nada de "hoje eu vou falar sobre". A apresentação, se couber, vai no fim.
- **Uma ideia por vídeo.** Duas ideias viram dois vídeos.
- **Callout onde a pessoa precisa ler**, não onde está bonito: nome de lei, número, nome do
  documento. De 2 a 4 por vídeo. Mais que isso vira poluição.
- **40 a 60 segundos** é o ponto. Acima de 90 s a retenção cai de verdade.
- **Fim seco.** Terminou a ideia, acabou o vídeo. Não fique despedindo.

## Antes de publicar

- [ ] Passou pelo `docs/PUBLICIDADE_OAB.md` (nada de promessa, valor ou caso identificável)
- [ ] Nenhum `[CONFERIR]` sobrou no texto do roteiro ou na legenda
- [ ] Nenhum nome de cliente, de empresa ou número de processo aparece na fala ou na tela
- [ ] A legenda queimada está certa (o Whisper erra nome próprio e sigla — confira na prévia)
- [ ] Quem assina o conteúdo é advogado inscrito, e está identificado no perfil
