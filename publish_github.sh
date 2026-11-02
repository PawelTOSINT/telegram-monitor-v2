#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="https://github.com/PawelTOSINT/telegram-monitor-v2.git"

cd "$PROJECT"

echo "=========================================="
echo " TELEGRAM MONITOR V2 - SAFE PUBLISHER"
echo "=========================================="

command -v git >/dev/null || {
    echo "[ERROR] Brak Git. Zainstaluj: sudo apt install git"
    exit 1
}

# 1. Bezpieczny .gitignore
cat > .gitignore <<'IGNORE'
__pycache__/
*.py[cod]
*.pyo

.venv/
venv/
env/

*.session
*.session-journal
session/

config/accounts.json
config/telegram_credentials.json
config/settings.json
config/keywords.txt
config/channels.txt
config/time_range.json
config/channels/

database/
results/
cache/
media/
videos/

*.tmp
*.log
.DS_Store
Thumbs.db

.env
.env.*
!.env.example
IGNORE

# 2. Kontrola wymaganych plików
for file in telegram_monitor.py requirements.txt; do
    if [ ! -f "$file" ]; then
        echo "[ERROR] Brakuje pliku: $file"
        exit 1
    fi
done

# 3. Kontrola JSON
echo
echo "[1/6] Kontrola plików JSON..."

python3 - <<'PY'
import json
from pathlib import Path

for path in sorted(Path("config").glob("*.example.json")):
    try:
        json.loads(path.read_text(encoding="utf-8"))
        print("[OK]", path)
    except Exception as exc:
        print("[ERROR]", path, exc)
        raise SystemExit(1)

path = Path("config/keyword_translations.json")
if path.exists():
    json.loads(path.read_text(encoding="utf-8"))
    print("[OK]", path)
PY

# 4. Kontrola składni Python
echo
echo "[2/6] Kontrola składni Python..."

python3 - <<'PY'
import ast
from pathlib import Path

failed = False

for path in sorted(Path(".").rglob("*.py")):
    if any(part in {".venv", "venv", "__pycache__"} for part in path.parts):
        continue
    try:
        ast.parse(path.read_text(encoding="utf-8"))
        print("[OK]", path)
    except Exception as exc:
        print("[ERROR]", path, exc)
        failed = True

if failed:
    raise SystemExit(1)
PY

# 5. Git
echo
echo "[3/6] Konfiguracja Git..."

if [ ! -d .git ]; then
    git init
fi

if git remote get-url origin >/dev/null 2>&1; then
    CURRENT_REMOTE="$(git remote get-url origin)"
    if [ "$CURRENT_REMOTE" != "$REPO" ]; then
        echo "[ERROR] Istniejący origin wskazuje na inne repozytorium:"
        echo "$CURRENT_REMOTE"
        echo "Nie zmieniam go automatycznie."
        exit 1
    fi
else
    git remote add origin "$REPO"
fi

git branch -M main

# 6. Sprawdzenie już śledzonych prywatnych plików
echo
echo "[4/6] Kontrola prywatnych plików..."

FORBIDDEN="$(git ls-files | grep -E \
'(^|/)(accounts\.json|telegram_credentials\.json|settings\.json|keywords\.txt|channels\.txt|time_range\.json|\.env)$|\.session(-journal)?$' \
|| true)"

if [ -n "$FORBIDDEN" ]; then
    echo "[ERROR] Git już śledzi prywatne pliki:"
    echo "$FORBIDDEN"
    echo "Najpierw usuń je z indeksu Git."
    exit 1
fi

# 7. Przygotowanie zmian
echo
echo "[5/6] Przygotowanie zmian..."

git add -A

FORBIDDEN="$(git diff --cached --name-only | grep -E \
'(^|/)(accounts\.json|telegram_credentials\.json|settings\.json|keywords\.txt|channels\.txt|time_range\.json|\.env)$|\.session(-journal)?$' \
|| true)"

if [ -n "$FORBIDDEN" ]; then
    echo "[ERROR] Wykryto prywatne pliki w commicie:"
    echo "$FORBIDDEN"
    exit 1
fi

git diff --cached --check

echo
echo "=========================================="
echo " PLIKI PRZYGOTOWANE DO PUBLIKACJI"
echo "=========================================="

git status --short
git diff --cached --stat

echo
echo "Sprawdź dokładnie powyższą listę."

read -r -p "Czy utworzyć lokalny commit? [t/N] " answer

if [[ ! "$answer" =~ ^[TtYy]$ ]]; then
    echo "Przerwano. Nic nie wysłano na GitHub."
    exit 0
fi

if git diff --cached --quiet; then
    echo "[INFO] Brak zmian do zapisania."
else
    git commit -m "Prepare Telegram Monitor V2 for publication"
fi

# 8. Push tylko po dodatkowym potwierdzeniu
echo
echo "[6/6] Lokalny commit jest gotowy."

echo "Repozytorium docelowe:"
echo "$REPO"

read -r -p "Czy wysłać commit na GitHub? [t/N] " answer

if [[ ! "$answer" =~ ^[TtYy]$ ]]; then
    echo "Gotowe. Commit pozostaje lokalnie."
    echo "Push możesz wykonać później: git push -u origin main"
    exit 0
fi

git push -u origin main

echo
echo "=========================================="
echo " PUBLIKACJA ZAKOŃCZONA"
echo "=========================================="
echo "$REPO"
