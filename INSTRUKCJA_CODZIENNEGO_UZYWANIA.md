# Telegram Monitor V3 - Instrukcja codziennego uzytkowania

## 1. Codzienny start programu

Wejscie do katalogu:
cd ~/telegram-monitor

Aktywacja srodowiska:
source .venv/bin/activate

Sprawdzenie programu:
python3 telegram_monitor.py --help

## 2. Wyszukiwanie historii

Domyslne wyszukiwanie:
./start.sh search

Ostatnie dni:
./start.sh search 1
./start.sh search 7

---

## 3. Dodawanie konta Telegram

Konfiguracja kont znajduje sie w:
config/accounts.json

Nie udostepniac tego pliku publicznie.

Kazde konto posiada:
- name
- api_id
- api_hash
- enabled
- search_enabled
- monitor_enabled

Przy pierwszym uruchomieniu nowego konta Telegram program utworzy sesje.

## 4. Dodawanie kanalu

Kanaly znajduja sie w:
config/channels/

Przyklad:
config/channels/konto_1.txt

Dodanie kanalu:
https://t.me/nazwa_kanalu

Po dodaniu kanalu nie trzeba robic rebuild-cache.
Uruchom tylko wyszukiwanie:
./start.sh search 1

---

## 5. Keywordy i cache

Lista keywordow znajduje sie w:
config/keywords.txt

Po kazdej zmianie keywordow trzeba wykonac:

python3 telegram_monitor.py --rebuild-cache

Dotyczy to:
- dodania keywordu
- zmiany keywordu
- usuniecia keywordu
- zmiany tlumaczen keywordow

Rebuild-cache wykonuje:
- aktualizacje tlumaczen
- generowanie wariantow jezykowych
- generowanie regex
- usuwanie starych wpisow cache

Po zmianie keywordu mozna wykonac test:
./start.sh test "keyword"

Zmiany, ktore NIE wymagaja rebuild-cache:
- dodanie kanalu
- usuniecie kanalu
- zmiana ustawien pobierania mediow
- zmiana zakresu dat

---

## 6. Media i raporty DOCX

Pobrane pliki znajduja sie w:
media/

Video znajduja sie w:
videos/

Raport wszystkich mediow:
results/media.docx

Program zapisuje media na biezaco.
Po przerwaniu programu Ctrl+C nie powinny byc tracone zapisane juz wpisy.

## 7. Backup programu

Przed zmianami w kodzie wykonaj backup:

cp telegram_monitor.py telegram_monitor.py.BACKUP_DATA

Pelna kopia katalogu:

tar -czf telegram-monitor_BACKUP_DATA.tar.gz telegram-monitor/

## 8. Diagnostyka problemow

Sprawdzenie czy program dziala:
ps aux | grep telegram-monitor

Sprawdzenie liczby mediow:
find media -type f | wc -l

Sprawdzenie video:
find videos -type f | wc -l

Sprawdzenie bazy mediow:
sqlite3 database/telegram_monitor.sqlite

---

## 9. Codzienna checklista

START:
1. Wejdz do katalogu programu:
cd ~/telegram-monitor

2. Aktywuj srodowisko:
source .venv/bin/activate

3. Sprawdz konfiguracje kanalow i keywordow.

PRACA:
./start.sh search 1

lub monitoring ciagly:
./start.sh monitor

KONIEC PRACY:
Zatrzymanie monitoringu:
CTRL+C

## 10. Bezpieczenstwo

Nigdy nie udostepniac:
- config/accounts.json
- config/telegram_credentials.json
- katalog session/
- plikow .session
- database/
- media/
- videos/
- results/

Publiczne repo GitHub powinno zawierac tylko kod i pliki example.
# 11. Zarządzanie konfiguracją

## 11.1 Dodawanie nowego konta Telegram

Konta Telegram znajdują się w pliku:

```
config/accounts.json
```

Przejdź do katalogu programu:

```
cd ~/telegram-monitor
```

Edytuj plik:

```
nano config/accounts.json
```

Dodaj nowe konto w sekcji `accounts`.

Przykład:

