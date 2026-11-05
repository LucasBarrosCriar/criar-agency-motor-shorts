"""Série "Detalhes que ninguém viu" (GTA 6) — Universo dos Clips. Gera um roteiro.json por Short.

Uso: python3 roteiros/universo-dos-clips/gerar_roteiros_gta6.py
Saída: roteiros/universo-dos-clips/2026-11-07/ ... 2026-11-11/ (3 Shorts por dia, na ordem de publicação)
Fatos conferidos na web em 05/11/2026. Fonte de cada fato no campo "fontes".
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
CRED = "Imagem: Rockstar Games"

F = {
    "vice_galeria": ("Rockstar soltou 39 screenshots novos antes do lançamento (05/11/2026)",
                     "https://www.vice.com/en/article/gta-6-38-new-screenshots-before-launch/"),
    "pcg_galeria": ("Detalhes da Launch Gallery: Vice City à noite, cachorro com equipamento de combate, poros, personagens 'Florida Man', jacaré, mergulho, Jason saindo de avião militar (05/11/2026)",
                    "https://www.pcgamer.com/games/grand-theft-auto/rockstar-drops-a-pile-of-new-gta-6-launch-screenshots-featuring-dancers-combat-dogs-and-so-many-pores/"),
    "ri_galeria": ("'The Launch Gallery': Vice City, Grassrivers, Leonida Keys, Port Gellhorn; assalto que parece ser em shopping; fuga de moto; possivelmente a última leva antes de 19/11 (05/11/2026)",
                   "https://rockstarintel.com/39-new-gta-6-screenshots-released-for-launch/"),
    "vgc_preload": ("Pré-load PS5 10/11 0h local; Xbox 10/11 0h GMT; código na caixa a partir de 12/11; até 212 GB; pôster e mapa de Leonida grátis no lançamento; pôster físico US$ 0,99 (03/11/2026)",
                    "https://www.videogameschronicle.com/news/rockstar-details-grand-theft-auto-6-pre-load-date-and-time-and-file-size/"),
    "vice_horario": ("Lançamento à meia-noite no horário local; Nova Zelândia primeiro; PS5 exige 212 GB livres; pré-load não libera antes (03/11/2026)",
                     "https://www.vice.com/en/article/gta-6-midnight-release-times-file-size-preload/"),
    "ch_preco": ("Brasil: padrão R$ 449,90; Ultimate R$ 549,90; upgrade R$ 100; caixa física só com código; bônus Vice City Vintage (25/06/2026)",
                 "https://criticalhits.com.br/games/preco-de-gta-6-no-brasil-e-confirmado-com-a-pre-venda-veja-os-valores/"),
    "mp1st_bios": ("Bios oficiais dos personagens e regiões de Leonida (06/05/2025)",
                   "https://mp1st.com/news/gta-6-character-bios-screenshots-locations"),
    "justice": ("Trilha original do Justice: 11/12, 30 faixas, CD e vinil; 'Pusher' com Gesaffelstein (29/10/2026)",
                "https://www.gamerfuzion.com/gta-6-original-score-justice-album-december-11-pusher-gesaffelstein/"),
    "justice2": ("Justice e Gesaffelstein lançam 'Pusher' antes do álbum da trilha",
                 "https://www.beatportal.com/articles/1705765-justice-tap-gesaffelstein-for-first-collab-pusher-ahead-of-gta-vi-score-album"),
}


def fontes(*chaves):
    return [{"fato": F[c][0], "url": F[c][1]} for c in chaves]


def b(id_, cena, narracao, tela, legenda=None):
    bloco = {"id": id_, "cena": cena, "narracao": narracao, "tela": tela}
    if legenda:
        bloco["legenda"] = legenda
    return bloco


def vinheta(n):
    return b("N01", "vinheta", "Detalhes que ninguém viu. GTA seis!",
             {"titulo": f"DETALHES QUE\nNINGUÉM VIU #{n}", "selo": "GTA 6"},
             legenda="Detalhes que ninguém viu. GTA 6!")


def cta(narr, titulo, sub, botao="COMENTA AÍ", legenda=None):
    return b("N05", "cta", narr, {"titulo": titulo, "sub": sub, "cta": botao}, legenda)


SHORTS = [
    # ---------------- 07/11 ----------------
    dict(data="2026-11-07", tema="39-imagens-novas", titulo_interno="39 imagens novas da Launch Gallery",
         fontes=fontes("vice_galeria", "ri_galeria", "pcg_galeria"),
         titulos=["GTA 6: 39 IMAGENS NOVAS 🔥 o que a Rockstar mostrou", "GTA 6 SOLTOU A LAUNCH GALLERY 😱", "GTA 6: A ÚLTIMA LEVA ANTES DO DIA 19? 👀"],
         tags=["gta 6", "gta 6 imagens novas", "gta 6 launch gallery", "gta 6 screenshots", "gta vi", "vice city", "leonida"],
         fixado="Qual imagem nova te chamou mais atenção? 👇 Amanhã tem mais detalhe da série.",
         blocos=lambda: [
             vinheta(1),
             b("N02", "manchete", "A Rockstar soltou trinta e nove imagens novas do GTA seis. E tem coisa ali que quase ninguém reparou.",
               {"chapeu": "LAUNCH GALLERY", "titulo": "39 IMAGENS\nNOVAS", "rodape": "Rockstar Games · 05/11/2026"},
               "A Rockstar soltou 39 imagens novas do GTA 6. E tem coisa ali que quase ninguém reparou."),
             b("N03", "imagem", "O nome é Launch Gallery. E pode ser a última leva de imagens antes do lançamento, no dia dezenove de novembro.",
               {"chapeu": "ÚLTIMA LEVA?", "titulo": "ANTES DO DIA 19", "descricao": "Screenshot oficial da Launch Gallery\n(Jason e Lucia)", "credito": CRED},
               "O nome é Launch Gallery. E pode ser a última leva de imagens antes do lançamento, no dia 19 de novembro."),
             b("N04", "lista", "Tem Vice City de noite, os Grassrivers, Leonida Keys e Port Gellhorn. Tem até assalto e fuga de moto.",
               {"chapeu": "O QUE APARECE", "titulo": "4 REGIÕES", "itens": ["Vice City à noite", "Grassrivers e Keys", "Port Gellhorn"]}),
             cta("Na série Detalhes que ninguém viu, eu te mostro tudo, um por um. Segue o canal pra não perder!",
                 "SÉRIE\nCOMPLETA", "Detalhes que ninguém viu", "SEGUE O CANAL"),
         ]),
    dict(data="2026-11-07", tema="pre-load", titulo_interno="Datas do pré-load",
         fontes=fontes("vgc_preload", "vice_horario"),
         titulos=["GTA 6: PRÉ-LOAD COMEÇA DIA 10 ⏳ anota o horário", "GTA 6: QUANDO BAIXAR NO PS5 E NO XBOX 🎮", "GTA 6: DÁ PRA BAIXAR ANTES? ⬇️"],
         tags=["gta 6", "gta 6 pre load", "gta 6 pré-load", "gta 6 ps5", "gta 6 xbox", "gta 6 lançamento", "gta vi"],
         fixado="Tu comprou digital ou física? 👇",
         blocos=lambda: [
             vinheta(2),
             b("N02", "manchete", "Anota aí: o pré-load do GTA seis começa dia dez de novembro.",
               {"chapeu": "PRÉ-LOAD", "titulo": "DIA 10/11", "rodape": "Fonte: VGC · 03/11/2026"},
               "Anota aí: o pré-load do GTA 6 começa dia 10 de novembro."),
             b("N03", "lista", "No PS cinco, à meia-noite do teu horário. No Xbox, à meia-noite de Londres, que é nove da noite do dia nove no horário de Brasília.",
               {"chapeu": "HORÁRIOS", "titulo": "PS5 E XBOX", "itens": ["PS5: 10/11, 0h local", "Xbox: 9/11, 21h Brasília", "Caixa: código a partir de 12/11"]},
               "No PS5, à meia-noite do teu horário. No Xbox, à meia-noite de Londres, que é 9 da noite do dia 9 no horário de Brasília."),
             b("N04", "manchete", "É pra quem comprou digital. E baixar antes não libera o jogo mais cedo, viu?",
               {"chapeu": "IMPORTANTE", "titulo": "NÃO LIBERA\nANTES", "rodape": "Fonte: VICE · 03/11/2026"}),
             cta("Tu vai baixar no primeiro minuto? Comenta aí!", "E AÍ?", "Vai baixar no primeiro minuto?"),
         ]),
    dict(data="2026-11-07", tema="preco-brasil", titulo_interno="Preço no Brasil",
         fontes=fontes("ch_preco"),
         titulos=["GTA 6: QUANTO CUSTA NO BRASIL? 💸", "GTA 6 POR R$ 449,90 🤯 e a caixa vem sem disco", "GTA 6: PADRÃO OU ULTIMATE? 💰"],
         tags=["gta 6", "gta 6 preço", "gta 6 preço brasil", "gta 6 ultimate", "gta 6 pré-venda", "gta vi"],
         fixado="Caro ou justo? 👇 (Preço da pré-venda; confere a loja do teu console, pode ter promoção.)",
         blocos=lambda: [
             vinheta(3),
             b("N02", "manchete", "Quanto custa o GTA seis no Brasil?",
               {"chapeu": "PREÇO NO BRASIL", "titulo": "R$ 449,90", "rodape": "Pré-venda · PS Store e Xbox Store"},
               "Quanto custa o GTA 6 no Brasil?"),
             b("N03", "lista", "A edição padrão sai por quatrocentos e quarenta e nove e noventa. A Ultimate, quinhentos e quarenta e nove e noventa. E dá pra fazer o upgrade depois por cem reais.",
               {"chapeu": "EDIÇÕES", "titulo": "PADRÃO X ULTIMATE", "itens": ["Padrão: R$ 449,90", "Ultimate: R$ 549,90", "Upgrade: R$ 100"]},
               "A edição padrão sai por R$ 449,90. A Ultimate, R$ 549,90. E dá pra fazer o upgrade depois por R$ 100."),
             b("N04", "manchete", "E presta atenção: a versão física vem só com um código de download. Não tem disco na caixa.",
               {"chapeu": "ATENÇÃO", "titulo": "SEM DISCO\nNA CAIXA", "rodape": "Fonte: Critical Hits · 25/06/2026"}),
             cta("Achou caro ou justo? Comenta aí!", "CARO OU\nJUSTO?", "Comenta o que tu achou"),
         ]),
    # ---------------- 08/11 ----------------
    dict(data="2026-11-08", tema="212-gb", titulo_interno="212 GB de espaço",
         fontes=fontes("vice_horario", "vgc_preload"),
         titulos=["GTA 6 PEDE 212 GB 😳 teu console aguenta?", "GTA 6: LIBERA ESPAÇO AGORA 💾", "GTA 6: O TAMANHO DO JOGO ASSUSTA 😱"],
         tags=["gta 6", "gta 6 tamanho", "gta 6 212 gb", "gta 6 ps5", "gta 6 espaço", "gta vi"],
         fixado="Quanto espaço livre tu tem hoje? 👇",
         blocos=lambda: [
             vinheta(4),
             b("N02", "manchete", "Prepara o console: o GTA seis pede até duzentos e doze gigas.",
               {"chapeu": "ATENÇÃO", "titulo": "212 GB", "rodape": "Fonte: VGC e VICE · 03/11/2026"},
               "Prepara o console: o GTA 6 pede até 212 GB."),
             b("N03", "manchete", "No PS cinco, esse é o espaço livre que precisa ter, segundo o blog oficial da PlayStation.",
               {"chapeu": "PS5", "titulo": "ESPAÇO\nLIVRE", "rodape": "PlayStation Blog, citado pela VICE"},
               "No PS5, esse é o espaço livre que precisa ter, segundo o blog oficial da PlayStation."),
             b("N04", "lista", "Console apertado? Confere o espaço, apaga o que tu não joga e se organiza antes do pré-load, no dia dez.",
               {"chapeu": "CHECKLIST", "titulo": "ANTES DO DIA 10", "itens": ["Confere o espaço livre", "Apaga o que não joga", "Pré-load: 10/11"]},
               "Console apertado? Confere o espaço, apaga o que tu não joga e se organiza antes do pré-load, no dia 10."),
             cta("Teu console aguenta? Comenta quanto espaço tu tem livre!", "TEU CONSOLE\nAGUENTA?", "Comenta o espaço livre"),
         ]),
    dict(data="2026-11-08", tema="cachorro-tatico", titulo_interno="O cachorro com equipamento de combate",
         fontes=fontes("pcg_galeria"),
         titulos=["GTA 6 TEM CACHORRO DE COMBATE? 🐕 repara no fundo", "GTA 6: O CÃO TÁTICO DAS IMAGENS NOVAS 👀", "GTA 6: NINGUÉM VIU ESSE CACHORRO 🐶"],
         tags=["gta 6", "gta 6 cachorro", "gta 6 detalhes", "gta 6 launch gallery", "gta 6 segredos", "gta vi"],
         fixado="Cachorro parceiro no GTA 6: sim ou não? 👇",
         blocos=lambda: [
             vinheta(5),
             b("N02", "manchete", "Repara no fundo dessa imagem: tem um cachorro com equipamento de combate no GTA seis.",
               {"chapeu": "REPARA NO FUNDO", "titulo": "CACHORRO\nTÁTICO?", "rodape": "Launch Gallery · 05/11/2026"},
               "Repara no fundo dessa imagem: tem um cachorro com equipamento de combate no GTA 6."),
             b("N03", "imagem", "Ele aparece atrás da ação, numa das imagens novas, com equipamento de cão de operação.",
               {"chapeu": "NA IMAGEM OFICIAL", "titulo": "OLHA ELE AQUI", "descricao": "Screenshot oficial com o cão\nde equipamento tático ao fundo", "credito": CRED}),
             b("N04", "lista", "No GTA cinco tinha o Chop. Agora a Rockstar não explicou se esse é parceiro, inimigo ou só cenário.",
               {"chapeu": "O QUE SE SABE", "titulo": "SEM CONFIRMAÇÃO", "itens": ["Está em imagem oficial", "Função não revelada", "Dia 19 a gente descobre"]},
               "No GTA 5 tinha o Chop. Agora a Rockstar não explicou se esse é parceiro, inimigo ou só cenário."),
             cta("Tu quer cachorro parceiro no GTA seis? Comenta aí!", "CACHORRO\nPARCEIRO?", "Sim ou não? Comenta",
                 legenda="Tu quer cachorro parceiro no GTA 6? Comenta aí!"),
         ]),
    dict(data="2026-11-08", tema="poros", titulo_interno="Detalhe da pele: dá pra ver os poros",
         fontes=fontes("pcg_galeria"),
         titulos=["GTA 6: DÁ PRA VER OS POROS 😳 nível absurdo", "GTA 6 TÁ REALISTA DEMAIS? 🔍", "GTA 6: O DETALHE DA PELE NAS IMAGENS NOVAS 👀"],
         tags=["gta 6", "gta 6 gráficos", "gta 6 realista", "gta 6 detalhes", "gta 6 imagens novas", "gta vi"],
         fixado="Realista demais ou no ponto? 👇",
         blocos=lambda: [
             vinheta(6),
             b("N02", "manchete", "O nível de detalhe do GTA seis chegou num ponto absurdo: dá pra ver os poros da pele.",
               {"chapeu": "GRÁFICOS", "titulo": "DÁ PRA VER\nOS POROS", "rodape": "Launch Gallery · 05/11/2026"},
               "O nível de detalhe do GTA 6 chegou num ponto absurdo: dá pra ver os poros da pele."),
             b("N03", "imagem", "Nas imagens novas, cada rosto tem poro, marca e textura diferente.",
               {"chapeu": "DÁ ZOOM", "titulo": "PELE DE VERDADE", "descricao": "Close oficial de rosto\n(dar zoom na pele)", "credito": CRED}),
             b("N04", "lista", "E cada personagem tem um cuidado de pele diferente. Uns caprichados, outros nem tanto.",
               {"chapeu": "REPARA", "titulo": "CADA UM É UM", "itens": ["Poros visíveis", "Marcas e textura", "Cada rosto diferente"]}),
             cta("Isso é imagem oficial, não é mod. Realista demais ou tá no ponto? Comenta!", "REALISTA\nDEMAIS?", "Imagem oficial, não é mod"),
         ]),
    # ---------------- 09/11 ----------------
    dict(data="2026-11-09", tema="quem-joga-primeiro", titulo_interno="Quem joga primeiro: Nova Zelândia",
         fontes=fontes("vice_horario"),
         titulos=["GTA 6: TEM GENTE QUE VAI JOGAR ANTES DE TU 😤", "GTA 6: QUE HORAS LIBERA NO BRASIL? ⏰", "GTA 6: A NOVA ZELÂNDIA JOGA PRIMEIRO 🌏"],
         tags=["gta 6", "gta 6 horário", "gta 6 que horas libera", "gta 6 lançamento", "gta 6 brasil", "gta vi"],
         fixado="Vai virar a noite do dia 18 pro 19? 👇 (Confere o horário na loja do teu console.)",
         blocos=lambda: [
             vinheta(7),
             b("N02", "manchete", "Sabia que tem gente que vai jogar GTA seis antes da gente?",
               {"chapeu": "LANÇAMENTO", "titulo": "QUEM JOGA\nPRIMEIRO?", "rodape": "Fonte: VICE · 03/11/2026"},
               "Sabia que tem gente que vai jogar GTA 6 antes da gente?"),
             b("N03", "manchete", "A Rockstar libera o jogo à meia-noite no horário de cada lugar. E quem chega primeiro na meia-noite é a Nova Zelândia.",
               {"chapeu": "MEIA-NOITE LOCAL", "titulo": "NOVA\nZELÂNDIA", "rodape": "Primeira a chegar no dia 19"}),
             b("N04", "lista", "Lá, o dia dezenove começa às oito da manhã do dia dezoito, no horário de Brasília. Aqui, é meia-noite do dia dezenove.",
               {"chapeu": "HORÁRIO DE BRASÍLIA", "titulo": "LÁ X AQUI", "itens": ["Nova Zelândia: 18/11, 8h", "Brasil: 19/11, 0h", "Confere na loja do console"]},
               "Lá, o dia 19 começa às 8 da manhã do dia 18, no horário de Brasília. Aqui, é meia-noite do dia 19."),
             cta("Tu vai virar a noite pra jogar? Comenta aí!", "VAI VIRAR\nA NOITE?", "Comenta aí"),
         ]),
    dict(data="2026-11-09", tema="florida-man", titulo_interno="Os personagens 'Florida Man' das imagens novas",
         fontes=fontes("pcg_galeria"),
         titulos=["GTA 6 NO MODO FLORIDA MAN 🐊 os NPCs mais bizarros", "GTA 6: OS PERSONAGENS MAIS ESTRANHOS DAS IMAGENS 😂", "GTA 6: REPARA NESSES NPCs 👀"],
         tags=["gta 6", "gta 6 florida man", "gta 6 npc", "gta 6 personagens", "gta 6 detalhes", "gta vi"],
         fixado="Qual desses tu encontraria na tua cidade? 👇",
         blocos=lambda: [
             vinheta(8),
             b("N02", "manchete", "Leonida é a Flórida da Rockstar. E os personagens das imagens novas provam isso.",
               {"chapeu": "PERSONAGENS", "titulo": "MODO\nFLORIDA MAN", "rodape": "Launch Gallery · 05/11/2026"}),
             b("N03", "imagem", "Tem um cara com um olho de cada cor, do lado de dois répteis mortos.",
               {"chapeu": "O PRIMEIRO", "titulo": "UM OLHO DE CADA COR", "descricao": "Personagem com heterocromia\nao lado de dois répteis", "credito": CRED}),
             b("N04", "lista", "Tem um sujeito de mullet, com faca, ameaçando o Jason. E policial de bigode com óculos aviador.",
               {"chapeu": "E TEM MAIS", "titulo": "A GALERA", "itens": ["Olho de cada cor + répteis", "Mullet com faca", "Bigode e óculos aviador"]}),
             cta("Qual desses tu encontraria na tua cidade? Comenta!", "QUAL É O\nMAIS DOIDO?", "Comenta aí"),
         ]),
    dict(data="2026-11-09", tema="jason-militar", titulo_interno="Jason saindo de avião militar",
         fontes=fontes("pcg_galeria", "mp1st_bios"),
         titulos=["GTA 6: JASON EM MISSÃO MILITAR? 🪖", "GTA 6: A IMAGEM DO AVIÃO MILITAR 😱", "GTA 6: O PASSADO DO JASON APARECEU 👀"],
         tags=["gta 6", "gta 6 jason", "jason duval", "gta 6 história", "gta 6 imagens novas", "gta vi"],
         fixado="Missão militar no GTA 6: curtiu? 👇",
         blocos=lambda: [
             vinheta(9),
             b("N02", "manchete", "Numa das imagens novas, o Jason desce de um avião militar direto pro meio de um tiroteio.",
               {"chapeu": "JASON DUVAL", "titulo": "MISSÃO\nMILITAR?", "rodape": "Launch Gallery · 05/11/2026"}),
             b("N03", "imagem", "Ele tá com equipamento tático completo.",
               {"chapeu": "NA IMAGEM OFICIAL", "titulo": "EQUIPAMENTO TÁTICO", "descricao": "Jason com equipamento tático\ndescendo do avião militar", "credito": CRED}),
             b("N04", "lista", "E faz sentido: na biografia oficial, o Jason é ex-soldado. A missão em si, a Rockstar ainda não explicou.",
               {"chapeu": "BIOGRAFIA OFICIAL", "titulo": "EX-SOLDADO", "itens": ["Bio oficial: ex-soldado", "Equipamento tático", "Missão sem detalhes"]}),
             cta("Missão de guerra no GTA: tu curte ou prefere o crime de rua? Comenta!", "GUERRA OU\nRUA?", "Comenta aí"),
         ]),
    # ---------------- 10/11 ----------------
    dict(data="2026-11-10", tema="mergulho-jacare", titulo_interno="Mergulho e jacaré",
         fontes=fontes("pcg_galeria", "mp1st_bios"),
         titulos=["GTA 6 VAI TER MERGULHO? 🤿 olha a imagem", "GTA 6: MERGULHO E JACARÉ 🐊", "GTA 6: O MAR DE LEONIDA 🌊"],
         tags=["gta 6", "gta 6 mergulho", "gta 6 jacaré", "gta 6 leonida keys", "gta 6 grassrivers", "gta vi"],
         fixado="Mergulhar ou fugir de jacaré? 👇",
         blocos=lambda: [
             vinheta(10),
             b("N02", "manchete", "Vai dar pra mergulhar no GTA seis? Uma das imagens novas mostra mergulho com cilindro.",
               {"chapeu": "ATIVIDADES", "titulo": "MERGULHO\nNO GTA 6", "rodape": "Launch Gallery · 05/11/2026"},
               "Vai dar pra mergulhar no GTA 6? Uma das imagens novas mostra mergulho com cilindro."),
             b("N03", "imagem", "E tem jacaré, claro. É Leonida.",
               {"chapeu": "E CLARO...", "titulo": "TEM JACARÉ", "descricao": "Screenshot oficial:\nmergulho e/ou jacaré", "credito": CRED}),
             b("N04", "lista", "Na apresentação oficial, os Grassrivers são um mangue cheio de jacaré. E os Leonida Keys ficam perto de águas perigosas.",
               {"chapeu": "MAPA OFICIAL", "titulo": "ÁGUA E PERIGO", "itens": ["Mergulho com cilindro", "Jacaré nos Grassrivers", "Águas perigosas nos Keys"]}),
             cta("O que tu faz primeiro: mergulha ou foge do jacaré? Comenta!", "MERGULHA\nOU FOGE?", "Comenta aí"),
         ]),
    dict(data="2026-11-10", tema="assalto-shopping", titulo_interno="Assalto que parece ser em shopping",
         fontes=fontes("ri_galeria", "mp1st_bios"),
         titulos=["GTA 6: ASSALTO NO SHOPPING? 💰", "GTA 6: A IMAGEM DO ASSALTO 😱 e a fuga de moto", "GTA 6: JASON E LUCIA EM FUGA 🏍️"],
         tags=["gta 6", "gta 6 assalto", "gta 6 heist", "gta 6 jason e lucia", "gta 6 imagens novas", "gta vi"],
         fixado="Tu planeja o assalto ou entra atirando? 👇",
         blocos=lambda: [
             vinheta(11),
             b("N02", "manchete", "Uma das imagens novas mostra um assalto que parece acontecer dentro de um shopping.",
               {"chapeu": "ASSALTO", "titulo": "NO\nSHOPPING?", "rodape": "Launch Gallery · 05/11/2026"}),
             b("N03", "imagem", "E tem Jason e Lucia fugindo de moto.",
               {"chapeu": "A FUGA", "titulo": "DE MOTO", "descricao": "Cena do assalto / Jason e Lucia\nfugindo de moto", "credito": CRED}),
             b("N04", "lista", "Na biografia oficial tem o Raul Bautista, um ladrão de banco experiente que recruta gente pra equipe. Tem ligação? Ainda não se sabe.",
               {"chapeu": "TEORIA", "titulo": "TEM LIGAÇÃO?", "itens": ["Assalto em interior novo", "Fuga de moto", "Raul monta equipes"]}),
             cta("Tu planeja o assalto ou entra atirando? Comenta!", "PLANEJA OU\nENTRA ATIRANDO?", "Comenta aí"),
         ]),
    dict(data="2026-11-10", tema="mapa-6-regioes", titulo_interno="As 6 regiões de Leonida",
         fontes=fontes("mp1st_bios", "vgc_preload"),
         titulos=["GTA 6: O MAPA EM 30 SEGUNDOS 🗺️", "GTA 6: AS 6 REGIÕES DE LEONIDA 🌴", "GTA 6: PRA ONDE TU VAI PRIMEIRO? 🗺️"],
         tags=["gta 6", "gta 6 mapa", "leonida", "vice city", "gta 6 regiões", "gta vi"],
         fixado="Qual região tu explora primeiro? 👇",
         blocos=lambda: [
             vinheta(12),
             b("N02", "manchete", "O mapa do GTA seis tem seis regiões já reveladas. Bora conhecer rapidinho.",
               {"chapeu": "MAPA DE LEONIDA", "titulo": "6 REGIÕES", "rodape": "Fonte: apresentação oficial (05/2025)"},
               "O mapa do GTA 6 tem 6 regiões já reveladas. Bora conhecer rapidinho."),
             b("N03", "lista", "Vice City, a cidade grande. Leonida Keys, as ilhas. E os Grassrivers, o mangue.",
               {"chapeu": "PARTE 1", "titulo": "CIDADE, ILHA, MANGUE", "itens": ["Vice City", "Leonida Keys", "Grassrivers"]}),
             b("N04", "lista", "Port Gellhorn, o balneário decadente. Ambrosia, a cidade da usina de açúcar. E Mount Kalaga, o parque nacional no norte.",
               {"chapeu": "PARTE 2", "titulo": "E MAIS TRÊS", "itens": ["Port Gellhorn", "Ambrosia", "Mount Kalaga"]}),
             cta("No dia dezenove, a Rockstar libera o mapa de Leonida grátis pra baixar. Qual região tu vai primeiro?",
                 "QUAL\nPRIMEIRO?", "Mapa grátis no dia 19",
                 legenda="No dia 19, a Rockstar libera o mapa de Leonida grátis pra baixar. Qual região tu vai primeiro?"),
         ]),
    # ---------------- 11/11 ----------------
    dict(data="2026-11-11", tema="bonus-pre-venda", titulo_interno="Bônus de pré-venda Vice City Vintage",
         fontes=fontes("ch_preco"),
         titulos=["GTA 6: O BÔNUS DE QUEM RESERVA 🎁", "GTA 6: VICE CITY VINTAGE 🚗 o que vem", "GTA 6: VALE RESERVAR? 🎁"],
         tags=["gta 6", "gta 6 bônus pré-venda", "vice city vintage", "gta 6 ultimate", "gta+", "gta vi"],
         fixado="Tu já reservou? 👇",
         blocos=lambda: [
             vinheta(13),
             b("N02", "manchete", "Quem reserva o GTA seis leva um bônus chamado Vice City Vintage.",
               {"chapeu": "PRÉ-VENDA", "titulo": "VICE CITY\nVINTAGE", "rodape": "Fonte: Critical Hits · 25/06/2026"},
               "Quem reserva o GTA 6 leva um bônus chamado Vice City Vintage."),
             b("N03", "lista", "Vem um veículo exclusivo, uma garagem personalizável, opções visuais pros protagonistas e um mês grátis de GTA mais.",
               {"chapeu": "O QUE VEM", "titulo": "O PACOTE", "itens": ["Veículo exclusivo", "Garagem personalizável", "1 mês de GTA+"]},
               "Vem um veículo exclusivo, uma garagem personalizável, opções visuais pros protagonistas e um mês grátis de GTA+."),
             b("N04", "manchete", "Vale pras duas edições. E a Ultimate ainda libera extras durante a campanha.",
               {"chapeu": "ULTIMATE", "titulo": "EXTRAS NA\nCAMPANHA", "rodape": "Carros, armas, missões e roupas"}),
             cta("Tu já reservou? Comenta aí!", "JÁ\nRESERVOU?", "Comenta aí"),
         ]),
    dict(data="2026-11-11", tema="brinde-mapa-poster", titulo_interno="Brinde: mapa de Leonida e pôster grátis",
         fontes=fontes("vgc_preload"),
         titulos=["GTA 6: MAPA DE LEONIDA DE GRAÇA 🗺️", "GTA 6: O BRINDE DO DIA DO LANÇAMENTO 🎁", "GTA 6: PÔSTER GRÁTIS PRA IMPRIMIR 🖨️"],
         tags=["gta 6", "gta 6 mapa", "gta 6 pôster", "gta 6 brinde", "leonida", "gta vi"],
         fixado="Vai imprimir o mapa? 👇",
         blocos=lambda: [
             vinheta(14),
             b("N02", "manchete", "No dia do lançamento, a Rockstar vai liberar um presente de graça.",
               {"chapeu": "BRINDE", "titulo": "MAPA DE\nLEONIDA GRÁTIS", "rodape": "Fonte: VGC · 03/11/2026"}),
             b("N03", "lista", "Um pôster da capa pra imprimir e o mapa de Leonida, pra baixar no site da Rockstar.",
               {"chapeu": "DIA 19/11", "titulo": "DOWNLOAD GRÁTIS", "itens": ["Pôster da capa", "Mapa de Leonida", "No site da Rockstar"]}),
             b("N04", "manchete", "E tem um pôster físico dupla face na loja da Rockstar, por noventa e nove centavos de dólar, ou de brinde em qualquer compra.",
               {"chapeu": "ROCKSTAR STORE", "titulo": "PÔSTER\nFÍSICO", "rodape": "US$ 0,99 ou brinde em compras"},
               "E tem um pôster físico dupla face na loja da Rockstar, por US$ 0,99, ou de brinde em qualquer compra."),
             cta("Vai imprimir o mapa? Comenta aí!", "VAI\nIMPRIMIR?", "Comenta aí"),
         ]),
    dict(data="2026-11-11", tema="trilha-justice", titulo_interno="Trilha original do Justice",
         fontes=fontes("justice", "justice2"),
         titulos=["GTA 6: A TRILHA É DO JUSTICE 🎧", "GTA 6: 30 FAIXAS ORIGINAIS 🎶 sai dia 11/12", "GTA 6: JÁ SAIU A PRIMEIRA MÚSICA 🔊"],
         tags=["gta 6", "gta 6 trilha sonora", "justice", "gesaffelstein", "pusher", "gta vi"],
         fixado="Rádio do jogo ou trilha original? 👇",
         blocos=lambda: [
             vinheta(15),
             b("N02", "manchete", "A trilha original do GTA seis é do Justice, a dupla francesa de música eletrônica.",
               {"chapeu": "TRILHA SONORA", "titulo": "JUSTICE\nNO GTA 6", "rodape": "Fonte: GamerFuzion · 29/10/2026"},
               "A trilha original do GTA 6 é do Justice, a dupla francesa de música eletrônica."),
             b("N03", "lista", "São trinta faixas, lançamento dia onze de dezembro, nos streamings, em CD e em vinil.",
               {"chapeu": "O ÁLBUM", "titulo": "11 DE DEZEMBRO", "itens": ["30 faixas", "Streaming em 11/12", "CD e vinil"]},
               "São 30 faixas, lançamento dia 11 de dezembro, nos streamings, em CD e em vinil."),
             b("N04", "manchete", "E a primeira já saiu: Pusher, com participação do Gesaffelstein.",
               {"chapeu": "JÁ SAIU", "titulo": "PUSHER", "rodape": "Justice + Gesaffelstein"}),
             cta("Tu prefere a rádio do jogo ou a trilha original? Comenta!", "RÁDIO OU\nTRILHA?", "Comenta aí"),
         ]),
]


def main():
    for i, s in enumerate(SHORTS, 1):
        slug = f"{s['data']}_SHORT_detalhes-gta6_{i:02d}-{s['tema']}"
        pasta = os.path.join(AQUI, s["data"])
        os.makedirs(pasta, exist_ok=True)
        desc = (f"{s['titulo_interno']} — série Detalhes que ninguém viu #{i}.\n"
                "GTA 6 chega em 19/11/2026 para PS5 e Xbox Series X|S.\n\n"
                "Imagens: Rockstar Games (material oficial, usado com comentário). Sem vazamentos e sem spoilers.\n"
                "🔔 Se inscreve e ativa o sino: clipes novos todo dia no Universo dos Clips.\n"
                "#gta6 #gtavi #universodosclips")
        rot = {
            "slug": slug,
            "titulo_interno": f"Detalhes que ninguém viu #{i} — {s['titulo_interno']}",
            "formato": "Detalhes que ninguém viu (Short 9:16)",
            "marca": "universo-dos-clips",
            "publicar_em": s["data"],
            "fontes": s["fontes"],
            "seo": {"titulos": s["titulos"], "descricao": desc, "tags": s["tags"] + ["universo dos clips"],
                    "comentario_fixado": s["fixado"],
                    "video_relacionado": "GTA 6: tudo que sabemos antes do lançamento (longo) [DEFINIR LINK]"},
            "blocos": s["blocos"](),
        }
        json.dump(rot, open(os.path.join(pasta, slug + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(slug)


if __name__ == "__main__":
    main()
