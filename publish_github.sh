#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT="$HOME/telegram-monitor-v2-build"
REPO="https://github.com/PawelTOSINT/telegram-monitor-v2.git"

echo "=========================================="
echo " TELEGRAM MONITOR V2 - GITHUB PUBLISHER"
echo "=========================================="

cd "$PROJECT" || {
    echo "[ERROR] Nie znaleziono katalogu projektu."
    exit 1
}

command -v git >/dev/null || {
    echo "[ERROR] Zainstaluj git: sudo apt install git"
    exit 1
}

# ------------------------------------------
# INSTALLER
# ------------------------------------------

cat > install.sh <<'INSTALL'
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
INSTALL

# ------------------------------------------
# RUN SCRIPT
# ------------------------------------------

cat > run.sh <<'RUN'
#!/usr/bin/env bash
set -Eeuo pipefail

cd "$(dirname "$0")"

if [ ! -x .venv/bin/python ]; then
    echo "Brak środowiska venv."
    echo "Najpierw uruchom: ./install.sh"
    exit 1
fi

exec .venv/bin/python telegram_monitor.py "$@"
RUN

chmod +x install.sh run.sh

# ------------------------------------------
# GITIGNORE - OCHRONA DANYCH
# ------------------------------------------

cat > .gitignore <<'IGNORE'
# Python
__pycache__/
*.py[cod]
*.pyo

# Virtual environment
.venv/
venv/
env/

# Private Telegram data
*.session
*.session-journal
session/
config/accounts.json
config/telegram_credentials.json
config/settings.json

# Private monitoring configuration
config/keywords.txt
config/channels.txt
config/channels/

# Databases and runtime data
database/
results/
cache/
media/
videos/

# Temporary files
*.tmp
*.log
.DS_Store
Thumbs.db

# Secrets
.env
.env.*
!.env.example
IGNORE

# ------------------------------------------
# USER DOCUMENTATION - POLISH
# ------------------------------------------

mkdir -p docs

cat > docs/USER_GUIDE_PL.md <<'DOC'
# Telegram Monitor V2 - Instrukcja użytkownika

## 1. Wymagania

- Linux (zalecany Kali Linux lub Debian)
- Python 3
- Git
- Połączenie z Internetem
- Konto Telegram

## 2. Instalacja

Sklonuj repozytorium:

```bash
git clone https://github.com/PawelTOSINT/telegram-monitor-v2.git
cd telegram-monitor-v2
```

Uruchom instalator:

```bash
chmod +x install.sh
./install.sh
```

Instalator samodzielnie:
- tworzy środowisko Python venv,
- instaluje zależności z requirements.txt,
- przygotowuje katalogi konfiguracyjne.

## 3. Uruchamianie programu

```bash
./run.sh
```

Główny plik aplikacji:

`telegram_monitor.py`

Nie uruchamiaj programu przez systemowego Pythona poza środowiskiem venv.

## 4. Konfiguracja Telegram API

1. Wejdź na https://my.telegram.org
2. Zaloguj się na swoje konto Telegram.
3. Otwórz API development tools.
4. Utwórz aplikację.
5. Odczytaj API ID oraz API HASH.
6. Wprowadź dane w konfiguracji wymaganej przez program.

Plik konfiguracyjny:

`config/telegram_credentials.json`

Nie publikuj tego pliku w Internecie.

## 5. Dodawanie keywordów

Plik:

`config/keywords.txt`

Dodawaj po jednym słowie lub frazie w każdym wierszu.

Przykład:

```text
dron
rakieta
artyleria
brat
example
```

Komentarze rozpoczynające się od # są pomijane.

Po zmianie listy uruchom ponownie program lub użyj funkcji aktualizacji keywordów, jeśli jest dostępna w menu.

Silnik keywordów obsługuje:
- polski,
- ukraiński,
- rosyjski,
- angielski,
- tłumaczenia lokalne,
- odmiany morfologiczne,
- transliterację.

## 6. Dodawanie kanałów Telegram

Podstawowy plik:

`config/channels.txt`