```json
{
  "accounts": [
    {
      "name": "konto_1",
      "api_id": 123456,
      "api_hash": "HASH_KONTA_1",
      "enabled": true,
      "search_enabled": true,
      "monitor_enabled": true
    },
    {
      "name": "konto_2",
      "api_id": 654321,
      "api_hash": "HASH_KONTA_2",
      "enabled": true,
      "search_enabled": true,
      "monitor_enabled": true
    }
  ]
}
```

Każde konto musi mieć:

* unikalną nazwę `name`,
* własne lub przypisane dane API Telegram,
* włączone opcje działania.

Dane API Telegram pobiera się ze strony:

```
https://my.telegram.org/apps
```

Przy pierwszym uruchomieniu nowego konta program poprosi o:

* numer telefonu,
* kod logowania Telegram,
* hasło 2FA (jeżeli jest ustawione).

Program utworzy osobną sesję:

```
session/
├── konto_1/
│   └── telegram.session
└── konto_2/
    └── telegram.session
```

Po dodaniu konta NIE trzeba wykonywać rebuild cache.

---

# 11.2 Dodawanie nowego kanału Telegram

Kanały są przechowywane w katalogu:

```
config/channels/
```

Każde konto ma własny plik kanałów.

Przykład:

```
config/channels/konto_1.txt
```

Edytowanie:

```
nano config/channels/konto_1.txt
```

Dodaj link kanału:

```
https://t.me/nazwa_kanalu
```

Można dodać wiele kanałów:

```
https://t.me/kanal_1
https://t.me/kanal_2
https://t.me/kanal_3
```

Po zmianie kanałów:

* nie trzeba robić rebuild cache,
* można ponownie uruchomić monitor.

Przykład:

```
./start.sh monitor
```

---

# 11.3 Zmiana keywordów

Keywordy znajdują się w:

```
config/keywords.txt
```

Edytowanie:

```
nano config/keywords.txt
```

Po dodaniu nowego keywordu należy przebudować cache:

```
python3 telegram_monitor.py --rebuild-cache
```

Powoduje to:

* ponowne wygenerowanie wariantów,
* odświeżenie tłumaczeń,
* przebudowanie regexów.

Po zmianie keywordów zawsze wykonuj:

```
--rebuild-cache
```

---

# 11.4 Usuwanie keywordów

Aby usunąć keyword:

1. Usuń go z:

```
config/keywords.txt
```

2. Przebuduj cache:

```
python3 telegram_monitor.py --rebuild-cache
```

Po tej operacji program przestanie używać usuniętego keywordu.

Uwaga:

* stare raporty DOCX pozostają,
* wcześniej pobrane media pozostają,
* historia w bazie pozostaje.

Jeżeli chcesz całkowicie usunąć stare wyniki, wykonaj osobną kopię bezpieczeństwa i usuń katalog wyników.

---

# 11.5 Kiedy wykonywać rebuild cache

## NIE trzeba wykonywać:

Po zmianie:

* konta Telegram,
* kanałów,
* trybu monitorowania,
* ustawień pobierania mediów.

## Trzeba wykonać:

Po zmianie:

* keywordów,
* tłumaczeń keywordów,
* wariantów językowych,
* regexów.

Polecenie:

```
python3 telegram_monitor.py --rebuild-cache
```

---

# 11.6 Typowa codzienna obsługa

Uruchomienie:

```
cd ~/telegram-monitor
source .venv/bin/activate
```

Sprawdzenie działania:

```
./start.sh stats
```

Uruchomienie wyszukiwania:

```
./start.sh search
```

Wyszukiwanie ostatnich dni:

```
./start.sh search 7
```

Uruchomienie ciągłego monitorowania:

```
./start.sh monitor
```

Test keywordu:

```
./start.sh test "keyword"
```

---

# 11.7 Przed większymi zmianami

Przed zmianą kodu lub konfiguracji wykonaj backup:

```
tar -czf telegram-monitor_BACKUP_$(date +%Y%m%d_%H%M).tar.gz ~/telegram-monitor
```

Nie usuwaj backupów, dopóki nowa wersja nie zostanie sprawdzona.
# 11. Zarządzanie konfiguracją programu

## 11.1 Dodawanie nowego konta Telegram

Konta Telegram znajdują się w:

config/accounts.json

Edytowanie:

cd ~/telegram-monitor
nano config/accounts.json

