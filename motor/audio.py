"""Narração por bloco (TTS aberto Kokoro, pt-BR) + trilha de baião gerada em código.

Uso: python3 audio.py roteiro.json build/
Saída: build/01_audio/N01.wav ... e build/01_audio/duracoes.json
A trilha é gerada depois, em render.py, quando a duração total é conhecida.
"""
import json
import os
import sys

import numpy as np
import soundfile as sf

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_DIR = os.environ.get("KOKORO_DIR", os.path.join(REPO, ".modelos", "kokoro"))
SR = 24000


def narrar(roteiro_path, build_dir):
    from kokoro_onnx import Kokoro

    rot = json.load(open(roteiro_path, encoding="utf-8"))
    out = os.path.join(build_dir, "01_audio")
    os.makedirs(out, exist_ok=True)
    if rot.get("narracao_dir"):  # narração pronta (ex.: ElevenLabs do Magnific), um arquivo por bloco
        return narracao_externa(rot, os.path.dirname(os.path.abspath(roteiro_path)), out)
    k = Kokoro(os.path.join(MODEL_DIR, "kokoro-v1.0.onnx"), os.path.join(MODEL_DIR, "voices-v1.0.bin"))
    marca = ler_marca(rot.get("marca"))  # a marca pode definir voz e velocidade padrão do canal
    voz = rot.get("voz") or marca.get("voz", "pm_alex")
    if ":" in voz:  # ex.: "elevenlabs:..." é só anotação de narração externa; o Kokoro usa a voz da marca
        voz = marca.get("voz", "pm_alex")
    velocidade = rot.get("velocidade", marca.get("velocidade", 1.0))
    dur = {}
    for b in rot["blocos"]:
        sinal, sr = k.create(b["narracao"], voice=voz, speed=velocidade, lang="pt-br")
        sinal = aparar_silencio(sinal, sr)
        sf.write(os.path.join(out, f"{b['id']}.wav"), sinal, sr)
        dur[b["id"]] = round(len(sinal) / sr, 3)
        print(b["id"], dur[b["id"]], "s")
    json.dump(dur, open(os.path.join(out, "duracoes.json"), "w"), indent=2)
    return dur


def ler_marca(valor):
    """Lê marcas/<nome>/marca.json (ou um caminho direto). Retorna {} se não achar."""
    if not valor:
        return {}
    caminho = valor if os.path.exists(valor) else os.path.join(REPO, "marcas", valor, "marca.json")
    return json.load(open(caminho, encoding="utf-8")) if os.path.exists(caminho) else {}


def narracao_externa(rot, base_rot, out):
    """Usa arquivos de narração já gravados: <narracao_dir>/<id>.mp3 (ou .wav) para cada bloco."""
    import subprocess
    pasta = os.path.join(base_rot, rot["narracao_dir"])
    dur = {}
    for b in rot["blocos"]:
        origem = next((os.path.join(pasta, b["id"] + ext) for ext in (".mp3", ".wav", ".m4a")
                       if os.path.exists(os.path.join(pasta, b["id"] + ext))), None)
        if not origem:
            raise FileNotFoundError(f"Narração do bloco {b['id']} não encontrada em {pasta}")
        tmp = os.path.join(out, f"{b['id']}_orig.wav")
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", origem, "-ac", "1", "-ar", str(SR), tmp], check=True)
        sinal, sr = sf.read(tmp)
        os.remove(tmp)
        sinal = aparar_silencio(sinal, sr)
        sf.write(os.path.join(out, f"{b['id']}.wav"), sinal, sr)
        dur[b["id"]] = round(len(sinal) / sr, 3)
        print(b["id"], dur[b["id"]], "s (narração externa)")
    json.dump(dur, open(os.path.join(out, "duracoes.json"), "w"), indent=2)
    return dur


def aparar_silencio(x, sr, limiar=0.01, margem=0.06):
    idx = np.where(np.abs(x) > limiar)[0]
    if len(idx) == 0:
        return x
    a = max(0, idx[0] - int(margem * sr))
    b = min(len(x), idx[-1] + int(margem * sr))
    return x[a:b]


