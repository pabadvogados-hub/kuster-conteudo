# Comece aqui

Dois programas, instalados uma vez por máquina:

- **Python 3.11 ou mais novo** — https://www.python.org/downloads/
  Marque **"Add Python to PATH"** na primeira tela.
- **Node.js 20 ou mais novo** — https://nodejs.org (só para a parte de vídeo).

## Instalação

```
git clone https://github.com/pabadvogados-hub/kuster-conteudo.git
cd kuster-conteudo

pip install -r requirements.txt
copy config\.env.example config\.env
```

Abra `config\.env` e cole a chave da Anthropic (`ANTHROPIC_API_KEY`). É a única coisa obrigatória:
ela paga a escrita dos roteiros, dos artigos e dos carrosséis. Pega em https://console.anthropic.com.

Para o estúdio de vídeo, mais um passo:

```
cd ESTUDIO_VIDEO
npm install
```

## O dia a dia

**Precisa de ideia para gravar hoje**
```
python ROTEIROS/main.py dia
```
Saem 5 roteiros, um de cada formato, já com gancho, corpo, fechamento, o que escrever na tela e a
legenda do post. Ficam em `SAIDA/roteiros/`.

Tema seu, em vez do rodízio:
```
python ROTEIROS/main.py tema "desconto de avaria no salário" --formato mito
python ROTEIROS/main.py formatos
```

**Gravou, quer o vídeo pronto**
```
cd ESTUDIO_VIDEO
npm run legendar
node editar.mjs <nome-do-corte>
```
Passo a passo e o que vai em cada campo: `docs/COMO_EDITAR_UM_SHORT.md`.

**Artigo para o blog ou o JusBrasil**
```
python ARTIGOS/main.py noticias       o que saiu na semana
python ARTIGOS/main.py novo           escolhe a melhor pauta e escreve
python ARTIGOS/main.py novo --tema "horas de espera"
```
O rascunho cai em `SAIDA/artigos/`, com um checklist de conferência no topo do arquivo.

**Carrossel para o Instagram**
```
python CARROSSEL/main.py "o que guardar antes de sair da empresa"
```

## Antes de publicar qualquer coisa

Leia uma vez `docs/PUBLICIDADE_OAB.md`. Vale para vídeo, artigo e carrossel.
Resumo: pode ensinar o direito, não pode prometer resultado, não pode falar valor, não pode
identificar cliente nem empresa.

## Quando aparecer `[CONFERIR]`

É de propósito. Significa que a IA precisaria de uma informação do escritório que ninguém deu
ainda — o percentual, o prazo, a norma coletiva, o Instagram do escritório. Troque pelo dado certo
antes de postar. O que ainda falta preencher está em `docs/O_QUE_FALTA.md`.
