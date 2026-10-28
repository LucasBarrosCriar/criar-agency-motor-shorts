"""Motor de Shorts do Universo do Piseiro — renderiza um roteiro.json em MP4 9:16.

Uso: python3 render.py roteiro.json build/
Precisa de: build/01_audio/N*.wav + duracoes.json (gerados por audio.py), FFmpeg e Pillow.
Saída: build/<slug>.mp4 + build/03_imagens/*.png + build/04_legendas/legenda.ass/.srt
"""
import json
import os
import re
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from audio import trilha_baiao  # noqa: E402

W, H, FPS = 1080, 1920, 30
T = 0.25  # duração da transição entre cenas (s)
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.environ.get("FONT_DIR", os.path.join(REPO, "marcas", "_provisoria", "fontes"))
ANTON = os.path.join(FONT_DIR, "Anton-Regular.ttf")
MONT = os.path.join(FONT_DIR, "Montserrat-VF.ttf")

# Identidade provisória do canal (trocar pelo kit oficial quando houver)
COR = {
    "noite": (16, 26, 51), "noite2": (34, 46, 92), "sol": (255, 122, 26),
    "amarelo": (255, 199, 44), "creme": (255, 244, 220), "vermelho": (215, 38, 61),
    "ouro": (255, 199, 44), "prata": (214, 222, 235), "bronze": (222, 142, 82),
}
LOGO = None       # PNG do logo (marca.json)
MOLDURA = None    # PNG transparente da moldura oficial do Short (logo + @), vai por cima do vídeo
ESTILO = "sol"    # "sol" (provisório) ou "listras" (Universo do Piseiro)
FONTE_LEG = "Anton"
ASS_FONT_DIR = FONT_DIR
DESLOC = 0        # empurra o conteúdo para baixo quando a moldura ocupa o topo


def resolver_marca(valor):
    """Aceita o nome de uma pasta em marcas/ ("universo-do-piseiro") ou um caminho para um marca.json."""
    if not valor:
        return None
    if os.path.exists(valor):
        return valor
    candidato = os.path.join(REPO, "marcas", valor, "marca.json")
    return candidato if os.path.exists(candidato) else None


def carregar_marca(caminho):
    """marca.json troca cores, fontes, logo, moldura e fundo sem mexer no código.
    Ex.: {"cores": {"noite": "#0A0605"}, "fonte_titulo": "/x/AlfaSlab.ttf", "fonte_texto": "/x/Zilla.ttf",
          "fonte_legenda": "Alfa Slab One", "logo": "/x/logo.png", "moldura": "/x/moldura.png",
          "estilo_fundo": "listras"}"""
    global ANTON, MONT, LOGO, MOLDURA, ESTILO, FONTE_LEG, ASS_FONT_DIR, DESLOC
    caminho = resolver_marca(caminho)
    if not caminho:
        return
    m = json.load(open(caminho, encoding="utf-8"))
    base = os.path.dirname(caminho)
    rel = lambda p: p if (not p or os.path.isabs(p)) else os.path.join(base, p)
    for chave in ("fonte_titulo", "fonte_texto", "logo", "moldura"):
        if chave in m:
            m[chave] = rel(m[chave])
    for nome, hexa in m.get("cores", {}).items():
        hexa = hexa.lstrip("#")
        COR[nome] = tuple(int(hexa[i:i + 2], 16) for i in (0, 2, 4))
    ANTON = m.get("fonte_titulo", ANTON)
    MONT = m.get("fonte_texto", MONT)
    LOGO = m.get("logo") or None
    MOLDURA = m.get("moldura") or None
    ESTILO = m.get("estilo_fundo", ESTILO)
    FONTE_LEG = m.get("fonte_legenda", FONTE_LEG)
    ASS_FONT_DIR = os.path.dirname(ANTON)
    DESLOC = 90 if MOLDURA else 0


def colar_logo(img, cx, y, largura=None, altura=None):
    logo = Image.open(LOGO).convert("RGBA")
    if largura:
        logo = logo.resize((largura, int(logo.height * largura / logo.width)), Image.LANCZOS)
    elif altura:
        logo = logo.resize((int(logo.width * altura / logo.height), altura), Image.LANCZOS)
    img.paste(logo, (int(cx - logo.width / 2), int(y)), logo)
    return y + logo.height


