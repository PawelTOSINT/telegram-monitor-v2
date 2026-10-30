#!/usr/bin/env python3

import json
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CONFIG_DIR = BASE_DIR / "config"

KEYWORDS_FILE = CONFIG_DIR / "keywords.txt"
TRANSLATIONS_FILE = CONFIG_DIR / "keyword_translations.json"

LANGUAGES = ["pl", "uk", "ru", "en"]
LANGUAGE_CODES = set(LANGUAGES)


def load_json(path, default):
    if not path.exists():
        return default

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[JSON ERROR] {path}: {e}")
        return default


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2,
        )


def load_keywords():
    if not KEYWORDS_FILE.exists():
        return []

    result = []

    with open(KEYWORDS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if line not in result:
                result.append(line)

    return result


def normalize(value):
    if value is None:
        return ""

    value = str(value).strip()
    value = re.sub(r"\s+", " ", value)

    return value


def valid_variant(value):
    """
    Sprawdza, czy tekst może być prawdziwym wariantem keywordu.
    Kodów językowych typu 'en' nie dopuszczamy.
    """
    value = normalize(value)

    if not value:
        return False

    if value.lower() in LANGUAGE_CODES:
        return False

    return True


# ============================================================
# DETEKCJA JĘZYKA
# ============================================================

def detect_by_pymorphy(text):
    """
    Próbuje rozpoznać krótkie słowa za pomocą pymorphy3.

    To ważne dla słów takich jak:
        mamusia
        brat
        dom
        example

    które mogą być zapisane alfabetem łacińskim
    bez znaków charakterystycznych dla polskiego.
    """

    word = normalize(text).lower()

    if not word:
        return None

    # pymorphy najlepiej działa na pojedynczych słowach
    if " " in word:
        return None

    # --------------------------------------------------------
    # POLSKI
    # --------------------------------------------------------
    try:
        import pymorphy3

        morph = pymorphy3.MorphAnalyzer(
            lang="uk"
        )
    except Exception:
        morph = None

    # pymorphy3 nie zawsze posiada jeden wspólny
    # mechanizm dla wszystkich języków.
    # Spróbujemy osobno polski/ukraiński/rosyjski.

    analyzers = []

    try:
        import pymorphy3

        for lang in ("pl", "uk", "ru"):
            try:
                analyzer = pymorphy3.MorphAnalyzer(
                    lang=lang
                )
                analyzers.append((lang, analyzer))
            except Exception:
                pass

    except Exception:
        return None

    scores = {
        "pl": 0,
        "uk": 0,
        "ru": 0,
    }

    for lang, analyzer in analyzers:
        try:
            parses = analyzer.parse(word)

            if parses:
                # Im więcej wiarygodnych analiz,
                # tym większy sygnał.
                scores[lang] += min(
                    len(parses),
                    5
                )

                # Normalna forma słownikowa.
                for parse in parses[:5]:
                    normal_form = getattr(
                        parse,
                        "normal_form",
                        ""
                    )

                    if normal_form:
                        scores[lang] += 1

        except Exception:
            pass

    best = max(
        scores,
        key=scores.get
    )

    if scores[best] > 0:
        # Nie ufamy jednak samemu wynikowi,
        # jeżeli wszystkie języki dały praktycznie
        # identyczny wynik.
        ordered = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        if len(ordered) >= 2:
            first_score = ordered[0][1]
            second_score = ordered[1][1]

            if (
                first_score == second_score
                and first_score > 0
            ):
                return None

        return best

    return None


def detect_language(text):
    text = normalize(text)

    if not text:
        return "en"

    lower = text.lower()

    # --------------------------------------------------------
    # Najpierw jednoznaczne alfabety
    # --------------------------------------------------------

    # Ukraiński
    if re.search(r"[іїєґ]", lower):
        return "uk"

    # Cyrylica rosyjska bez typowych ukraińskich znaków
    if re.search(r"[ёыэъ]", lower):
        return "ru"

    # Jeżeli jest cyrylica i brak ukraińskich znaków,
    # domyślnie rosyjski.
    if re.search(r"[а-я]", lower):
        return "ru"

    # --------------------------------------------------------
    # Polski
    # --------------------------------------------------------

    if re.search(r"[ąćęłńóśźż]", lower):
        return "pl"

    # --------------------------------------------------------
    # Krótkie polskie słowa bez znaków diakrytycznych.
    # --------------------------------------------------------

    known_polish = {
        "mamusia",
        "mama",
        "matka",
        "brat",
        "siostra",
        "ojciec",
        "tata",
        "syn",
        "córka",
        "dom",
        "example",
        "exampley",
        "rakieta",
        "rakiety",
        "pocisk",
        "pociski",
        "wojsko",
        "żołnierz",
        "żołnierze",
        "granat",
        "granaty",
        "samolot",
        "helikopter",
        "śmigłowiec",
        "bezpilotnik",
        "bezzałogowiec",
        "artyleria",
    }

    if lower in known_polish:
        return "pl"

    # --------------------------------------------------------
    # Morfologia
    # --------------------------------------------------------

    detected = detect_by_pymorphy(lower)

    if detected:
        return detected

    # --------------------------------------------------------
    # Fallback
    # --------------------------------------------------------

    return "en"


# ============================================================
# ARGOS TRANSLATE
# ============================================================

def try_import_argos():
    try:
        import argostranslate.translate
        return True
    except ImportError:
        return False


MANUAL_TRANSLATIONS = {
    ("example", "pl", "uk"): "дрон",
}


def get_translation(text, source, target):
    text = normalize(text)

    if not text:
        return None

    if source == target:
        return text

    manual = MANUAL_TRANSLATIONS.get(
        (text.casefold(), source, target)
    )

    if manual:
        return manual

    try:
        import argostranslate.translate

        installed = (
            argostranslate.translate
            .get_installed_languages()
        )

        source_lang = next(
            (
                language
                for language in installed
                if language.code == source
            ),
            None,
        )

        target_lang = next(
            (
                language
                for language in installed
                if language.code == target
            ),
            None,
        )

        if not source_lang:
            print(
                f"[ARGOS] Brak języka źródłowego: "
                f"{source}"
            )
            return None

        if not target_lang:
            print(
                f"[ARGOS] Brak języka docelowego: "
                f"{target}"
            )
            return None

        translation = source_lang.get_translation(
            target_lang
        )

        if not translation:
            print(
                f"[ARGOS] Brak modelu "
                f"{source}->{target}"
            )
            return None

        result = translation.translate(
            text
        )

        result = normalize(result)

        if not valid_variant(result):
            return None

        return result

    except Exception as e:
        print(
            f"[TRANSLATION ERROR] "
            f"{source}->{target}: {e}"
        )
        return None


# ============================================================
# WARIANTY
# ============================================================

def unique_variants(values):
    result = []
    seen = set()

    for value in values:
        value = normalize(value)

        if not valid_variant(value):
            continue

        key = value.casefold()

        if key in seen:
            continue

        seen.add(key)
        result.append(value)

    return result


def add_unidecode_variants(values):
    result = list(values)

    try:
        from unidecode import unidecode
    except ImportError:
        return result

    for value in values:
        converted = normalize(
            unidecode(value)
        )

        if (
            converted
            and converted.casefold()
            != value.casefold()
        ):
            result.append(converted)

    return unique_variants(result)


def build_regex(variants):
    """
    Regex wyszukuje keyword również wtedy, gdy jest częścią
    większego ciągu znaków.

    Przykłady:
        3brat       -> brat
        superbrat   -> brat
        brat123     -> brat
        3брат       -> брат
        брата       -> брат
        братом      -> брат
        братиком    -> брат
    """

    variants = unique_variants(variants)

    if not variants:
        return ""

    patterns = []

    for value in variants:
        value = normalize(value)

        if value:
            patterns.append(re.escape(value))

    patterns.sort(key=len, reverse=True)

    if not patterns:
        return ""

    return "(?:" + "|".join(patterns) + ")"


# ============================================================
# KEYWORD
# ============================================================

def translate_keyword(keyword):
    keyword = normalize(keyword)

    if not keyword:
        return {}

    source = detect_language(
        keyword
    )

    print()
    print("=" * 70)
    print(f"[KEYWORD] {keyword}")
    print(f"[LANGUAGE] {source}")
    print("=" * 70)

    result = {
        "source": source,
        "pl": [],
        "uk": [],
        "ru": [],
        "en": [],
        "variants": [],
        "regex": "",
    }

    # Oryginalne słowo zawsze zostaje
    result[source].append(
        keyword
    )

    for target in LANGUAGES:

        if target == source:
            continue

        print(
            f"[TRANSLATE] "
            f"{source} -> {target}: "
            f"{keyword}"
        )

        translated = get_translation(
            keyword,
            source,
            target
        )

        if translated:
            result[target].append(
                translated
            )

            print(
                f"  {target}: "
                f"{translated}"
            )
        else:
            print(
                f"  {target}: brak tłumaczenia"
            )

    # Wszystkie tłumaczenia
    variants = []

    for lang in LANGUAGES:
        variants.extend(
            result[lang]
        )

    # Transliteracja
    variants = add_unidecode_variants(
        variants
    )

    result["variants"] = unique_variants(
        variants
    )

    result["regex"] = build_regex(
        result["variants"]
    )

    print()
    print(
        "[VARIANTS]"
    )

    for variant in result["variants"]:
        print(
            f"  {variant}"
        )

    print()
    print(
        "[REGEX]"
    )

    print(
        result["regex"]
    )

    return result


# ============================================================
# AKTUALIZACJA WSZYSTKICH KEYWORDÓW
# ============================================================

def _saved_language():
    import json

    config = Path(__file__).resolve().parent / "config" / "settings.json"

    try:
        settings = json.loads(config.read_text(encoding="utf-8"))
        saved = settings.get("interface_language", "pl")
    except (OSError, ValueError, TypeError):
        saved = "pl"

    return saved if saved in ("pl", "en") else "pl"



def update_all(language=None):
    """Aktualizuje wszystkie keywordy przez unified_keyword_engine."""

    from unified_keyword_engine import generate

    keywords = load_keywords()

    if not keywords:
        print("[ERROR] config/keywords.txt jest pusty.")
        return 1

    print()
    print("=" * 70)
    print("[UNIFIED] AKTUALIZACJA KEYWORDÓW")
    print("=" * 70)

    try:
        for keyword in keywords:
            print(f"\n[UNIFIED] {keyword}")
            result = generate(keyword, force=True)

            print(
                f"[OK] Wariantów: {len(result['variants'])}"
            )

        print("\n[OK] Aktualizacja zakończona.")
        return 0

    except Exception as error:
        print(f"[ERROR] Unified engine: {error}")
        return 1


# ============================================================
# SHOW
# ============================================================

def show_keyword(keyword, language=None):
    if language is None:
        language = _saved_language()
    database = load_json(
        TRANSLATIONS_FILE,
        {}
    )

    data = database.get(
        keyword
    )

    if not data:
        print(
            _cli_text(f"Brak keywordu: {keyword}", f"Keyword not found: {keyword}", language)
        )
        print(
            _cli_text("Uruchom najpierw:", "Run this first:", language)
        )
        print(
            "python auto_keywords.py"
        )
        return 1

    print()
    print("=" * 70)
    print(keyword)
    print("=" * 70)

    print(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        )
    )

    return 0


