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

mkdir -p config/channels cache database results session media videos

for name in settings keywords channels accounts telegram_credentials time_range; do
    case "$name" in
        settings) target="settings.json" ;;
        keywords) target="keywords.txt" ;;
        channels) target="channels.txt" ;;
        accounts) target="accounts.json" ;;
        telegram_credentials) target="telegram_credentials.json" ;;
        time_range) target="time_range.json" ;;
    esac

    if [ ! -f "config/$target" ]; then
        cp "config/$name.example.$(
            case "$name" in
                keywords|channels) echo txt ;;
                *) echo json ;;
            esac
        )" "config/$target"
        echo "[UTWORZONO] config/$target"
    fi
done

echo
echo "Instalacja zakończona."
echo "Uruchom: ./run.sh"
echo
echo "Uzupełnij konfigurację w katalogu config."
