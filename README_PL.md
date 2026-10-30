# Telegram Monitor V2

**Wielojęzyczna platforma OSINT do monitorowania Telegrama**

Telegram Monitor V2 to narzędzie napisane w Pythonie, przeznaczone do monitorowania kanałów Telegram i wykrywania wiadomości zawierających istotne słowa kluczowe w wielu językach.

## Główne funkcje

- Wielojęzyczne monitorowanie słów kluczowych (polski, ukraiński, rosyjski i angielski)
- Dopasowywanie słów kluczowych i analiza tekstu
- Transliteracja i warianty słów kluczowych
- Konfigurowalne monitorowanie kanałów Telegram
- Konfiguracja kont Telegram
- Lokalny zapis danych
- Obsługa bazy danych SQLite

## Szybki start

Pobierz repozytorium i uruchom instalator:

```bash
git clone https://github.com/PawelTOSINT/telegram-monitor-v2.git
cd telegram-monitor-v2
chmod +x install.sh run.sh
./install.sh
```

Skonfiguruj dane Telegram, kanały i słowa kluczowe w katalogu `config/`.

Uruchom aplikację:

```bash
./run.sh
```

Szczegółowe informacje znajdują się w sekcji [Instalacja](#instalacja).

## Wymagania

- Linux (zalecany Kali Linux lub Debian)
- Python 3
- Git
- Obsługa środowisk wirtualnych Python
- Połączenie z Internetem
- Konto Telegram

## Instalacja

### Pakiety systemowe

W Kali Linux lub Debianie:

```bash
sudo apt update
sudo apt install python3 python3-venv git
```

### Automatyczna instalacja

Po pobraniu repozytorium uruchom:

```bash
./install.sh
```

Instalator przygotowuje środowisko Python i instaluje zależności projektu. Może również tworzyć wymagane katalogi i pliki konfiguracyjne na podstawie dostępnych szablonów.

Istniejące pliki konfiguracyjne powinny zostać zachowane.

### Ręczna instalacja zależności

Jeżeli środowisko wirtualne już istnieje:

```bash
.venv/bin/python -m pip install -r requirements.txt
```

## Konfiguracja

Pliki konfiguracyjne znajdują się w katalogu `config/`.

Przed uruchomieniem zapoznaj się z szablonami konfiguracji dostępnymi w repozytorium.

Typowe obszary konfiguracji:

- Dane dostępowe Telegram API
- Konta Telegram
- Kanały do monitorowania
- Słowa kluczowe i frazy
- Ustawienia monitorowania

### Dane dostępowe Telegram API

1. Wejdź na https://my.telegram.org.
2. Zaloguj się na swoje konto Telegram.
3. Otwórz API development tools.
4. Pobierz API ID oraz API HASH.
5. Wprowadź dane w odpowiednim pliku konfiguracyjnym.

Nigdy nie publikuj API HASH, danych dostępowych ani plików sesji.

### Słowa kluczowe i kanały

Korzystaj z szablonów konfiguracji dostępnych w repozytorium. Zachowaj ich istniejący format podczas dodawania słów kluczowych i identyfikatorów kanałów.

Monitoruj wyłącznie kanały, do których masz uprawniony dostęp.

## Uruchamianie aplikacji

Uruchom Telegram Monitor V2:

```bash
./run.sh
```

Korzystaj z aplikacji zgodnie z dokumentacją projektu.

## Opcjonalne modele tłumaczeniowe

Jeżeli obsługuje je zainstalowana wersja projektu:

```bash
.venv/bin/python install_argos_models.py
```

## Rozwiązywanie problemów

### Brak obsługi środowisk wirtualnych Python

```bash
sudo apt install python3-venv
```

### Ponowna instalacja zależności

```bash
.venv/bin/python -m pip install -r requirements.txt
```

### Sprawdzenie składni Pythona

```bash
.venv/bin/python -m compileall -q .
```

## Bezpieczeństwo

Nigdy nie publikuj ani nie udostępniaj:

- Danych dostępowych Telegram API
- API HASH
- Plików sesji Telegram
- Kodów uwierzytelniających
- Prywatnej konfiguracji kont

Przed udostępnieniem logów usuń z nich informacje poufne.

## Zastrzeżenie

Telegram Monitor V2 jest przeznaczony do legalnych badań OSINT i monitorowania, do którego użytkownik posiada odpowiednie uprawnienia.

Użytkownik odpowiada za przestrzeganie obowiązujących przepisów prawa, regulacji dotyczących prywatności oraz regulaminu Telegrama.

## Dokumentacja

- [English README](README.md)
- [Repozytorium](https://github.com/PawelTOSINT/telegram-monitor-v2)