def trilha_baiao(duracao, caminho, bpm=128, sr=44100):
    """Baião sintético: zabumba (grave + bacalhau), triângulo e baixo. Sem amostras de terceiros."""
    n = int(duracao * sr)
    mix = np.zeros(n)
    beat = 60.0 / bpm
    t_env = lambda dur: np.arange(int(dur * sr)) / sr

    def add(sinal, inicio):
        i = int(inicio * sr)
        if i >= n:
            return
        f = min(len(sinal), n - i)
        mix[i:i + f] += sinal[:f]

    def zabumba(vol=0.9):
        t = t_env(0.35)
        freq = 95 * np.exp(-t * 9) + 48
        fase = 2 * np.pi * np.cumsum(freq) / sr
        return vol * np.sin(fase) * np.exp(-t * 11)

    def bacalhau(vol=0.18):
        t = t_env(0.05)
        return vol * np.random.default_rng(1).standard_normal(len(t)) * np.exp(-t * 90)

    def triangulo(aberto, vol=0.10):
        t = t_env(0.45 if aberto else 0.07)
        s = sum(np.sin(2 * np.pi * f * t) for f in (3150, 4410, 6620))
        return vol * s / 3 * np.exp(-t * (6 if aberto else 60))

    def baixo(freq, dur, vol=0.22):
        t = t_env(dur)
        env = np.minimum(1, t * 80) * np.exp(-t * 3)
        return vol * (np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(4 * np.pi * freq * t)) * env

    progressao = [55.0, 55.0, 73.42, 61.74]  # Lá, Lá, Ré, Si (dó mixolídio nordestino)
    compasso = 2 * beat  # baião em 2/4
    c = 0
    while c * compasso < duracao:
        t0 = c * compasso
        # zabumba: colcheia pontuada + semicolcheia + semínima (célula do baião)
        add(zabumba(), t0)
        add(zabumba(0.7), t0 + beat * 0.75)
        add(zabumba(0.8), t0 + beat)
        add(bacalhau(), t0 + beat * 0.5)
        add(bacalhau(), t0 + beat * 1.5)
        for s in range(8):  # triângulo em semicolcheias, aberto no contratempo
            add(triangulo(s % 4 == 2), t0 + s * beat / 4)
        f = progressao[(c // 2) % len(progressao)]
        add(baixo(f, beat * 0.7), t0)
        add(baixo(f * 1.5, beat * 0.4), t0 + beat * 0.75)
        add(baixo(f, beat * 0.9), t0 + beat)
        c += 1
    mix /= np.max(np.abs(mix)) + 1e-9
    fade = int(1.2 * sr)
    mix[-fade:] *= np.linspace(1, 0, fade)
    mix[: int(0.3 * sr)] *= np.linspace(0, 1, int(0.3 * sr))
    sf.write(caminho, (mix * 0.9).astype(np.float32), sr)


def trilha_synth(duracao, caminho, bpm=112, sr=44100):
    """Synthwave sintético (Universo dos Clips): bumbo, palma, chimbal e baixo em arpejo menor. Sem amostras."""
    n = int(duracao * sr)
    mix = np.zeros(n)
    beat = 60.0 / bpm
    t_env = lambda dur: np.arange(int(dur * sr)) / sr
    rng = np.random.default_rng(7)

    def add(sinal, inicio):
        i = int(inicio * sr)
        if i >= n:
            return
        f = min(len(sinal), n - i)
        mix[i:i + f] += sinal[:f]

    def bumbo(vol=0.95):
        t = t_env(0.32)
        freq = 120 * np.exp(-t * 22) + 45
        return vol * np.sin(2 * np.pi * np.cumsum(freq) / sr) * np.exp(-t * 9)

    def palma(vol=0.30):
        t = t_env(0.18)
        ruido = rng.standard_normal(len(t))
        return vol * ruido * (np.exp(-t * 28) + 0.4 * np.exp(-((t - 0.012) ** 2) / 1e-5))

    def chimbal(vol=0.06):
        t = t_env(0.05)
        return vol * rng.standard_normal(len(t)) * np.exp(-t * 120)

    def baixo(freq, dur, vol=0.20):
        t = t_env(dur)
        serra = 2 * (t * freq - np.floor(0.5 + t * freq))  # dente de serra
        env = np.minimum(1, t * 120) * np.exp(-t * 4)
        return vol * (0.6 * serra + 0.4 * np.sin(2 * np.pi * freq * t)) * env

    def pad(freqs, dur, vol=0.05):
        t = t_env(dur)
        env = np.minimum(1, t * 2) * np.minimum(1, (dur - t) * 2 + 0.01)
        return vol * sum(np.sin(2 * np.pi * f * t) + 0.5 * np.sin(2 * np.pi * f * 1.005 * t) for f in freqs) * env

    progressao = [55.0, 43.65, 65.41, 49.0]  # Lá menor, Fá, Dó, Sol (i-VI-III-VII)
    compasso = 4 * beat
    c = 0
    while c * compasso < duracao:
        t0 = c * compasso
        f = progressao[c % len(progressao)]
        add(pad([f * 4, f * 4 * 1.19, f * 6], compasso), t0)
        for s in range(4):
            add(bumbo(), t0 + s * beat)
            if s % 2 == 1:
                add(palma(), t0 + s * beat)
        for s in range(8):
            add(chimbal(0.08 if s % 2 else 0.04), t0 + s * beat / 2)
            add(baixo(f * (2 if s % 2 else 1), beat * 0.45), t0 + s * beat / 2)
        c += 1
    mix /= np.max(np.abs(mix)) + 1e-9
    fade = int(1.2 * sr)
    mix[-fade:] *= np.linspace(1, 0, fade)
    mix[: int(0.3 * sr)] *= np.linspace(0, 1, int(0.3 * sr))
    sf.write(caminho, (mix * 0.9).astype(np.float32), sr)


TRILHAS = {"baiao": trilha_baiao, "synth": trilha_synth}


if __name__ == "__main__":
    narrar(sys.argv[1], sys.argv[2])
