"""
Busca noticias recentes sobre direitos do motorista profissional no Google News (RSS publico).
Nao precisa de chave de API: le o XML aberto do Google News.

Para mudar os assuntos vigiados, mexa na lista QUERIES abaixo.
"""
import re
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import quote


QUERIES = [
    "caminhoneiro direitos trabalhistas",
    "motorista profissional hora extra",
    "lei do caminhoneiro 13103",
    "TST motorista decisao",
    "jornada motorista transporte rodoviario",
    "ANTT caminhoneiro norma",
    "adicional periculosidade motorista",
    "descanso motorista 35 horas",
    "acordo coletivo motoristas rodoviarios",
    "salario caminhoneiro piso",
    "convencao coletiva transporte rodoviario Santa Catarina",
    "justica do trabalho motorista Santa Catarina",
]


def _buscar_rss(query: str, dias: int = 7):
    """Busca o RSS do Google News para uma query e retorna itens dentro da janela."""
    url = (
        "https://news.google.com/rss/search?"
        f"q={quote(query)}&hl=pt-BR&gl=BR&ceid=BR:pt-419"
    )
    try:
        resp = requests.get(
            url, timeout=20,
            headers={"User-Agent": "Mozilla/5.0 Radar-Juridico"},
        )
        resp.raise_for_status()
    except Exception as e:
        print(f"   Erro RSS '{query}': {e}")
        return []

    corte = datetime.now(timezone.utc) - timedelta(days=dias)
    noticias = []
    try:
        root = ET.fromstring(resp.content)
    except Exception as e:
        print(f"   XML invalido '{query}': {e}")
        return []

    for item in root.iter("item"):
        titulo = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        descricao = (item.findtext("description") or "").strip()
        pub_str = item.findtext("pubDate") or ""
        fonte_el = item.find("source")
        fonte = fonte_el.text if fonte_el is not None else ""

        try:
            pub = parsedate_to_datetime(pub_str)
            if pub.tzinfo is None:
                pub = pub.replace(tzinfo=timezone.utc)
        except Exception:
            continue
        if pub < corte:
            continue

        # limpa HTML bruto da descricao
        descricao_limpa = re.sub(r"<[^>]+>", "", descricao).strip()
        descricao_limpa = re.sub(r"\s+", " ", descricao_limpa)

        noticias.append({
            "titulo": titulo,
            "link": link,
            "descricao": descricao_limpa,
            "fonte": fonte,
            "data": pub.strftime("%d/%m/%Y"),
            "query": query,
        })
    return noticias


def buscar_noticias_caminhoneiro(dias: int = 7, max_por_query: int = 5):
    """Busca todas as queries e deduplica por titulo."""
    todas = []
    vistos = set()
    for q in QUERIES:
        print(f"   Buscando: {q}")
        for n in _buscar_rss(q, dias=dias)[:max_por_query]:
            chave = n["titulo"].lower()[:80]
            if chave in vistos:
                continue
            vistos.add(chave)
            todas.append(n)
    print(f"   Total de noticias unicas: {len(todas)}")
    return todas


if __name__ == "__main__":
    noticias = buscar_noticias_caminhoneiro()
    for n in noticias[:10]:
        print(f"- [{n['fonte']}] {n['titulo']}")
        print(f"  {n['data']} | {n['link'][:90]}")
