#!/usr/bin/env bash
set -Eeuo pipefail

cd "$(dirname "$0")"

echo "=== NAPRAWA KONFIGURACJI TELEGRAM MONITOR ==="

mkdir -p config/channels cache database results session media videos

# Bezpieczne przykładowe pliki publiczne
cat > config/settings.example.json <<'EOF'
{
  "interface_language": "pl"
}
EOF

cat > config/keywords.example.txt <<'EOF'
# Jeden keyword w każdej linii
# Przykład:
# dron
# rakieta
EOF

cat > config/channels.example.txt <<'EOF'
# Jeden kanał Telegram w każdej linii
# Przykład:
# https://t.me/example_channel
EOF

cat > config/accounts.example.json <<'EOF'
{
  "accounts": []
}
EOF

cat > config/telegram_credentials.example.json <<'EOF'
{
  "api_id": 0,
  "api_hash": ""
}
EOF

cat > config/time_range.example.json <<'EOF'
{
  "from": "2026-01-01",
  "to": "2026-12-31"
}
EOF

# Tworzenie prywatnych plików tylko jeśli nie istnieją
create_private() {
    local source="$1"
    local target="$2"

    if [ ! -f "$target" ]; then
        cp "$source" "$target"
        echo "[UTWORZONO] $target"
    else
        echo "[ZACHOWANO] $target"
    fi
}

create_private config/settings.example.json config/settings.json
create_private config/keywords.example.txt config/keywords.txt
create_private config/channels.example.txt config/channels.txt
create_private config/accounts.example.json config/accounts.json
create_private config/telegram_credentials.example.json config/telegram_credentials.json
create_private config/time_range.example.json config/time_range.json

# Prywatne pliki i katalogi
cat >> .gitignore <<'EOF'

# Local configuration and Telegram secrets
config/settings.json
config/keywords.txt
config/channels.txt
config/accounts.json
config/telegram_credentials.json
config/time_range.json
config/channels/
EOF

# Aktualizacja instalatora
cat > install.sh <<'EOF'
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
EOF

chmod +x install.sh

echo
echo "=== GOTOWE ==="
echo "Sprawdź teraz katalog config."