_SESSAO_RECORTE = None


def recortar(foto, destino):
    """Remove o fundo da foto oficial do artista (rembg, modelo aberto). Faz cache."""
    global _SESSAO_RECORTE
    if os.path.exists(destino):
        return Image.open(destino).convert("RGBA")
    os.environ.setdefault("U2NET_HOME", os.path.join(REPO, ".modelos", "rembg"))
    from rembg import new_session, remove
    if _SESSAO_RECORTE is None:
        _SESSAO_RECORTE = new_session("isnet-general-use")
    out = remove(Image.open(foto).convert("RGB"), session=_SESSAO_RECORTE)
    caixa = out.getbbox()
    if caixa:
        out = out.crop(caixa)
    out.save(destino)
    return out


def fonte(caminho, tamanho, peso=None):
    f = ImageFont.truetype(caminho, tamanho)
    if peso:
        try:
            f.set_variation_by_axes([peso])
        except Exception:
            pass
    return f


def caber(texto, caminho, tamanho_max, largura_max, peso=None):
    """Reduz o corpo até a linha mais larga caber na largura."""
    tam = tamanho_max
    while tam > 20:
        f = fonte(caminho, tam, peso)
        larg = max(f.getbbox(l)[2] - f.getbbox(l)[0] for l in texto.split("\n"))
        if larg <= largura_max:
            return f
        tam -= 4
    return fonte(caminho, tam, peso)


def texto_centro(d, y, texto, f, cor, sombra=None, entre=0.92):
    linhas = texto.split("\n")
    asc, desc = f.getmetrics()
    alt = int((asc + desc) * entre)
    for i, l in enumerate(linhas):
        larg = f.getlength(l)
        x = (W - larg) / 2
        yy = y + i * alt
        if sombra:
            d.text((x + 10, yy + 12), l, font=f, fill=sombra)
        d.text((x, yy), l, font=f, fill=cor)
    return y + len(linhas) * alt


