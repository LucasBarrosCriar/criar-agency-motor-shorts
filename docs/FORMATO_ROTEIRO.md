# Formato do roteiro (`roteiro.json`)

Cada Short é um arquivo JSON. O motor lê os blocos em ordem: cada bloco vira uma cena com a sua narração.

## Campos do roteiro

| Campo | Obrigatório | O que é |
|---|---|---|
| `slug` | sim | Nome do vídeo e da pasta de saída. Padrão: `AAAA-MM-DD_SHORT_formato_tema` |
| `titulo_interno` | não | Nome legível do vídeo |
| `marca` | sim | Pasta em `marcas/` (ex.: `universo-do-piseiro`) ou caminho de um `marca.json` |
| `voz` | não | Voz do Kokoro. pt-BR: `pm_alex`, `pm_santa`, `pf_dora`. Se vazio, usa a `voz` do `marca.json` (Piseiro: `pm_alex`; Clips: `pm_santa`) |
| `velocidade` | não | Velocidade da fala. Padrão `1.0`; o piloto usou `1.08` |
| `fontes` | sim | Lista de `{fato, url}`. Sem fonte, o fato não entra no roteiro |
| `seo` | não | `titulos` (3), `descricao`, `tags`, `comentario_fixado`, `video_relacionado` → vira o `SEO.txt` |
| `blocos` | sim | Lista de cenas (abaixo) |

## Campos de cada bloco

| Campo | O que é |
|---|---|
| `id` | `N01`, `N02`… (também nomeia o áudio da narração) |
| `cena` | Tipo de cena: `vinheta`, `manchete`, `podio`, `lista`, `cta` |
| `narracao` | Texto exato que a voz lê. Escreva como se fala: números por extenso ("doze de dezembro"), "Hot cem" em vez de "Hot 100" |
| `legenda` | Opcional. Texto da legenda quando a narração usa grafia fonética (ex.: narração "fór ól", legenda "for all"). Se vazio, a legenda usa a própria narração |
| `tela` | Textos que aparecem na cena (campos abaixo) |
| `musica` | Opcional. Só com faixa **autorizada**: `{arquivo, inicio, destaque, vol_fala, vol_destaque}` |

## Campos de `tela` por cena

- **vinheta**: `titulo` (use `\n` para quebrar linha), `selo`
- **manchete**: `chapeu`, `titulo`, `rodape` (a fonte da notícia)
- **podio**: `posicao` (`1º`, `2º`, `3º`), `musica`, `artista`, `extra`, `foto` (opcional: caminho da foto **oficial** do artista; o fundo é removido sozinho)
- **lista**: `chapeu`, `titulo`, `itens` (até 3)
- **cta**: `titulo`, `sub`, `cta`
- **imagem**: `chapeu`, `titulo`, `credito`, `imagem` (opcional), `descricao`. Mostra uma imagem oficial (screenshot, frame autorizado) num quadro de 900x560 abaixo do título. Sem `imagem`, o motor procura `imagens/<slug>_<id>.jpg|png` ao lado do roteiro; se não achar, desenha o quadro com a `descricao` para o editor encaixar a imagem no CapCut (a posição do quadro sai em `timeline.json`, campo `quadros_imagem_px`).

## Regras editoriais (vêm da skill de pauta do canal)

- Só fato público, verificável e com fonte. Boato vira "circula nas redes que…".
- Nunca gerar rosto ou voz de artista real com IA. Foto só oficial, enviada pela equipe ou pela assessoria.
- Música de artista só com repertório autorizado. Sem autorização, o Short vai sem a faixa (a trilha de baião do motor entra no lugar).
- Datas relativas ("nesta quinta") vencem. Prefira a data ("quinta, dia 29").

## Marcas

| Marca | Pasta | Fundo | Trilha | Voz padrão |
|---|---|---|---|---|
| Universo do Piseiro | `universo-do-piseiro` | `listras` | `baiao` | `pm_alex` |
| Universo dos Clips | `universo-dos-clips` | `neon` | `synth` | `pm_santa` (1,1) |

Campos do `marca.json` além de cores, fontes, logo e moldura: `estilo_fundo` (`sol`, `listras`, `neon`), `trilha` (`baiao`, `synth`), `assinatura` (texto da faixa quando não há logo nem moldura), `voz` e `velocidade` padrão.
