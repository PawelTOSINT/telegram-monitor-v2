# Telegram Monitor

**Multilingual Telegram OSINT Monitoring Platform**

Telegram Monitor is a Python application for authorized monitoring of Telegram channels, searching message history and identifying messages matching configured keywords.

The application supports Polish, Ukrainian, Russian and English keyword processing.

## Features

- Multiple Telegram account support
- Account-specific channel configuration
- Historical message search
- Continuous monitoring of new messages
- Multilingual keyword detection
- Keyword translation and expansion
- Morphological variants and transliteration
- Regex-based keyword matching
- OPTIONAL local translation using Argos Translate (install it yourself: .venv/bin/python install_argos_models.py)
- SQLite database
- DOCX reports
- Media processing and downloads
- Keyword testing and cache rebuilding
- Polish and English interface

## Requirements

- Linux (Kali Linux or Debian recommended)
- Python 3
- Git
- Python virtual environment support
- Internet connection
- Telegram account and Telegram API credentials

## Installation

Clone the repository:

```bash
git clone https://github.com/PawelTOSINT/telegram-monitor-v2.git
cd telegram-monitor-v2
```

Install system requirements:

```bash
sudo apt update
sudo apt install python3 python3-venv git
```

Run the installer:

```bash
chmod +x install.sh run.sh
./install.sh
```

The installer creates a Python virtual environment, installs dependencies and prepares application directories.

Existing configuration files are not overwritten by the installer.

## Configuration

Configuration files are stored in `config/`.

### Telegram API credentials

Obtain your API ID and API HASH from:

https://my.telegram.org

Configure them in:

`config/telegram_credentials.json`

### Telegram accounts

Configure accounts in:

`config/accounts.json`.

Example structure:

```json
{
  "accounts": [
    {
      "name": "account_1",
      "api_id": 123456,
      "api_hash": "YOUR_API_HASH",
      "search_enabled": true,
      "monitor_enabled": true
    }
  ]
}
```

Account-specific channels are stored in:

`config/channels/account_1.txt`

Replace `account_1` with the corresponding account name.

The application also supports account activation through the `enabled` setting.

### Keywords

Configure keywords in:

`config/keywords.txt`

Use one keyword or phrase per line.

### Settings

The interface language is configured in:

`config/settings.json`.

The example configuration uses Polish (`pl`).

### Search date range

The optional date range is configured in:

`config/time_range.json`.

Example:

```json
{
  "from": "2026-01-01",
  "to": "2026-12-31"
}
```

## Running the application

All commands should be executed through `run.sh`.

Display help:

```bash
./run.sh --help
```

Search historical messages:

```bash
./run.sh --search
```

Search the last three days:

```bash
./run.sh --search --days 3
```

Continuous monitoring:

```bash
./run.sh --monitor
```

Display database statistics:

```bash
./run.sh --stats
```

Test a keyword:

```bash
./run.sh --test-keyword "brother"
```

Rebuild keyword cache:

```bash
./run.sh --rebuild-cache
```

Press `Ctrl+C` to stop continuous monitoring.

## Database and reports

The application uses SQLite for local message storage.

The database includes:

- `messages` – message records and keyword matches
- `media_documents` – records used to prevent duplicate entries in the global media report

The application also generates DOCX documents and processes supported media.

## Optional translation models

Install optional Argos Translate models:

```bash
.venv/bin/python install_argos_models.py
```

Translation functionality depends on installed models and available language pairs.

## Troubleshooting

Check Python syntax:

```bash
.venv/bin/python -m compileall -q .
```

Reinstall dependencies:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

Install virtual environment support:

```bash
sudo apt install python3-venv
```

## Security

Never publish:

- Telegram API HASH
- Private account configurations
- Telegram session files
- Authentication codes
- Private monitoring configurations
- Databases or collected data containing sensitive information

Review `.gitignore` before publishing changes.

Monitor only channels and information you are authorized to access.

## Documentation

- [Polish README](README_PL.md)
- [English User Guide](docs/USER_GUIDE_EN.md)
- [Polish User Guide](docs/USER_GUIDE_PL.md)
- [Daily Usage Guide](DAILY_USAGE_GUIDE.en.md)
- [Polish Daily Usage Guide](INSTRUKCJA_CODZIENNEGO_UZYWANIA.md)

## Disclaimer

This software is intended for lawful research and authorized monitoring.

Users are responsible for complying with applicable laws, privacy requirements and Telegram Terms of Service.

## Repository

https://github.com/PawelTOSINT/telegram-monitor-v2
