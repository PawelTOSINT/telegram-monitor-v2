# Telegram Monitor

**Wielojęzyczna platforma OSINT do monitorowania Telegrama**

Telegram Monitor to aplikacja napisana w Pythonie, przeznaczona do legalnego monitorowania kanałów Telegram, przeszukiwania historii wiadomości i wykrywania treści odpowiadających skonfigurowanym słowom kluczowym.

Aplikacja obsługuje przetwarzanie słów kluczowych w języku polskim, ukraińskim, rosyjskim i angielskim.

## Główne funkcje

- Obsługa wielu kont Telegram
- Osobne kanały dla poszczególnych kont
- Przeszukiwanie historii wiadomości
- Ciągły monitoring nowych wiadomości
- Wielojęzyczne wykrywanie słów kluczowych
- Tłumaczenie i rozszerzanie keywordów
- Warianty morfologiczne i transliteracja
- Dopasowywanie za pomocą wyrażeń regularnych
- Opcjonalne lokalne tłumaczenie Argos Translate
- Lokalna baza SQLite
- Generowanie raportów DOCX
- Obsługa i pobieranie multimediów
- Testowanie keywordów i przebudowa cache
- Polski i angielski interfejs

## Wymagania

- Linux (zalecany Kali Linux lub Debian)
- Python 3
- Git
- Obsługa środowisk wirtualnych Python
- Połączenie z Internetem
- Konto Telegram i dane Telegram API

## Instalacja

Sklonuj repozytorium:

```bash
git clone https://github.com/PawelTOSINT/telegram-monitor-v2.git
cd telegram-monitor-v2
```

Zainstaluj wymagane pakiety systemowe:

```bash
sudo apt update
sudo apt install python3 python3-venv git
```

Uruchom instalator:

```bash
chmod +x install.sh run.sh
./install.sh
```

Instalator tworzy środowisko wirtualne Python, instaluje zależności i przygotowuje katalogi aplikacji.

Istniejące pliki konfiguracyjne nie są nadpisywane przez instalator.

## Konfiguracja

Pliki konfiguracyjne znajdują się w katalogu `config/`.

### Dane Telegram API

Dane API ID oraz API HASH uzyskasz na stronie:

https://my.telegram.org

Wprowadź je do pliku:

`config/telegram_credentials.json`

### Konta Telegram

Konta konfiguruje się w pliku:

`config/accounts.json`.

Przykładowa struktura:

```json
{
  "accounts": [
    {
      "name": "konto_1",
      "api_id": 123456,
      "api_hash": "TWOJ_API_HASH",
      "search_enabled": true,
      "monitor_enabled": true
    }
  ]
}
```

Kanały przypisane do konkretnego konta znajdują się w pliku:

`config/channels/konto_1.txt`

Zastąp `konto_1` odpowiednią nazwą konta.

Aplikacja obsługuje również ustawienie `enabled`, które pozwala aktywować lub wyłączyć konto.

### Słowa kluczowe

Plik:

`config/keywords.txt`

Dodawaj jedno słowo lub frazę w każdym wierszu.

### Ustawienia

Język interfejsu konfiguruje się w:

`config/settings.json`.

Przykładowa konfiguracja wykorzystuje język polski (`pl`).

### Zakres dat wyszukiwania

Opcjonalny zakres dat można skonfigurować w:

`config/time_range.json`.

Przykład:

```json
{
  "from": "2026-01-01",
  "to": "2026-12-31"
}
```

## Uruchamianie aplikacji

Wszystkie polecenia należy wykonywać przez `run.sh`.

Pomoc:

```bash
./run.sh --help
```

Przeszukiwanie historii wiadomości:

```bash
./run.sh --search
```

Wyszukiwanie z ostatnich trzech dni:

```bash
./run.sh --search --days 3
```

Ciągły monitoring:

```bash
./run.sh --monitor
```

Statystyki bazy danych:

```bash
./run.sh --stats
```

Test słowa kluczowego:

```bash
./run.sh --test-keyword "brat"
```

Ponowne generowanie cache:

```bash
./run.sh --rebuild-cache
```

Aby zatrzymać ciągły monitoring, naciśnij `Ctrl+C`.

## Baza danych i raporty

Aplikacja wykorzystuje lokalną bazę SQLite.

Baza zawiera między innymi:

- `messages` – rekordy wiadomości i dopasowania słów kluczowych;
- `media_documents` – informacje wykorzystywane do zapobiegania duplikatom w globalnym raporcie multimedialnym.

Aplikacja generuje również dokumenty DOCX i obsługuje przetwarzanie obsługiwanych typów multimediów.

## Opcjonalne modele tłumaczeniowe

Instalacja modeli Argos Translate:

```bash
.venv/bin/python install_argos_models.py
```

Dostępność tłumaczenia zależy od zainstalowanych modeli i obsługiwanych par językowych.

## Rozwiązywanie problemów

Sprawdzenie składni Pythona:

```bash
.venv/bin/python -m compileall -q .
```

Ponowna instalacja zależności:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

Instalacja obsługi środowisk wirtualnych:

```bash
sudo apt install python3-venv
```

## Bezpieczeństwo

Nigdy nie publikuj:

- Telegram API HASH
- Prywatnych konfiguracji kont
- Plików sesji Telegram
- Kodów uwierzytelniających
- Prywatnych konfiguracji monitorowania
- Baz danych ani zebranych danych zawierających informacje poufne

Przed publikacją zmian sprawdź `.gitignore`.

Monitoruj wyłącznie kanały i informacje, do których masz odpowiednie uprawnienia.

## Dokumentacja

- [English README](README.md)
- [Instrukcja użytkownika PL](docs/USER_GUIDE_PL.md)
- [English User Guide](docs/USER_GUIDE_EN.md)
- [Instrukcja codziennego używania PL](INSTRUKCJA_CODZIENNEGO_UZYWANIA.md)
- [Daily Usage Guide EN](DAILY_USAGE_GUIDE.en.md)

## Zastrzeżenie

Oprogramowanie jest przeznaczone do legalnych badań i monitorowania, do którego użytkownik posiada odpowiednie uprawnienia.

Użytkownik odpowiada za przestrzeganie obowiązujących przepisów prawa, regulacji dotyczących prywatności oraz regulaminu Telegrama.

## Repozytorium

https://github.com/PawelTOSINT/telegram-monitor-v2