# ============================================================
# MAIN
# ============================================================

def main():
    language = _cli_language()

    if len(sys.argv) >= 2:

        command = sys.argv[1]

        if command == "show":

            if len(sys.argv) < 3:
                print(
                    _cli_text(
                        'Użycie: python auto_keywords.py show "mamusia"',
                        'Usage: python auto_keywords.py show "mamusia"',
                        language,
                    )
                )
                return 1

            return show_keyword(sys.argv[2], language)

    return update_all(language)



# ============================================================
# BILINGUAL CLI
# ============================================================
def _cli_language():
    import json
    from pathlib import Path

    config = Path(__file__).resolve().parent / "config" / "settings.json"

    try:
        settings = json.loads(config.read_text(encoding="utf-8"))
        saved = settings.get("interface_language", "pl")
    except Exception:
        settings = {}
        saved = "pl"

    if saved not in ("pl", "en"):
        saved = "pl"

    print()
    print("=" * 50)
    print("PROGRAM LANGUAGE / JEZYK PROGRAMU")
    print("[1] Polski")
    print("[2] English")
    print("[3] Use saved language / Uzyj zapisanego jezyka (" + saved + ")")

    while True:
        try:
            choice = input("Choose language / Wybierz jezyk [1/2/3]: ").strip()
        except EOFError:
            choice = "3"

        if choice == "1":
            language = "pl"
            break
        elif choice == "2":
            language = "en"
            break
        elif choice == "3":
            language = saved
            break
        else:
            print("Enter 1, 2, or 3 / Wpisz 1, 2 lub 3.")

    settings["interface_language"] = language
    try:
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(
            json.dumps(settings, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except OSError as exc:
        print("Warning: could not save language / Nie zapisano jezyka:", exc)

    return language


def _cli_text(pl, en, language):
    return pl if language == "pl" else en


if __name__ == "__main__":
    sys.exit(
        main()
    )


# ============================================================
