#!/usr/bin/env bash
set -Eeuo pipefail

cd "$(dirname "$0")"

echo "======================================"
echo " TELEGRAM MONITOR V2 - INSTALLER"
echo "======================================"

command -v python3 >/dev/null || {
    echo "Python 3 nie jest zainstalowany."
    exit 1
}

if ! python3 -m venv --help >/dev/null 2>&1; then
    echo "Brak modułu venv."
    echo "Zainstaluj: sudo apt install python3-venv"
    exit 1
fi

if [ ! -d .venv ]; then
    echo "[1/4] Tworzenie środowiska Python..."
    python3 -m venv .venv
else
    echo "[1/4] Używam istniejącego venv."
fi

echo "[2/4] Aktualizacja pip..."
.venv/bin/python -m pip install --upgrade pip

echo "[3/4] Instalacja zależności..."
.venv/bin/python -m pip install -r requirements.txt

echo "[4/4] Przygotowanie konfiguracji..."

mkdir -p config cache database results session media videos

touch config/keywords.txt
touch config/channels.txt

echo
echo "Instalacja zakończona."
echo
echo "Uruchom program:"
echo "  ./run.sh"
echo
echo "Modele Argos można zainstalować dodatkowo:"
echo "  .venv/bin/python install_argos_models.py"
