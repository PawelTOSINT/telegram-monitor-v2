#!/usr/bin/env bash

cd "$(dirname "$0")"

source .venv/bin/activate

case "$1" in

    search)
        python keyword_engine.py

        if [ -n "$2" ]; then
            python telegram_monitor.py --search --days "$2"
        else
            python telegram_monitor.py --search
        fi
        ;;

    monitor)
        python keyword_engine.py
        python telegram_monitor.py --monitor
        ;;

    stats)
        python telegram_monitor.py --stats
        ;;

    test)
        if [ -z "$2" ]; then
            echo 'Użycie: ./start.sh test "brat"'
            exit 1
        fi

        python -c "
from keyword_engine import get_keyword
import json

x = get_keyword('$2')

print()
print('=' * 70)
print('KEYWORD:', x['keyword'])
print('JĘZYK:', x['detected_language'])
print()
print('PL:', ', '.join(x['languages']['pl']))
print('UK:', ', '.join(x['languages']['uk']))
print('RU:', ', '.join(x['languages']['ru']))
print('EN:', ', '.join(x['languages']['en']))
print()
print('LICZBA WARIANTÓW:', len(x['variants']))
print()
print('WARIANTY:')
for v in x['variants']:
    print(' ', v)
print()
print('REGEX:')
print(x['regex'])
"

        ;;

    help|*)
        echo
        echo "TELEGRAM MONITOR"
        echo
        echo "./start.sh search"
        echo "  przeszukuje zakres z config/time_range.json"
        echo
        echo "./start.sh search 3"
        echo "  przeszukuje ostatnie 3 dni"
        echo
        echo "./start.sh search 7"
        echo "  przeszukuje ostatnie 7 dni"
        echo
        echo "./start.sh monitor"
        echo "  monitoruje nowe wiadomości"
        echo
        echo './start.sh test "brat"'
        echo "  testuje keyword"
        echo
        echo "./start.sh stats"
        echo "  statystyki"
        echo
        ;;
esac
