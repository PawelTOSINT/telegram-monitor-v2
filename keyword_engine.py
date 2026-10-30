#!/usr/bin/env python3

import json
import re
from pathlib import Path

from unidecode import unidecode
from lingua import Language, LanguageDetectorBuilder

try:
    import pymorphy3

    MORPH_RU = pymorphy3.MorphAnalyzer(
        lang="ru"
    )
except Exception:
    MORPH_RU = None

try:
    MORPH_UK = pymorphy3.MorphAnalyzer(
        lang="uk"
    )
except Exception:
    MORPH_UK = None


BASE_DIR = Path(__file__).resolve().parent

CONFIG_DIR = BASE_DIR / "config"

KEYWORDS_FILE = CONFIG_DIR / "keywords.txt"
TRANSLATIONS_FILE = CONFIG_DIR / "keyword_translations.json"


LANGUAGES = [
    Language.POLISH,
    Language.UKRAINIAN,
    Language.RUSSIAN,
    Language.ENGLISH,
]

DETECTOR = LanguageDetectorBuilder.from_languages(
    *LANGUAGES
).build()


def load_json(path, default):
    if not path.exists():
        return default

    try:
        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path, data):
    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=2
        )


def load_keywords():
    if not KEYWORDS_FILE.exists():
        return []

    result = []

    with open(
        KEYWORDS_FILE,
        "r",
        encoding="utf-8"
    ) as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            if line not in result:
                result.append(line)

    return result


def detect_language(text):
    text = str(text).strip()
    if not text:
        return "unknown"

    try:
        result = DETECTOR.detect_language_of(text)

        mapping = {
            Language.POLISH: "pl",
            Language.UKRAINIAN: "uk",
            Language.RUSSIAN: "ru",
            Language.ENGLISH: "en",
        }
        return mapping.get(result, "unknown")
    except Exception:
        return "unknown"


def morphology_variants(word, analyzer):
    variants = set()

    if analyzer is None:
        return variants

    try:
        parsed = analyzer.parse(word)

        if not parsed:
            return variants

        parse = parsed[0]

        normal = parse.normal_form

        if normal:
            variants.add(normal)

        for form in parse.lexeme:
            text = getattr(form, "word", None)

            if text:
                variants.add(text)

    except Exception:
        pass

    return variants


def transliteration_variants(word):
    result = set()

    converted = unidecode(word)

    if converted:
        result.add(converted)

    return result


def generate_dictionary_variants(word, language):
    variants = set()

    variants.add(word)

    if language == "ru":
        variants.update(
            morphology_variants(
                word,
                MORPH_RU
            )
        )

    elif language == "uk":
        variants.update(
            morphology_variants(
                word,
                MORPH_UK
            )
        )

    variants.update(
        transliteration_variants(word)
    )

    return {
        x.strip()
        for x in variants
        if x and x.strip()
    }


def build_regex(variants):
    variants = sorted(
        set(variants),
        key=lambda x: (
            -len(x),
            x.lower()
        )
    )

    escaped = [
        re.escape(x)
        for x in variants
    ]

    if not escaped:
        return ""

    return (
        r"(?<!\w)(?:"
        + "|".join(escaped)
        + r")(?!\w)"
    )


def translate_local(text):
    """
    Lokalny punkt wejścia dla tłumaczenia.

    W tej wersji używamy lokalnych słowników
    i odmiany morfologicznej.

    Dla słów, których nie da się rozpoznać
    automatycznie, zachowujemy oryginał.
    """

    translations = {
        "brat": {
            "pl": ["brat"],
            "uk": ["брат"],
            "ru": ["брат"],
            "en": ["brother"],
        },

        "example": {
            "pl": ["example"],
            "uk": [
                "дрон",
                "безпілотник",
                "БПЛА",
            ],
            "ru": [
                "дрон",
                "беспилотник",
                "БПЛА",
            ],
            "en": [
                "examplee",
                "UAV",
            ],
        },

        "rakieta": {
            "pl": ["rakieta"],
            "uk": [
                "ракета",
            ],
            "ru": [
                "ракета",
            ],
            "en": [
                "sample",
                "rocket",
            ],
        },

        "artylery": {
            "pl": [
                "artyleria",
            ],
            "uk": [
                "артилерія",
            ],
            "ru": [
                "артиллерия",
            ],
            "en": [
                "example",
            ],
        },
    }

    key = text.lower().strip()

    if key in translations:
        return translations[key]

    return {
        "pl": [text],
        "uk": [text],
        "ru": [text],
        "en": [text],
    }


