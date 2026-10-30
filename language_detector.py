import re
from functools import lru_cache

import pymorphy3


MORPH_RU = pymorphy3.MorphAnalyzer(lang="ru")
MORPH_UK = pymorphy3.MorphAnalyzer(lang="uk")


UA_CHARS = set("іїєґІЇЄҐ")
RU_CHARS = set("ыэъёЫЭЪЁ")


UA_WORDS = {
    "і", "ї", "є", "ґ",
    "це", "цей", "ця", "ці",
    "який", "яка", "яке", "які",
    "що", "також", "тільки",
    "можна", "потрібно", "треба",
    "буде", "був", "була", "були",
    "вони", "їх", "їхній",
    "мені", "тобі", "йому", "нею",
    "дуже", "тому", "через",
    "будь", "будь-який",
}


RU_WORDS = {
    "ы", "э", "ъ", "ё",
    "это", "этот", "эта", "эти",
    "который", "которая", "которое", "которые",
    "что", "также", "только",
    "можно", "нужно", "надо",
    "будет", "был", "была", "были",
    "они", "их", "ими",
    "мне", "тебе", "ему", "ей",
    "очень", "поэтому", "через",
}


def normalize_text(text):
    return text.lower().strip()


def get_words(text):
    return re.findall(
        r"[а-яіїєґёыэъ]+",
        text.lower(),
        flags=re.IGNORECASE,
    )


@lru_cache(maxsize=10000)
def morphology_score(word, language):
    try:
        morph = MORPH_UK if language == "uk" else MORPH_RU
        analyses = morph.parse(word)

        if analyses and analyses[0].normal_form:
            return 1.0

    except Exception:
        pass

    return 0.0


def detect_language(text):
    if not text or not text.strip():
        return {
            "language": "other",
            "confidence": 0.0,
            "ru_score": 0.0,
            "uk_score": 0.0,
        }

    text = normalize_text(text)
    words = get_words(text)

    if not words:
        return {
            "language": "other",
            "confidence": 0.0,
            "ru_score": 0.0,
            "uk_score": 0.0,
        }

    ru_score = 0.0
    uk_score = 0.0

    # Charakterystyczne znaki
    for char in text:
        if char in UA_CHARS:
            uk_score += 5.0

        if char in RU_CHARS:
            ru_score += 5.0

    # Charakterystyczne słowa
    for word in words:
        if word in UA_WORDS:
            uk_score += 4.0

        if word in RU_WORDS:
            ru_score += 4.0

    # Analiza morfologiczna
    sample = words[:100]

    ru_morph = 0.0
    uk_morph = 0.0

    for word in sample:
        ru_morph += morphology_score(word, "ru")
        uk_morph += morphology_score(word, "uk")

    if sample:
        ru_morph /= len(sample)
        uk_morph /= len(sample)

    ru_score += ru_morph * 2.0
    uk_score += uk_morph * 2.0

    # Decyzja
    total = ru_score + uk_score

    if total == 0:
        language = "other"
        confidence = 0.0

    else:
        difference = abs(ru_score - uk_score)

        if difference < 1.5:
            language = "other"
            confidence = 0.5

        elif uk_score > ru_score:
            language = "uk"
            confidence = min(
                0.99,
                uk_score / max(ru_score + uk_score, 1.0)
            )

        else:
            language = "ru"
            confidence = min(
                0.99,
                ru_score / max(ru_score + uk_score, 1.0)
            )

    return {
        "language": language,
        "confidence": round(confidence, 3),
        "ru_score": round(ru_score, 3),
        "uk_score": round(uk_score, 3),
        "words": len(words),
    }



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
    print("WYBÓR JĘZYKA PROGRAMU" if saved == "pl" else "PROGRAM LANGUAGE")
    print("[1] Polski")
    print("[2] English")
    print(("[3] Użyj zapisanego języka (" if saved == "pl" else "[3] Use saved language (") + saved + ")")

    while True:
        try:
            prompt = "Wybierz język [1/2/3]: " if saved == "pl" else "Choose language [1/2/3]: "
            choice = input(prompt).strip()
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
            print("Wpisz 1, 2 lub 3." if saved == "pl" else "Enter 1, 2, or 3.")

    settings["interface_language"] = language
    try:
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(
            json.dumps(settings, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    except OSError as exc:
        print(("Ostrzeżenie: nie udało się zapisać języka:" if language == "pl" else "Warning: could not save language:"), exc)

    return language


def _cli_text(pl, en, language):
    return pl if language == "pl" else en


if __name__ == "__main__":
    language = _cli_language()
    if language == "pl":
        print("=" * 60)
        print("DETEKTOR JĘZYKA RU / UA")
        print("Wpisz tekst i naciśnij Enter.")
        print("Ctrl+C kończy program.")
    else:
        print("=" * 60)
        print("RU / UA LANGUAGE DETECTOR")
        print("Enter text and press Enter.")
        print("Press Ctrl+C to exit.")
    print()

    while True:
        try:
            text = input("> ")
            result = detect_language(text)
            if language == "pl":
                print(f"Język:     {result['language']}")
                print(f"Pewność:   {result['confidence']}")
                print(f"Wynik RU:  {result['ru_score']}")
                print(f"Wynik UA:  {result['uk_score']}")
            else:
                print(f"Language:  {result['language']}")
                print(f"Confidence:{result['confidence']}")
                print(f"RU score:  {result['ru_score']}")
                print(f"UA score:  {result['uk_score']}")
            print()
        except KeyboardInterrupt:
            print("\n" + ("Koniec." if language == "pl" else "Finished."))
            break