Dodawaj identyfikatory lub nazwy publicznych kanałów, po jednym w każdym wierszu.

Przykład:

```text
example_channel
https://t.me/example_channel
```

Używaj kanałów, do których masz dostęp i których monitorowanie jest zgodne z prawem oraz regulaminem Telegrama.

Jeśli projekt zawiera dodatkowe pliki kanałów w katalogu config/channels, zachowaj format wymagany przez daną konfigurację.

## 7. Dodawanie kont użytkownika

Plik:

`config/accounts.json`

Program korzysta z konfiguracji kont Telegrama.

Aby dodać konto:

1. Przygotuj konto Telegram.
2. Uzyskaj API ID i API HASH.
3. Dodaj konto za pomocą mechanizmu konfiguracji obsługiwanego przez program.
4. Zachowaj strukturę JSON używaną przez aplikację.
5. Zapisz konfigurację.
6. Uruchom program i sprawdź połączenie.

Nie kopiuj sesji Telegrama pomiędzy niezaufanymi komputerami.

Każde konto powinno mieć własną sesję.

Nie udostępniaj:
- accounts.json,
- telegram_credentials.json,
- plików *.session,
- API HASH,
- kodów logowania.

## 8. Instalacja modeli tłumaczenia

Opcjonalnie:

```bash
.venv/bin/python install_argos_models.py
```

Modele Argos umożliwiają lokalne tłumaczenie bez korzystania z zewnętrznego API tłumaczeniowego.

## 9. Katalogi projektu

| Katalog | Zastosowanie |
|---|---|
| config | Konfiguracja |
| cache | Cache keywordów |
| database | Baza danych |
| results | Wyniki monitorowania |
| session | Sesje |
| media | Pliki multimedialne |
| videos | Materiały wideo |
| docs | Dokumentacja |

## 10. Rozwiązywanie problemów

Brak venv:

```bash
sudo apt install python3-venv
```

Ponowna instalacja zależności:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

Kontrola składni:

```bash
.venv/bin/python -m compileall -q .
```

## 11. Bezpieczeństwo

Nie publikuj danych uwierzytelniających ani prywatnych sesji.

Przed zgłoszeniem problemu usuń z logów dane osobowe, tokeny i sekrety.
DOC

# ------------------------------------------
# USER DOCUMENTATION - ENGLISH
# ------------------------------------------

cat > docs/USER_GUIDE_EN.md <<'DOC'
# Telegram Monitor V2 - User Guide

## 1. Requirements

- Linux (Kali Linux or Debian recommended)
- Python 3
- Git
- Internet connection
- Telegram account

## 2. Installation

Clone the repository:

```bash
git clone https://github.com/PawelTOSINT/telegram-monitor-v2.git
cd telegram-monitor-v2
```

Run:

```bash
chmod +x install.sh
./install.sh
```

The installer automatically creates a Python virtual environment,
installs requirements and prepares configuration directories.

## 3. Starting the application

```bash
./run.sh
```

Main application:

`telegram_monitor.py`

## 4. Telegram API configuration

Visit:

https://my.telegram.org

Log in, open API development tools and obtain your API ID and API HASH.

Configure them using the application's expected configuration format.

Configuration file:

`config/telegram_credentials.json`

Never publish your credentials.

## 5. Adding keywords

Edit:

`config/keywords.txt`

Add one keyword or phrase per line.

Example:

```text
drone
rocket
artillery
example
```

The keyword engine supports Polish, Ukrainian, Russian and English,
including translations, morphology and transliteration.

## 6. Adding Telegram channels

Edit:

`config/channels.txt`

Add one channel identifier or public channel link per line.

Example:

```text
example_channel
https://t.me/example_channel
```

Only monitor channels you are authorized to access.

## 7. Adding Telegram accounts

Configuration:

`config/accounts.json`

Add accounts using the configuration mechanism supported by the application.
Preserve the JSON structure expected by the program.

Each account should use its own Telegram session.

Never share account credentials or session files.

## 8. Translation models

Optional installation:

```bash
.venv/bin/python install_argos_models.py
```

Argos Translate provides local translation models.

## 9. Troubleshooting