def generate_keyword(keyword):
    detected = detect_language(keyword)

    translation_data = translate_local(
        keyword
    )

    all_variants = set()

    languages = {}

    for language in (
        "pl",
        "uk",
        "ru",
        "en"
    ):
        words = set()

        for word in translation_data.get(
            language,
            []
        ):
            words.update(
                generate_dictionary_variants(
                    word,
                    language
                )
            )

        languages[language] = sorted(
            words
        )

        all_variants.update(words)

    regex = build_regex(
        all_variants
    )

    return {
        "keyword": keyword,
        "detected_language": detected,
        "languages": languages,
        "variants": sorted(
            all_variants,
            key=lambda x: (
                -len(x),
                x.lower()
            )
        ),
        "regex": regex,
    }


def update_all():
    data = load_json(
        TRANSLATIONS_FILE,
        {}
    )

    keywords = load_keywords()

    changed = False

    for keyword in keywords:

        if keyword not in data:

            print(_cli_text(
                f"[AUTO] Nowy keyword: {keyword}",
                f"[AUTO] New keyword: {keyword}",
                _saved_language(),
            ))

            data[keyword] = generate_keyword(
                keyword
            )

            changed = True

    save_json(
        TRANSLATIONS_FILE,
        data
    )

    return data, changed


def get_keyword(keyword):
    data, changed = update_all()

    if keyword not in data:
        data[keyword] = generate_keyword(
            keyword
        )

        save_json(
            TRANSLATIONS_FILE,
            data
        )

    return data[keyword]


def main():
    language = _cli_language()

    data, changed = update_all()

    print()
    print("=" * 70)
    print(_cli_text("AUTOMATYCZNY KEYWORD ENGINE", "AUTOMATIC KEYWORD ENGINE", language))
    print("=" * 70)

    for keyword, item in data.items():

        print()
        print(
            _cli_text("SŁOWO KLUCZOWE:", "KEYWORD:", language),
            keyword
        )

        print(
            _cli_text("JĘZYK:", "LANGUAGE:", language),
            item.get(
                "detected_language"
            )
        )

        print(
            _cli_text("POLSKI (PL):", "POLISH (PL):", language),
            ", ".join(
                item.get(
                    "pl",
                    []
                )
            )
        )

        print(
            _cli_text("UKRAIŃSKI (UK):", "UKRAINIAN (UK):", language),
            ", ".join(
                item.get(
                    "uk",
                    []
                )
            )
        )

        print(
            _cli_text("ROSYJSKI (RU):", "RUSSIAN (RU):", language),
            ", ".join(
                item.get(
                    "ru",
                    []
                )
            )
        )

        print(
            _cli_text("ANGIELSKI (EN):", "ENGLISH (EN):", language),
            ", ".join(
                item.get(
                    "en",
                    []
                )
            )
        )

        print()
        print(
            _cli_text("WARIANTÓW:", "VARIANTS:", language),
            len(item["variants"])
        )

        print(
            _cli_text("WYRAŻENIE REGULARNE (REGEX):", "REGULAR EXPRESSION (REGEX):", language)
        )

        print(
            item["regex"]
        )

    print()
    print(
        _cli_text("[OK] Zapisano:", "[OK] Saved:", language),
        TRANSLATIONS_FILE
    )



# ============================================================
# BILINGUAL CLI
# ============================================================
def _saved_language():
    import json
    from pathlib import Path
    config = Path(__file__).resolve().parent / "config" / "settings.json"
    try:
        settings = json.loads(config.read_text(encoding="utf-8"))
        value = settings.get("interface_language", "pl")
    except (OSError, ValueError, TypeError):
        value = "pl"
    return value if value in ("pl", "en") else "pl"


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
    main()


# ============================================================
