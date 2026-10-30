# Telegram Monitor

Narzędzie Python do wyszukiwania i monitorowania wiadomości Telegram
według skonfigurowanych słów kluczowych.

## Wymagania
- Linux
- Python 3
- Dostęp do internetu
- Własne dane API Telegrama

## Instalacja

```bash
git clone https://github.com/PawelTOSINT/telegram-monitor.git
cd telegram-monitor
sudo apt install python3-venv
bash install.sh
```

## Konfiguracja

1. Uzupełnij własne dane API Telegrama w lokalnych plikach konfiguracyjnych.
2. Nie udostępniaj plików z tokenami, hasłami ani sesjami.
3. Skonfiguruj słowa kluczowe i pozostałe ustawienia zgodnie z potrzebami.

## Uruchomienie

```bash
.venv/bin/python telegram_monitor.py
```

## Bezpieczeństwo

Konfiguracja, sesje, bazy danych i wyniki lokalne nie powinny być
publikowane w repozytorium. Przed wysłaniem kodu sprawdź `.gitignore`.