def pilula(d, cx, y, texto, f, fundo, cor, pad=(34, 16)):
    larg = f.getlength(texto)
    asc, desc = f.getmetrics()
    caixa = (cx - larg / 2 - pad[0], y, cx + larg / 2 + pad[0], y + asc + desc + 2 * pad[1])
    d.rounded_rectangle(caixa, radius=(caixa[3] - caixa[1]) // 2, fill=fundo)
    d.text((cx - larg / 2, y + pad[1]), texto, font=f, fill=cor)
    return caixa[3]


def fundo_listras(semente=7, brilho=None):
    """Fundo do Universo do Piseiro: preto, listras diagonais em degradê laranja, poeira branca."""
    import random

    import numpy as np
    base = Image.new("RGB", (W, H), COR["noite"])
    # máscara de listras horizontais, girada
    big = Image.new("L", (int(W * 1.8), int(H * 1.4)), 0)
    db = ImageDraw.Draw(big)
    for y in range(0, big.height, 54):
        db.rectangle((0, y, big.width, y + 27), fill=255)
    big = big.rotate(9, resample=Image.BICUBIC)
    x0, y0 = (big.width - W) // 2, (big.height - H) // 2
    mask = np.asarray(big.crop((x0, y0, x0 + W, y0 + H)), dtype=np.float32) / 255
    # intensidade cresce para a direita e para baixo (como no banner)
    xx, yy = np.meshgrid(np.linspace(0, 1, W), np.linspace(0, 1, H))
    k = np.clip(0.95 * xx + 0.55 * yy - 0.35, 0, 1) ** 1.25
    c0, c1 = np.array(COR["vermelho"], np.float32), np.array(COR["sol"], np.float32)
    cor = c0[None, None, :] * (1 - k[..., None]) + c1[None, None, :] * k[..., None]
    alfa = (mask * k)[..., None]
    arr = np.asarray(base, np.float32) * (1 - alfa) + cor * alfa
    if brilho:  # halo quente atrás de um elemento (ex.: logo na vinheta)
        cx, cy, r = brilho
        dist = np.sqrt((xx * W - cx) ** 2 + (yy * H - cy) ** 2)
        g = np.clip(1 - dist / r, 0, 1) ** 2 * 0.55
        arr = arr * (1 - g[..., None]) + c1[None, None, :] * g[..., None]
    img = Image.fromarray(arr.clip(0, 255).astype("uint8"))
    # poeira / respingos brancos
    d = ImageDraw.Draw(img)
    rnd = random.Random(semente)
    for _ in range(140):
        x, y, r = rnd.randint(0, W), rnd.randint(0, H), rnd.choice([1, 1, 1, 2, 2, 3])
        v = rnd.randint(150, 255)
        d.ellipse((x - r, y - r, x + r, y + r), fill=(v, v, v))
    ruido = Image.effect_noise((W, H), 22).convert("RGB")
    return Image.blend(img, ruido, 0.035)


def fundo(centro_sol=(540, 1300), raios=True):
    if ESTILO == "listras":
        return fundo_listras(semente=centro_sol[1])
    img = Image.new("RGB", (W, H), COR["noite"])
    d = ImageDraw.Draw(img)
    for y in range(H):  # degradê noite
        k = y / H
        c = tuple(int(COR["noite"][i] * (1 - k) + COR["noite2"][i] * k) for i in range(3))
        d.line([(0, y), (W, y)], fill=c)
    if raios:  # sol do sertão
        camada = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        dc = ImageDraw.Draw(camada)
        import math
        cx, cy = centro_sol
        for i in range(24):
            if i % 2:
                continue
            a0, a1 = math.radians(i * 15), math.radians((i + 1) * 15)
            dc.polygon([(cx, cy), (cx + 3000 * math.cos(a0), cy + 3000 * math.sin(a0)),
                        (cx + 3000 * math.cos(a1), cy + 3000 * math.sin(a1))], fill=(255, 122, 26, 26))
        img = Image.alpha_composite(img.convert("RGBA"), camada).convert("RGB")
    # granulado leve
    ruido = Image.effect_noise((W, H), 18).convert("RGB")
    return Image.blend(img, ruido, 0.04)


def faixa_marca(d, img=None):
    if MOLDURA:  # a moldura oficial já traz logo e @; entra por cima no FFmpeg
        return
    d.rectangle((0, 0, W, 10), fill=COR["sol"])
    if LOGO and img is not None:
        colar_logo(img, W / 2, 110, altura=90)
    else:
        f = fonte(MONT, 34, 800)
        texto = "UNIVERSO DO PISEIRO  ·  NOTÍCIA DO FORRÓ"
        d.text(((W - f.getlength(texto)) / 2, 150), texto, font=f, fill=COR["amarelo"])
    # zigue-zague de xilogravura
    y = 210
    for x in range(110, 970, 40):
        d.line([(x, y), (x + 20, y + 14), (x + 40, y)], fill=COR["sol"], width=5)


def cena_vinheta(tela):
    if ESTILO == "listras" and LOGO:
        img = fundo_listras(semente=3, brilho=(540, 760, 620))
        d = ImageDraw.Draw(img)
        y = colar_logo(img, W / 2, 430, largura=780)
        titulo = tela["titulo"].replace("\n", " ") if len(tela["titulo"]) < 20 else tela["titulo"]
        f = caber(titulo, ANTON, 120, 900)
        texto_centro(d, y + 40, titulo, f, COR["creme"], sombra=COR["vermelho"])
        return img
    img = fundo(centro_sol=(540, 880))
    d = ImageDraw.Draw(img)
    d.ellipse((540 - 330, 880 - 330, 540 + 330, 880 + 330), fill=COR["sol"])
    f = caber(tela["titulo"], ANTON, 260, 900)
    y = texto_centro(d, 560, tela["titulo"], f, COR["creme"], sombra=COR["vermelho"])
    if LOGO:
        colar_logo(img, W / 2, y + 50, largura=520)
    else:
        pilula(d, W / 2, y + 60, tela["selo"], fonte(MONT, 44, 800), COR["amarelo"], COR["noite"])
    return img


def cena_manchete(tela):
    img = fundo()
    d = ImageDraw.Draw(img)
    faixa_marca(d, img)
    y = pilula(d, W / 2, 330, tela["chapeu"], fonte(MONT, 46, 800), COR["amarelo"], COR["noite"])
    f = caber(tela["titulo"], ANTON, 200, 880)
    y = texto_centro(d, y + 50, tela["titulo"], f, COR["creme"], sombra=COR["vermelho"])
    fr = fonte(MONT, 36, 600)
    d.text(((W - fr.getlength(tela["rodape"])) / 2, y + 50), tela["rodape"], font=fr, fill=COR["prata"])
    return img


PASTA_IMG = "."


def cena_podio(tela):
    if tela.get("foto"):
        return cena_podio_foto(tela)
    img = fundo()
    d = ImageDraw.Draw(img)
    faixa_marca(d, img)
    cor_pos = {"1º": COR["ouro"], "2º": COR["prata"], "3º": COR["bronze"]}[tela["posicao"]]
    numero = tela["posicao"].rstrip("º")
    fp = fonte(ANTON, 400)
    fo = fonte(MONT, 150, 900)  # o "º" da Anton parece um zero; usa o da Montserrat
    larg_n, larg_o = fp.getlength(numero), fo.getlength("º")
    x = (W - larg_n - larg_o) / 2
    d.text((x + 14, 242 + DESLOC), numero, font=fp, fill=COR["vermelho"])
    d.text((x, 230 + DESLOC), numero, font=fp, fill=cor_pos)
    d.text((x + larg_n + 6, 300 + DESLOC), "º", font=fo, fill=cor_pos)
    musica = "“" + tela["musica"] + "”"
    f = caber(musica, ANTON, 120, 860)
    y = texto_centro(d, 800 + DESLOC // 2, musica, f, COR["creme"], sombra=COR["vermelho"])
    fa = caber(tela["artista"], MONT, 58, 860, 800)
    d.text(((W - fa.getlength(tela["artista"])) / 2, y + 30), tela["artista"], font=fa, fill=COR["amarelo"])
    pilula(d, W / 2, y + 130, tela["extra"], fonte(MONT, 40, 700), COR["noite"], COR["amarelo"])
    return img


def cena_podio_foto(tela):
    """Pódio com foto oficial do artista recortada: posição + música no topo, artista embaixo."""
    img = fundo(centro_sol=(540, 1050))
    d = ImageDraw.Draw(img)
    faixa_marca(d, img)
    cor_pos = {"1º": COR["ouro"], "2º": COR["prata"], "3º": COR["bronze"]}[tela["posicao"]]
    d.ellipse((540 - 360, 1050 - 360, 540 + 360, 1050 + 360), fill=COR["sol"])
    # foto recortada, base em y=1400, dentro de 900x760
    nome = os.path.splitext(os.path.basename(tela["foto"]))[0]
    rec = recortar(tela["foto"], os.path.join(PASTA_IMG, f"recorte_{nome}.png"))
    esc = min(900 / rec.width, 760 / rec.height)
    rec = rec.resize((int(rec.width * esc), int(rec.height * esc)), Image.LANCZOS)
    img.paste(rec, (int((W - rec.width) / 2), 1400 - rec.height), rec)
    # degradê para a foto "assentar" no fundo
    deg = Image.new("RGBA", (W, 220), (0, 0, 0, 0))
    dg = ImageDraw.Draw(deg)
    for i in range(220):
        dg.line([(0, i), (W, i)], fill=COR["noite2"] + (int(255 * i / 220),))
    img.paste(deg, (0, 1260), deg)
    d = ImageDraw.Draw(img)
    # posição + música
    numero = tela["posicao"].rstrip("º")
    fp, fo = fonte(ANTON, 230), fonte(MONT, 90, 900)
    larg_n = fp.getlength(numero)
    d.text((110 + 10, 262 + DESLOC), numero, font=fp, fill=COR["vermelho"])
    d.text((110, 252 + DESLOC), numero, font=fp, fill=cor_pos)
    d.text((110 + larg_n + 4, 290 + DESLOC), "º", font=fo, fill=cor_pos)
    musica = "“" + tela["musica"].replace("\n", " ") + "”"
    x0 = 110 + larg_n + 90
    fm = caber(musica, ANTON, 96, 970 - x0)
    if fm.size < 70:  # título longo: quebra em duas linhas
        musica = "“" + tela["musica"] + "”"
        fm = caber(musica, ANTON, 96, 970 - x0)
    asc, desc = fm.getmetrics()
    for i, linha in enumerate(musica.split("\n")):
        d.text((x0, 300 + DESLOC + i * int((asc + desc) * 0.9)), linha, font=fm, fill=COR["creme"])
    # artista e dado extra sobre a base da foto
    fa = caber(tela["artista"], MONT, 56, 860, 800)
    y = pilula(d, W / 2, 1300, tela["artista"], fa, COR["amarelo"], COR["noite"])
    pilula(d, W / 2, y + 14, tela["extra"], fonte(MONT, 36, 700), COR["noite"], COR["amarelo"], pad=(26, 10))
    return img


def cena_lista(tela):
    img = fundo()
    d = ImageDraw.Draw(img)
    faixa_marca(d, img)
    y = pilula(d, W / 2, 300 + DESLOC // 2, tela["chapeu"], fonte(MONT, 46, 800), COR["amarelo"], COR["noite"])
    f = caber(tela["titulo"], ANTON, 190, 880)
    y = texto_centro(d, y + 40, tela["titulo"], f, COR["creme"], sombra=COR["vermelho"]) + 40
    fi = fonte(MONT, 44, 700)
    for item in tela["itens"]:
        d.rounded_rectangle((110, y, 970, y + 100), radius=22, fill=COR["creme"])
        d.rectangle((110, y, 132, y + 100), fill=COR["sol"])
        fit = caber(item, MONT, 44, 780, 700)
        d.text((160, y + 26), item, font=fit, fill=COR["noite"])
        y += 124
    return img


def cena_cta(tela):
    img = fundo(centro_sol=(540, 1500))
    d = ImageDraw.Draw(img)
    faixa_marca(d, img)
    f = caber(tela["titulo"], ANTON, 190, 880)
    y = texto_centro(d, 380, tela["titulo"], f, COR["creme"], sombra=COR["vermelho"])
    fs = fonte(MONT, 54, 700)
    d.text(((W - fs.getlength(tela["sub"])) / 2, y + 30), tela["sub"], font=fs, fill=COR["amarelo"])
    fb = caber(tela["cta"], MONT, 50, 760, 800)
    larg = fb.getlength(tela["cta"])
    caixa = (W / 2 - larg / 2 - 50, y + 170, W / 2 + larg / 2 + 50, y + 300)
    d.rounded_rectangle(caixa, radius=30, fill=COR["sol"], outline=COR["creme"], width=4)
    d.text((W / 2 - larg / 2, y + 206), tela["cta"], font=fb, fill=COR["creme"])
    return img


CENAS = {"vinheta": cena_vinheta, "manchete": cena_manchete, "podio": cena_podio,
         "lista": cena_lista, "cta": cena_cta}


def ts(seg, srt=False):
    h, r = divmod(seg, 3600)
    m, s = divmod(r, 60)
    if srt:
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s % 1) * 1000)):03d}"
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def blocos_legenda(texto, max_palavras=3, max_chars=18):
    palavras = texto.split()
    pedacos, atual = [], []
    for p in palavras:
        atual.append(p)
        junto = " ".join(atual)
        if len(atual) >= max_palavras or len(junto) >= max_chars or re.search(r"[.,!?:]$", p):
            pedacos.append(junto)
            atual = []
    if atual:
        pedacos.append(" ".join(atual))
    return pedacos


