#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unified Keyword Engine
PL / UK / RU / EN

Morfologia:
PL - Morfeusz2
UK - Pymorphy3
RU - Pymorphy3
EN - reguly fleksyjne

Translation:
Argos Translate + lokalne poprawki.
"""

import re
import json
import hashlib
from pathlib import Path

BASE = Path(__file__).resolve().parent

TRANSLATIONS = BASE / "config" / "keyword_translations.json"
CACHE = BASE / "cache" / "auto_keywords.json"

LANGUAGES = ("pl", "uk", "ru", "en")
ENGINE_VERSION = 4


# =========================================================
# NORMALIZACJA
# =========================================================

def normalize(value):
    return re.sub(r"\s+", " ", str(value or "")).strip()


def unique(values):
    result = {}
    for value in values:
        value = normalize(value)

        if not value:
            continue

        if len(value) > 120:
            continue

        result.setdefault(value.casefold(), value)

    return set(result.values())


def sort_variants(values):
    return sorted(
        unique(values),
        key=lambda x: (-len(x), x.casefold())
    )


# =========================================================
# JSON
# =========================================================

def load_json(path):
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError, TypeError):
        return {}


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)

    temporary = path.with_suffix(path.suffix + ".tmp")

    temporary.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )

    temporary.replace(path)


def cache_signature(keyword):
    raw = f"{ENGINE_VERSION}:{normalize(keyword).casefold()}"

    return hashlib.sha256(
        raw.encode("utf-8")
    ).hexdigest()


# =========================================================
# ROZPOZNAWANIE JĘZYKA
# =========================================================

def detect_language(word):
    word = normalize(word).lower()

    if re.search(r"[іїєґ]", word):
        return "uk"

    if re.search(r"[ёыэъ]", word):
        return "ru"

    if re.search(r"[а-я]", word):
        return "ru"

    if re.search(r"[ąćęłńóśźż]", word):
        return "pl"

    known_pl = {
        "brat", "siostra", "sister",
        "rakieta", "rakiety",
        "artyleria", "artylery",
        "dron", "dom", "matka",
        "ojciec", "mama", "tata",
    }

    if word in known_pl:
        return "pl"

    try:
        import auto_keywords
        return auto_keywords.detect_language(word)
    except Exception:
        return "en"


# =========================================================
# POPRAWKI TŁUMACZEŃ
# =========================================================

MANUAL = {
    "brat": {
        "pl": ["brat"],
        "uk": ["брат"],
        "ru": ["брат"],
        "en": ["brother"],
    },

    "дрон": {
        "pl": ["dron"],
        "uk": ["дрон"],
        "ru": ["дрон"],
        "en": ["drone"],
    },

    "rakieta": {
        "pl": ["rakieta"],
        "uk": ["ракета"],
        "ru": ["ракета"],
        "en": ["rocket"],
    },

    "sister": {
        "pl": ["siostra"],
        "uk": ["сестра"],
        "ru": ["сестра"],
        "en": ["sister"],
    },

    "artyleria": {
        "pl": ["artyleria"],
        "uk": ["артилерія"],
        "ru": ["артиллерия"],
        "en": ["artillery"],
    },

    "артилерія": {
        "pl": ["artyleria"],
        "uk": ["артилерія"],
        "ru": ["артиллерия"],
        "en": ["artillery"],
    },
}


def translate_keyword(keyword):
    key = keyword.casefold()

    if key in MANUAL:
        return {
            lang: list(MANUAL[key].get(lang, []))
            for lang in LANGUAGES
        }, "manual"

    import auto_keywords

    result = auto_keywords.translate_keyword(keyword)

    languages = {}

    for lang in LANGUAGES:
        values = result.get(lang, [])

        if not isinstance(values, list):
            values = []

        languages[lang] = values

    return languages, result.get("source", "argos")


# =========================================================
# POLSKA MORFOLOGIA - MORFEUSZ2
# =========================================================

def generate_polish_variants(word):
    variants = {word}

    try:
        import morfeusz2

        morph = morfeusz2.Morfeusz()

        # Obsługa również słów wpisanych w odmianie.
        analyses = morph.analyse(word)

        lemmas = set()

        for item in analyses:
            analysis = item[2]

            form = analysis[0]
            lemma = analysis[1]
            tag = analysis[2]

            if tag.startswith("subst"):
                lemmas.add(lemma)

            if form:
                variants.add(form)

        lemmas.add(word)

        for lemma in lemmas:
            try:
                generated = morph.generate(lemma)

                for item in generated:
                    form, generated_lemma, tag = item[:3]

                    if generated_lemma != lemma:
                        continue

                    # Rzeczowniki, bez skrótów i innych kategorii.
                    if not tag.startswith("subst"):
                        continue

                    variants.add(form)

            except Exception:
                pass

    except ImportError:
        print("[MORPH] Brak Morfeusz2")

    except Exception as error:
        print("[MORPH PL ERROR]", error)

    return unique(variants)


# =========================================================
# ROSYJSKA I UKRAIŃSKA MORFOLOGIA
# =========================================================

_MORPH_ANALYZERS = {}


def get_pymorphy(lang):
    if lang in _MORPH_ANALYZERS:
        return _MORPH_ANALYZERS[lang]

    import pymorphy3

    analyzer = pymorphy3.MorphAnalyzer(lang=lang)

    _MORPH_ANALYZERS[lang] = analyzer

    return analyzer


def generate_pymorphy_variants(word, lang):
    variants = {word}

    try:
        analyzer = get_pymorphy(lang)

        parses = analyzer.parse(word)

        for parse in parses[:5]:
            try:
                # Wszystkie formy rozpoznanego leksemu.
                for form in parse.lexeme:
                    value = getattr(form, "word", None)

                    if value:
                        variants.add(value)

            except Exception:
                pass

    except ImportError:
        print(f"[MORPH] Brak pymorphy3 dla {lang}")

    except Exception as error:
        print(f"[MORPH {lang.upper()} ERROR] {word}: {error}")

    return unique(variants)


# =========================================================
# ANGIELSKA MORFOLOGIA
# =========================================================

ENGLISH_IRREGULAR = {
    "child": ["child", "children", "child's", "children's"],
    "person": ["person", "people", "person's", "people's"],
    "man": ["man", "men", "man's", "men's"],
    "woman": ["woman", "women", "woman's", "women's"],
    "foot": ["foot", "feet", "foot's", "feet's"],
    "tooth": ["tooth", "teeth", "tooth's", "teeth's"],
    "mouse": ["mouse", "mice", "mouse's", "mice's"],
    "goose": ["goose", "geese", "goose's", "geese's"],
}



def generate_english_variants(word):
    word = normalize(word)
    lower = word.casefold()

    irregular = {
        "child": ["children"],
        "person": ["people"],
        "man": ["men"],
        "woman": ["women"],
        "foot": ["feet"],
        "tooth": ["teeth"],
        "mouse": ["mice"],
        "goose": ["geese"],
    }

    plural = irregular.get(lower)

    if plural:
        plural_forms = plural
    elif lower.endswith("y") and len(lower) > 1:
        if lower[-2] not in "aeiou":
            plural_forms = [word[:-1] + "ies"]
        else:
            plural_forms = [word + "s"]
    elif lower.endswith(("s", "x", "z", "ch", "sh")):
        plural_forms = [word + "es"]
    else:
        plural_forms = [word + "s"]

    result = {word}

    for form in plural_forms:
        result.add(form)
        result.add(word + "'s")
        result.add(form + "'")

    result.add(word + "'s")

    return unique(result)


# =========================================================
# TRANSLITERACJA
# =========================================================


def transliterate(values):
    result = set(values)

    try:
        from unidecode import unidecode
    except ImportError:
        return unique(result)

    for word in values:
        # Transliterujemy tylko tekst zawierający cyrylicę.
        if not re.search(r"[а-яёіїєґ]", word, re.IGNORECASE):
            continue

        converted = normalize(unidecode(word))

        # Usuwamy apostrofy techniczne z transliteracji.
        converted = re.sub(r"['’`]", "", converted)

        if converted and converted.casefold() != word.casefold():
            result.add(converted)

    return unique(result)


# =========================================================
# PEŁNA MORFOLOGIA
# =========================================================

def expand_language(values, lang):
    result = set()

    for word in values:
        result.add(word)

        if lang == "pl":
            result.update(generate_polish_variants(word))

        elif lang == "uk":
            result.update(generate_pymorphy_variants(word, "uk"))

        elif lang == "ru":
            result.update(generate_pymorphy_variants(word, "ru"))

        elif lang == "en":
            result.update(generate_english_variants(word))

    return unique(result)


# =========================================================
# REGEX
# =========================================================

def build_pattern(variants):
    variants = sort_variants(variants)

    if not variants:
        return ""

    escaped = [
        re.escape(word)
        for word in variants
    ]

    # Celowo bez granic slow:
    # pozwala wykrywac odmiany i formy wewnatrz tekstu.
    return "(?:" + "|".join(escaped) + ")"


# =========================================================
# GŁÓWNY GENERATOR
# =========================================================

def make_result(keyword, variants, data=None):
    variants = sorted(
        set(
            normalize(x)
            for x in variants
            if normalize(x)
        ),
        key=lambda x: (-len(x), x.casefold())
    )

    if not variants:
        raise RuntimeError(f"Brak wariantów dla {keyword}")

    pattern = (
        r"(?<!\w)(?:"
        + "|".join(re.escape(x) for x in variants)
        + r")(?!\w)"
    )

    return {
        "keyword": keyword,
        "variants": variants,
        "pattern": pattern,
        "regex": re.compile(
            pattern,
            re.IGNORECASE | re.UNICODE
        ),
        "languages": (data or {}).get("languages", {}),
    }

def generate(keyword, force=False):
    keyword = normalize(keyword)

    if not keyword:
        raise ValueError("Pusty keyword")

    database = load_json(TRANSLATIONS)
    cache = load_json(CACHE)

    signature = cache_signature(keyword)

    cached = cache.get(keyword.casefold())

    # Cache tylko aktualnej wersji.
    if not force and isinstance(cached, dict):
        if (
            cached.get("engine") == ENGINE_VERSION
            and cached.get("signature") == signature
            and isinstance(cached.get("variants"), list)
            and cached["variants"]
        ):
            return make_result(
                keyword,
                cached["variants"],
                database.get(keyword, cached)
            )

    print(f"\n[UNIFIED] Generowanie: {keyword}")

    languages, source = translate_keyword(keyword)

    expanded_languages = {}

    for lang in LANGUAGES:
        values = languages.get(lang, [])

        values = unique(values)

        # Oryginalne słowo nie może zniknąć.
        if lang == detect_language(keyword):
            values.add(keyword)

        print(f"[MORPH] {lang.upper()}")

        expanded_languages[lang] = sort_variants(
            expand_language(values, lang)
        )

    # Wszystkie języki.
    all_variants = set()

    for lang in LANGUAGES:
        all_variants.update(expanded_languages[lang])

    all_variants.add(keyword)

    # Transliteration wszystkich form.
    all_variants = transliterate(all_variants)

    variants = sort_variants(all_variants)

    if not variants:
        raise RuntimeError("Generator zwrócił pustą listę")

    pattern = build_pattern(variants)

    data = {
        "keyword": keyword,
        "source": source,
        "languages": expanded_languages,
        "variants": variants,
        "regex": pattern,
        "engine": ENGINE_VERSION,
        "signature": signature,
    }

    database[keyword] = data

    cache[keyword.casefold()] = {
        "keyword": keyword,
        "engine": ENGINE_VERSION,
        "signature": signature,
        "languages": list(LANGUAGES),
        "variants": variants,
    }

    save_json(TRANSLATIONS, database)
    save_json(CACHE, cache)

    print(f"[OK] Wariantów: {len(variants)}")

    return make_result(keyword, variants, data)


# =========================================================
# REBUILD
# =========================================================

def rebuild_all():
    import auto_keywords

    keywords = auto_keywords.load_keywords()

    if not keywords:
        raise RuntimeError("Brak słów w config/keywords.txt")

    results = {}

    for keyword in keywords:
        result = generate(keyword, force=True)
        results[keyword] = result

    return results


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        result = generate(" ".join(sys.argv[1:]), force=True)

        print("\n===== WARIANTY =====")

        for word in result["variants"]:
            print(word)

        print("\n===== REGEX =====")
        print(result["pattern"])

    else:
        rebuild_all()
