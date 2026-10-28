#!/usr/bin/env bash
# Instala as dependências e baixa os modelos abertos (voz e recorte de fundo).
# Uso: bash setup.sh
set -e
cd "$(dirname "$0")"

command -v ffmpeg >/dev/null || { echo "Instale o FFmpeg (com libass) antes de continuar."; exit 1; }

PIP_FLAGS=""
pip install --help 2>/dev/null | grep -q -- "--break-system-packages" && PIP_FLAGS="--break-system-packages"
pip install -q $PIP_FLAGS kokoro-onnx soundfile numpy pillow "rembg[cpu]"

mkdir -p .modelos/kokoro .modelos/rembg
baixar () { [ -s "$2" ] || curl -sSL -o "$2" "$1"; }
baixar https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx .modelos/kokoro/kokoro-v1.0.onnx
baixar https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin .modelos/kokoro/voices-v1.0.bin
baixar https://github.com/danielgatis/rembg/releases/download/v0.0.0/isnet-general-use.onnx .modelos/rembg/isnet-general-use.onnx

echo "Pronto. Teste com:"
echo "  python3 motor/gerar.py roteiros/exemplos/2026-10-27_noticia-do-forro.json saida/"
