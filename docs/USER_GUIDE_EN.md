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