Install Python venv support:

```bash
sudo apt install python3-venv
```

Reinstall dependencies:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

Check Python syntax:

```bash
.venv/bin/python -m compileall -q .
```

## 10. Security

Never publish:
- Telegram credentials
- API HASH
- Account JSON files
- Telegram session files
- Private monitoring configuration

Review logs before sharing them.
DOC

# ------------------------------------------
# README
# ------------------------------------------

cat > README.md <<'DOC'
# Telegram Monitor V2

Telegram monitoring application with multilingual keyword detection.

## Features

- Polish, Ukrainian, Russian and English keyword support
- Keyword translation and expansion
- Morphological variants
- Transliteration
- Telegram channel monitoring
- Local Argos Translate integration
- SQLite database

## Quick start

```bash
git clone https://github.com/PawelTOSINT/telegram-monitor-v2.git
cd telegram-monitor-v2
chmod +x install.sh run.sh
./install.sh
./run.sh
```

The installer automatically creates a Python virtual environment.

## Configuration

- `config/keywords.txt` - keywords
- `config/channels.txt` - Telegram channels
- `config/accounts.json` - Telegram accounts
- `config/telegram_credentials.json` - Telegram API credentials

Private configuration files are excluded from Git.

## Documentation

- [Instrukcja polska](docs/USER_GUIDE_PL.md)
- [English user guide](docs/USER_GUIDE_EN.md)

## Main application

`telegram_monitor.py`

## Translation models

Optional:

```bash
.venv/bin/python install_argos_models.py
```

## Security

Do not publish Telegram credentials, account files or session files.

Use the software responsibly and comply with Telegram's terms and applicable laws.
DOC

# ------------------------------------------
# CHECKS
# ------------------------------------------

echo
echo "[1/5] Sprawdzanie składni Python..."

if command -v python3 >/dev/null; then
    python3 - <<'PY'
import ast
from pathlib import Path

failed = False

for path in sorted(Path(".").glob("*.py")):
    try:
        ast.parse(path.read_text(encoding="utf-8"))
        print("[OK]", path)
    except (SyntaxError, OSError) as exc:
        print("[ERROR]", path, exc)
        failed = True

if failed:
    raise SystemExit(1)
PY
fi

echo
echo "[2/5] Kontrola plików..."

for file in telegram_monitor.py requirements.txt README.md install.sh run.sh; do
    if [ ! -f "$file" ]; then
        echo "[ERROR] Brakuje: $file"
        exit 1
    fi
done

echo
echo "[3/5] Konfiguracja Git..."

if [ ! -d .git ]; then
    git init
fi

git branch -M main

if git remote get-url origin >/dev/null 2>&1; then
    git remote set-url origin "$REPO"
else
    git remote add origin "$REPO"
fi

echo
echo "[4/5] Przygotowanie plików..."

git add -A

echo
echo "Pliki przygotowane do publikacji:"
git status --short

echo
echo "Sprawdź, czy nie ma tu żadnych prywatnych danych."

read -r -p "Czy zatwierdzasz utworzenie commita? [t/N] " answer
if [[ ! "$answer" =~ ^[TtYy]$ ]]; then
    echo "Przerwano. Zmiany pozostają lokalnie."
    exit 0
fi

if git diff --cached --quiet; then
    echo "Brak zmian do zapisania."
else
    git commit -m "Prepare Telegram Monitor V2 with installation and user documentation"
fi

echo
echo "[5/5] Publikacja na GitHub..."

read -r -p "Wysłać projekt do GitHub? [t/N] " answer
if [[ ! "$answer" =~ ^[TtYy]$ ]]; then
    echo "Commit zapisany lokalnie. Publikację możesz wykonać później:"
    echo "git push -u origin main"
    exit 0
fi

git push -u origin main

echo
echo "=========================================="
echo " PUBLIKACJA ZAKOŃCZONA"
echo "=========================================="
echo "Repozytorium:"
echo "$REPO"
echo
echo "Dokumentacja:"
echo "docs/USER_GUIDE_PL.md"
echo "docs/USER_GUIDE_EN.md"