def legendas(rot, inicios, dur, build):
    pasta = os.path.join(build, "04_legendas")
    os.makedirs(pasta, exist_ok=True)
    cab = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Leg,{FONTE_LEG},88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,0,0,0,0,100,100,1,0,1,8,4,2,120,120,340,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    eventos, srt, n = [], [], 1
    for b in rot["blocos"]:
        if b["cena"] == "vinheta":
            continue
        pedacos = blocos_legenda(b.get("legenda") or b["narracao"])
        pesos = [len(p) + 2 for p in pedacos]
        total = sum(pesos)
        t = inicios[b["id"]]
        for p, w in zip(pedacos, pesos):
            fim = t + dur[b["id"]] * w / total
            txt = p.upper().replace("HOT CEM", "HOT 100").replace("TOP DEZ", "TOP 10").rstrip(",:")
            pop = r"{\fscx80\fscy80\t(0,110,\fscx108\fscy108)\t(110,200,\fscx100\fscy100)}"
            eventos.append(f"Dialogue: 0,{ts(t)},{ts(fim)},Leg,,0,0,0,,{pop}{txt}")
            srt.append(f"{n}\n{ts(t, True)} --> {ts(fim, True)}\n{p.replace('Hot cem', 'Hot 100').replace('top dez', 'top 10')}\n")
            n += 1
            t = fim
    open(os.path.join(pasta, "legenda.ass"), "w", encoding="utf-8").write(cab + "\n".join(eventos) + "\n")
    open(os.path.join(pasta, "legenda.srt"), "w", encoding="utf-8").write("\n".join(srt))
    return os.path.join(pasta, "legenda.ass")


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(" ".join(cmd)[:500])
        print(r.stderr[-2500:])
        raise SystemExit(1)