Przykład drugiego konta:

{
  "accounts": [
    {
      "name": "konto_1",
      "api_id": 123456,
      "api_hash": "HASH_1",
      "enabled": true,
      "search_enabled": true,
      "monitor_enabled": true
    },
    {
      "name": "konto_2",
      "api_id": 654321,
      "api_hash": "HASH_2",
      "enabled": true,
      "search_enabled": true,
      "monitor_enabled": true
    }
  ]
}

Po dodaniu konta:
- program przy pierwszym użyciu poprosi o logowanie Telegram,
- zostanie utworzona nowa sesja,
- nie wykonuje się rebuild cache.

Sesje znajdują się w:

session/

---

## 11.2 Dodawanie kanału Telegram

Program obsługuje kanały globalne oraz kanały przypisane do konkretnego konta.

### Kanały globalne

Plik:

config/channels.txt

Edytowanie:

nano config/channels.txt

Dodaj link kanału:

https://t.me/nazwa_kanalu


### Kanały dla konkretnego konta

Przy obsłudze wielu kont można używać osobnych plików:

config/channels/<nazwa_konta>.txt

Przykład:

config/channels/konto_1.txt


Po zmianie kanałów:

- nie wykonuje się rebuild cache,
- wystarczy ponownie uruchomić program.

Przykład:

./start.sh monitor


## 11.3 Zmiana keywordów

Keywordy znajdują się w:

config/keywords.txt

Po dodaniu lub zmianie keywordu należy wykonać:

python3 telegram_monitor.py --rebuild-cache

Rebuild cache wykonuje:
- generowanie wariantów,
- aktualizację tłumaczeń,
- przebudowę regexów.

---

## 11.4 Usuwanie keywordów

Aby usunąć keyword:

1. Usuń wpis z:

config/keywords.txt

2. Wykonaj:

python3 telegram_monitor.py --rebuild-cache

Usunięcie keywordu usuwa go z aktualnego mechanizmu wyszukiwania.

Nie usuwa:
- istniejących raportów DOCX,
- pobranych zdjęć i video,
- zapisów w bazie.

---

## 11.5 Kiedy używać rebuild cache

NIE używać po zmianie:

- kont Telegram,
- kanałów,
- ustawień pobierania mediów.

Używać po zmianie:

- keywordów,
- tłumaczeń,
- wariantów językowych,
- regexów.

Polecenie:

python3 telegram_monitor.py --rebuild-cache

---

## 11.6 Codzienne uruchamianie

Start:

cd ~/telegram-monitor
source .venv/bin/activate

Sprawdzenie:

./start.sh stats

Wyszukiwanie:

./start.sh search

Ostatnie dni:

./start.sh search 7

Monitoring na żywo:

./start.sh monitor

Test keywordu:

./start.sh test "keyword"

---

## 11.7 Backup przed zmianami

Przed większymi zmianami wykonaj:

tar -czf telegram-monitor_BACKUP_$(date +%Y%m%d_%H%M).tar.gz ~/telegram-monitor

Backup zachowuje:
- kod,
- konfigurację,
- bazę,
- cache,
- wyniki.


# 12. Diagnostyka problemów

## 12.1 Program nie widzi nowego kanału

Sprawdź:
- czy kanał jest poprawnie zapisany,
- czy konto Telegram ma dostęp,
- czy link jest poprawny.

Kanały globalne:

cat config/channels.txt


## 12.2 Zmiana keywordów

Po dodaniu, zmianie lub usunięciu keywordu wykonaj:

python3 telegram_monitor.py --rebuild-cache


## 12.3 Dodanie nowego konta Telegram

Po zmianie:

config/accounts.json

uruchom program ponownie.

Nowa sesja zostanie utworzona automatycznie.


## 12.4 Brak zdjęć lub video

Sprawdź:

config/settings.json

Opcje:

download_media

download_media_without_keyword


## 12.5 Pusty raport DOCX

Sprawdź:
- czy keyword istnieje,
- czy cache został przebudowany,
- czy kanał zawiera pasujące wiadomości.


## 12.6 Backup przed zmianami

Wykonaj:

tar -czf telegram-monitor_BACKUP_$(date +%Y%m%d_%H%M).tar.gz ~/telegram-monitor
