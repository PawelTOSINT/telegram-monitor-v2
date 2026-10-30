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