def main(roteiro_path, build):
    global PASTA_IMG
    rot = json.load(open(roteiro_path, encoding="utf-8"))
    base_rot = os.path.dirname(os.path.abspath(roteiro_path))
    carregar_marca(rot.get("marca") or os.path.join(base_rot, "marca.json"))
    os.makedirs(os.path.join(build, "01_audio"), exist_ok=True)
    dur = json.load(open(os.path.join(build, "01_audio", "duracoes.json")))
    pasta_img = os.path.join(build, "03_imagens")
    PASTA_IMG = pasta_img
    pasta_vid = os.path.join(build, "02_video")
    os.makedirs(pasta_img, exist_ok=True)
    os.makedirs(pasta_vid, exist_ok=True)

    # 1) tempos de cena: cada cena cobre a fala do bloco + transições
    blocos = rot["blocos"]
    dcena, inicios, offsets = [], {}, []
    for i, b in enumerate(blocos):
        if i == 0:
            d = max(2.3, 0.35 + dur[b["id"]] + 0.25 + T)
        else:
            d = dur[b["id"]] + 2 * T + 0.35
        if i == len(blocos) - 1:
            d += 1.6  # respiro no card final
        if b.get("musica"):
            d += b["musica"].get("destaque", 2.5)  # janela em que a música sobe depois da fala
        dcena.append(round(d, 3))
    acumulado = 0.0
    for i, b in enumerate(blocos):
        if i == 0:
            offsets.append(0.0)
            inicios[b["id"]] = 0.35
        else:
            acumulado += dcena[i - 1] - T
            offsets.append(acumulado)
            inicios[b["id"]] = acumulado + T + 0.05
    total = offsets[-1] + dcena[-1]
    print(f"duração total: {total:.2f}s")

    # 2) imagens e clipes com movimento
    clipes = []
    for i, b in enumerate(blocos):
        img = CENAS[b["cena"]](b["tela"])
        png = os.path.join(pasta_img, f"{b['id']}_{b['cena']}.png")
        img.save(png)
        frames = int(round(dcena[i] * FPS))
        if b["cena"] == "vinheta":
            z = "if(lte(on,8),1.30-0.0375*on,1.0+0.0004*(on-8))"
        else:
            z = f"1.0+0.07*on/{frames}"
        mp4 = os.path.join(pasta_vid, f"V{i + 1:02d}_{b['cena']}.mp4")
        run(["ffmpeg", "-y", "-loop", "1", "-i", png, "-vf",
             f"scale=2160:3840,zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s={W}x{H}:fps={FPS},format=yuv420p",
             "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast", "-crf", "16", mp4])
        clipes.append(mp4)

    # 3) encadear com transições
    entradas, filtro, ultimo = [], [], "[0:v]"
    for c in clipes:
        entradas += ["-i", c]
    transicoes = ["smoothleft", "smoothleft", "slideup", "slideup", "smoothleft", "fade"]
    for i in range(1, len(clipes)):
        saida = f"[x{i}]"
        filtro.append(f"{ultimo}[{i}:v]xfade=transition={transicoes[(i - 1) % len(transicoes)]}:duration={T}:offset={offsets[i]:.3f}{saida}")
        ultimo = saida
    ass = legendas(rot, inicios, dur, build)
    if MOLDURA:  # moldura oficial por cima de tudo, a partir da 2ª cena (a vinheta já tem o logo grande)
        entradas += ["-loop", "1", "-i", MOLDURA]
        idx = len(clipes)
        filtro.append(f"[{idx}:v]scale={W}:{H},format=rgba[mold]")
        filtro.append(f"{ultimo}[mold]overlay=0:0:shortest=1:enable='gte(t,{offsets[1] + T:.2f})'[comMold]")
        ultimo = "[comMold]"
    filtro.append(f"{ultimo}ass={ass}:fontsdir={ASS_FONT_DIR}[v]")

    # 4) áudio: narrações nos tempos + trilha baixa
    trilha = os.path.join(build, "01_audio", "trilha_baiao.wav")
    trilha_baiao(total, trilha)
    base = len(clipes) + (1 if MOLDURA else 0)
    entradas += ["-i", trilha]
    for b in blocos:
        entradas += ["-i", os.path.join(build, "01_audio", f"{b['id']}.wav")]
    rotulos = []
    for j, b in enumerate(blocos):
        ms = int(inicios[b["id"]] * 1000)
        filtro.append(f"[{base + 1 + j}:a]aresample=44100,adelay={ms}|{ms},apad[n{j}]")
        rotulos.append(f"[n{j}]")
    filtro.append(f"{''.join(rotulos)}amix=inputs={len(rotulos)}:normalize=0,atrim=0:{total:.3f}[voz]")

    # trechos de música (só arquivos autorizados): baixos sob a fala, sobem no destaque
    janelas, musicas = [], []
    prox = base + 1 + len(blocos)
    for i, b in enumerate(blocos):
        m = b.get("musica")
        if not m:
            continue
        entradas += ["-i", m["arquivo"]]
        ini, fim = offsets[i], offsets[i] + dcena[i]
        janelas.append((ini, fim))
        fala_fim = inicios[b["id"]] - ini + dur[b["id"]]
        lg = dcena[i]
        ms = int(ini * 1000)
        filtro.append(
            f"[{prox}:a]aresample=44100,atrim={m.get('inicio', 0)}:{m.get('inicio', 0) + lg:.3f},asetpts=PTS-STARTPTS,"
            f"volume='if(lt(t,{fala_fim:.2f}),{m.get('vol_fala', 0.22)},{m.get('vol_destaque', 0.9)})':eval=frame,"
            f"afade=t=in:d=0.15,afade=t=out:st={lg - 0.35:.2f}:d=0.35,adelay={ms}|{ms},apad[m{prox}]")
        musicas.append(f"[m{prox}]")
        prox += 1
    # trilha de baião some nas janelas de música
    corte = "".join(f"*(1-between(t,{a:.2f},{b:.2f}))" for a, b in janelas)
    filtro.append(f"[{base}:a]volume='0.16{corte}':eval=frame[bg]")
    camadas = ["[voz]", "[bg]"] + musicas
    filtro.append(f"{''.join(camadas)}amix=inputs={len(camadas)}:normalize=0,atrim=0:{total:.3f},"
                  "loudnorm=I=-14:TP=-1.5:LRA=11[a]")

    saida = os.path.join(build, f"{rot['slug']}.mp4")
    run(["ffmpeg", "-y", *entradas, "-filter_complex", ";".join(filtro), "-map", "[v]", "-map", "[a]",
         "-t", f"{total:.3f}", "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "19",
         "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "44100", "-movflags", "+faststart", saida])
    json.dump({"duracao_total": total, "cenas": dict(zip([b["id"] for b in blocos], dcena)),
               "inicio_narracao": inicios}, open(os.path.join(build, "timeline.json"), "w"), indent=2)
    print("ok:", saida)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
