#!/usr/bin/env bash
set -Eeuo pipefail

cd "$(dirname "$0")"

if [ ! -x .venv/bin/python ]; then
    echo "Brak środowiska venv."
    echo "Najpierw uruchom: ./install.sh"
    exit 1
fi

exec .venv/bin/python telegram_monitor.py "$@"
