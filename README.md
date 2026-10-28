# Motor de Shorts — Criar Agency

Gera Shorts narrados (9:16, 1080x1920, 30 fps) a partir de um roteiro em JSON: narração com voz aberta em pt-BR, cenas no padrão visual da marca, legenda dinâmica, trilha própria, transições e exportação. Feito para o **Universo do Piseiro** (Notícia do Forró, Top 10, Universo Explica) e pronto para os canais irmãos: basta criar uma pasta nova em `marcas/`.

## Como usar

```bash
bash setup.sh                                      # 1x por máquina: dependências e modelos abertos
python3 motor/gerar.py roteiros/exemplos/2026-10-27_noticia-do-forro.json saida/
python3 motor/gerar.py "roteiros/2026-11-03/*.json" saida/    # a semana inteira de uma vez
```

Cada Short sai em `saida/<slug>/` com:

- `<slug>.mp4`: o vídeo final, com legenda queimada
- `04_legendas/legenda.srt`: legenda para subir à parte, se quiser
- `03_imagens/`: as cenas em PNG
- `SEO.txt`: títulos, descrição com fontes, tags e comentário fixado

## Estrutura

```
motor/          audio.py (narração + trilha), render.py (cenas, legenda, montagem), gerar.py (tudo junto)
marcas/         uma pasta por marca: marca.json + logo + moldura + fontes
roteiros/       roteiros dos Shorts (exemplos/ tem o piloto)
docs/           FORMATO_ROTEIRO.md e o guia de templates para o design
```

## Marca

`marcas/<nome>/marca.json` define cores, fontes, logo, moldura e estilo de fundo. Caminhos relativos à própria pasta da marca. Trocar o visual de todos os Shorts = editar esse arquivo.

Os templates desenhados no Photoshop (ver `docs/Guia_Templates_Shorts_Universo_do_Piseiro.docx`) entram em `marcas/<nome>/templates/` quando estiverem prontos.

## Ferramentas e licenças

| Peça | Projeto | Licença |
|---|---|---|
| Voz pt-BR | Kokoro (kokoro-onnx) | Apache 2.0 |
| Recorte de fundo das fotos | rembg (modelo isnet-general-use) | MIT |
| Montagem | FFmpeg + libass | LGPL/GPL |
| Fontes | Alfa Slab One, Zilla Slab, Anton, Montserrat | SIL OFL 1.1 (licenças em cada pasta de fontes) |
| Trilha | Baião sintetizado pelo próprio motor | sem amostras de terceiros |

Verifique as licenças de novas fontes antes de usar em canal monetizado.

## Regras do canal

Ver `docs/FORMATO_ROTEIRO.md`. Resumo: só fato com fonte; foto de artista só oficial; nenhum rosto ou voz de artista gerado por IA; música só de repertório autorizado.
