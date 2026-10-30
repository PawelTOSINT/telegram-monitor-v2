# Telegram Monitor V2

Advanced Multilingual Telegram OSINT Monitoring Platform

A Python-based OSINT tool for monitoring Telegram channels, identifying relevant messages and analyzing keywords in Polish, Ukrainian, Russian and English.

## Key Features
- Multilingual keyword detection (PL / UK / RU / EN)
- Automatic translations with Argos Translate
- Morphological analysis and keyword expansion
- Regex matching and transliteration
- Multiple Telegram account support
- Configurable channel monitoring
- Automated keyword generation

## Installation
bash
git clone https://github.com/PawelTOSINT/telegram-monitor-v2.git
cd telegram-monitor-v2
./install.sh


## Configuration
Configure Telegram credentials, accounts, channels and keywords using the example files in config/. Never publish private credentials or session files.

## Running
bash
./run.sh


## Documentation
- English User Guide
- Polish User Guide
- Daily Usage Guide

## Technology
Python 3, Telethon, Argos Translate, Pymorphy3, Morfeusz2 and Lingua.

## Disclaimer
For lawful OSINT research and authorized monitoring. Users are responsible for complying with applicable laws and Telegram Terms of Service.

## Repository
https://github.com/PawelTOSINT/telegram-monitor-v2

---

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
