# Telegram Monitor V3 — Daily Usage Guide

This guide explains how to install, configure, run, and maintain Telegram Monitor.

Repository: https://github.com/PawelTOSINT/telegram-monitor

## 1. Requirements and installation

Requirements:
- Linux
- Python 3
- Internet access
- Your own Telegram API credentials

Clone the repository and install dependencies:

```bash
git clone https://github.com/PawelTOSINT/telegram-monitor.git
cd telegram-monitor
sudo apt install python3-venv
bash install.sh
```

Start the application:

```bash
.venv/bin/python telegram_monitor.py
```

If the application reports missing dependencies, check `requirements.txt` and the installation output.

## 2. Daily startup

Enter the project directory:

```bash
cd ~/telegram-monitor
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Check the available command-line options:

```bash
python3 telegram_monitor.py --help
```

Check application statistics, if supported by the current launcher:

```bash
./start.sh stats
```

## 3. Searching message history

Run the default search:

```bash
./start.sh search
```

Search a recent time period:

```bash
./start.sh search 1
./start.sh search 7
```

The number specifies the requested recent period in days, as supported by the launcher.

To test a keyword:

```bash
./start.sh test "keyword"
```

Use channels and accounts that you are authorized to access.

## 4. Telegram API credentials and accounts

Account configuration is stored locally in:

```text
config/accounts.json
```

Never publish this file or share it with other people.

Each account can contain fields such as:

- `name`
- `api_id`
- `api_hash`
- `enabled`
- `search_enabled`
- `monitor_enabled`

Obtain your own Telegram API credentials from:

https://my.telegram.org/apps

Edit the account configuration:

```bash
nano config/accounts.json
```

Example structure (replace the example values with your own):

```json
{
  "accounts": [
    {
      "name": "account_1",
      "api_id": 123456,
      "api_hash": "YOUR_API_HASH",
      "enabled": true,
      "search_enabled": true,
      "monitor_enabled": true
    }
  ]
}
```

The example credentials above are placeholders, not real credentials.

On the first login, Telegram may request your phone number, a login code, and your two-factor authentication password if enabled.

The application creates local session data. Treat session files as passwords: anyone who obtains an authenticated session may be able to access your account.

Do not upload session files to GitHub.

## 5. Adding Telegram channels

Depending on your configuration, channels can be stored in:

```text
config/channels.txt
config/channels/
```

For a global channel list, edit:

```bash
nano config/channels.txt
```

For an account-specific list, edit the corresponding file, for example:

```bash
nano config/channels/account_1.txt
```

Add one channel link per line:

```text
https://t.me/channel_name
https://t.me/another_channel
```

Use the actual file structure supported by your configuration.

Adding or removing a channel normally does not require rebuilding the keyword cache. Restart the relevant search or monitoring operation after changing the channel list.

## 6. Managing keywords

The main keyword list is:

```text
config/keywords.txt
```

Edit it:

```bash
nano config/keywords.txt
```

After adding, changing, or removing keywords, rebuild the cache:

```bash
python3 telegram_monitor.py --rebuild-cache
```

This operation updates generated keyword data, including language variants, translations, and regular expressions where supported.

You should rebuild the cache after changing:
- Keywords
- Keyword translations
- Language variants
- Generated regular expressions

A channel change, date-range change, or media-download setting change normally does not require a keyword-cache rebuild.

Test a keyword with:

```bash
./start.sh test "keyword"
```

## 7. Continuous monitoring

Start monitoring:

```bash
./start.sh monitor
```

To stop a foreground process, press:

```text
Ctrl+C
```

Before starting a long-running monitoring task, check the configured accounts, channel lists, keywords, and date or media settings.

## 8. Media and reports

Depending on your settings, downloaded files may be stored in:

```text
media/
videos/
```

A media report may be saved as:

```text
results/media.docx
```

Actual output depends on the application's configuration and the messages found.

Media, reports, and databases may contain private or sensitive information. Keep them out of public repositories.

To count files, run:

```bash
find media -type f | wc -l
find videos -type f | wc -l
```

## 9. Backups

Before modifying code or configuration, create a backup.

Back up the main script:

```bash
cp telegram_monitor.py telegram_monitor.py.BACKUP
```

Back up the project directory:

```bash
tar -czf telegram-monitor_BACKUP_$(date +%Y%m%d_%H%M).tar.gz ~/telegram-monitor
```

A full backup may include credentials, authenticated sessions, databases, downloaded media, and reports. Store it securely and never upload it to a public repository.

Verify that a backup exists before making substantial changes.

## 10. Troubleshooting

### The program cannot find a channel

Check:
- The channel link is correct.
- The configured Telegram account can access the channel.
- The channel is listed in the correct configuration file.

For a global channel list:

```bash
cat config/channels.txt
```

### Keyword changes do not take effect

Rebuild the cache:

```bash
python3 telegram_monitor.py --rebuild-cache
```

Then rerun the search or monitoring operation.

### A new account does not work

Check `config/accounts.json` for valid JSON and correct field names. Confirm that the account is enabled and that its API credentials are correct.

Restart the application and complete Telegram login if requested.

### Images or videos are missing

Review the local settings file:

```text
config/settings.json
```

Check the media-download options supported by your version, including `download_media` if present. Also check available disk space and whether the relevant messages contain downloadable media.

### A DOCX report is empty

Check:
- The keywords are configured correctly.
- The cache has been rebuilt after keyword changes.
- The selected channels contain matching messages.
- The configured time range includes the messages you expect.

### Inspecting the database

The database may be located at:

```text
database/telegram_monitor.sqlite
```

If SQLite is installed, you can open it with:

```bash
sqlite3 database/telegram_monitor.sqlite
```

Type `.quit` to exit the SQLite shell.

Do not publish the database: it may contain collected messages or other sensitive data.

## 11. Security checklist

Never publish or share:

- `config/accounts.json`
- `config/telegram_credentials.json`
- Files containing API hashes or other credentials
- The `session/` directory and `.session` files
- Private databases under `database/`
- Downloaded media under `media/` or `videos/`
- Reports and results under `results/`
- Local environment files or personal backups

Before pushing changes to GitHub, review:

```bash
git status --short
git diff --cached --check
git ls-files
```

Remember that `.gitignore` prevents new untracked files from being added by default, but it does not remove files that Git already tracks.

Use only accounts and channels you are authorized to access. Follow Telegram's terms and applicable laws.

## 12. Quick daily checklist

1. Enter the project directory.
2. Activate `.venv`.
3. Check the account and channel configuration.
4. Confirm the keyword list and date range.
5. Run a search or start monitoring.
6. Check the resulting reports and media.
7. Stop continuous monitoring with `Ctrl+C` when finished.
8. Back up important local data securely.

## Documentation

- Polish README: `README.md`
- English README: `README.en.md`
- Polish daily guide: `INSTRUKCJA_CODZIENNEGO_UZYWANIA.md`
- English daily guide: `DAILY_USAGE_GUIDE.en.md`
