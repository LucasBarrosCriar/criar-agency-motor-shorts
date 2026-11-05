"""Gera o logo e a moldura PROVISÓRIOS do Universo dos Clips (até o Brand Kit oficial chegar).

Uso: python3 marcas/universo-dos-clips/gerar_assets.py
Saída: logo.png (transparente) e moldura.png (1080x1920 transparente) nesta pasta.
Quando o Brand Kit do Magnific estiver pronto, basta substituir os dois PNGs com o mesmo nome.
"""
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
ANTON = os.path.join(AQUI, "fontes", "Anton-Regular.ttf")
MONT = os.path.join(AQUI, "fontes", "Montserrat-VF.ttf")
LARANJA, ROSA, ROXO, CREME = (232, 80, 30), (255, 62, 165), (155, 61, 255), (247, 243, 255)


def fonte(c, t, peso=None):
    f = ImageFont.truetype(c, t)
    if peso:
        try:
            f.set_variation_by_axes([peso])
        except Exception:
            pass
    return f


def degrade(w, h, cores):
    """Degradê horizontal passando pelas cores dadas."""
    xs = np.linspace(0, 1, w)
    seg = len(cores) - 1
    out = np.zeros((h, w, 3), np.float32)
    for i, x in enumerate(xs):
        p = min(int(x * seg), seg - 1)
        k = x * seg - p
        c = np.array(cores[p]) * (1 - k) + np.array(cores[p + 1]) * k
        out[:, i] = c
    return Image.fromarray(out.astype("uint8"))


def texto_degrade(texto, f, cores, pad=30):
    larg = int(f.getlength(texto)) + 2 * pad
    asc, desc = f.getmetrics()
    alt = asc + desc + 2 * pad
    mask = Image.new("L", (larg, alt), 0)
    ImageDraw.Draw(mask).text((pad, pad), texto, font=f, fill=255)
    cor = degrade(larg, alt, cores).convert("RGBA")
    cor.putalpha(mask)
    return cor, mask


def neon(camada, cor, raio=18, forca=1.6):
    """Brilho neon atrás de uma camada RGBA."""
    a = camada.split()[-1].filter(ImageFilter.GaussianBlur(raio))
    a = a.point(lambda v: min(255, int(v * forca)))
    glow = Image.new("RGBA", camada.size, cor + (0,))
    glow.putalpha(a)
    out = Image.new("RGBA", camada.size, (0, 0, 0, 0))
    out.alpha_composite(glow)
    out.alpha_composite(camada)
    return out


def logo():
    fc = fonte(ANTON, 230)
    cam, _ = texto_degrade("DOS CLIPS", fc, [LARANJA, ROSA, ROXO], pad=10)
    W, H = cam.width + 260, cam.height + 220
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    x = 180  # espaço à esquerda para o botão play
    # "UNIVERSO" pequeno e espaçado, alinhado ao bloco "DOS CLIPS"
    fu = fonte(MONT, 60, 800)
    txt = "U N I V E R S O"
    ImageDraw.Draw(img).text((x + (cam.width - fu.getlength(txt)) / 2, 40), txt, font=fu, fill=CREME)
    camada = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    camada.alpha_composite(cam, (x, 110))
    # botão play à esquerda da palavra
    cy = 110 + cam.height // 2 + 10
    ImageDraw.Draw(camada).polygon([(x - 120, cy - 60), (x - 120, cy + 60), (x - 25, cy)], fill=LARANJA + (255,))
    # sublinhado neon
    yb = 110 + cam.height - 45
    ImageDraw.Draw(camada).rounded_rectangle((x + 10, yb, x + cam.width - 10, yb + 16), radius=8, fill=ROSA + (255,))
    img.alpha_composite(neon(camada, ROSA, raio=22, forca=0.9))
    img = img.crop(img.getbbox())
    img.save(os.path.join(AQUI, "logo.png"))
    return img


def moldura(lg):
    W, H = 1080, 1920
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # logo pequeno no topo
    l = lg.resize((300, int(lg.height * 300 / lg.width)), Image.LANCZOS)
    img.alpha_composite(l, ((W - l.width) // 2, 70))
    # @ no rodapé, com fundo translúcido
    fa = fonte(MONT, 44, 800)
    at = "@UNIVERSODOSCLIPS"
    larg = fa.getlength(at)
    d = ImageDraw.Draw(img)
    y = 1745
    d.rounded_rectangle(((W - larg) / 2 - 34, y - 12, (W + larg) / 2 + 34, y + 66), radius=39, fill=(10, 8, 18, 170),
                        outline=ROSA + (255,), width=3)
    d.text(((W - larg) / 2, y), at, font=fa, fill=CREME)
    img.save(os.path.join(AQUI, "moldura.png"))


if __name__ == "__main__":
    moldura(logo())
    print("logo.png e moldura.png gerados em", AQUI)
