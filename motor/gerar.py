"""Gera um Short completo a partir de um roteiro: narração + render + pacote de SEO.

Uso:
    python3 motor/gerar.py roteiros/exemplos/2026-10-27_noticia-do-forro.json saida/
    python3 motor/gerar.py roteiros/semana/*.json saida/          (vários de uma vez)

Cada roteiro sai em saida/<slug>/ com o MP4, a legenda (.srt/.ass), as cenas em PNG e o SEO.txt.
"""
import glob
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audio  # noqa: E402
import render  # noqa: E402


def seo_txt(rot, destino):
    seo = rot.get("seo")
    if not seo:
        return
    linhas = [rot.get("titulo_interno", rot["slug"]), ""]
    linhas.append("TÍTULO (opções)")
    for i, t in enumerate(seo.get("titulos", []), 1):
        linhas.append(f"{i}. {t}" + ("   ← recomendado" if i == 1 else ""))
    linhas += ["", "DESCRIÇÃO", seo.get("descricao", "")]
    if rot.get("fontes"):
        linhas += ["", "Fontes:"] + [f"- {f['fato']}: {f['url']}" for f in rot["fontes"]]
    linhas += ["", "TAGS", ", ".join(seo.get("tags", [])), "", "COMENTÁRIO FIXADO", seo.get("comentario_fixado", ""),
               "", "VÍDEO RELACIONADO", seo.get("video_relacionado", "[DEFINIR]")]
    open(destino, "w", encoding="utf-8").write("\n".join(linhas) + "\n")


def gerar(roteiro_path, saida_base):
    rot = json.load(open(roteiro_path, encoding="utf-8"))
    pasta = os.path.join(saida_base, rot["slug"])
    os.makedirs(pasta, exist_ok=True)
    t0 = time.time()
    audio.narrar(roteiro_path, pasta)
    render.main(roteiro_path, pasta)
    seo_txt(rot, os.path.join(pasta, "SEO.txt"))
    print(f"[{rot['slug']}] pronto em {time.time() - t0:.0f}s")


if __name__ == "__main__":
    *roteiros, saida = sys.argv[1:]
    arquivos = [f for padrao in roteiros for f in sorted(glob.glob(padrao))]
    for r in arquivos:
        gerar(r, saida)
