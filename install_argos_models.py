#!/usr/bin/env python3

import sys

import argostranslate.package
import argostranslate.translate


# Modele wymagane do tłumaczenia PL, UK, RU i EN.
# Tłumaczenia PL <-> UK/RU realizowane są przez EN.
CORE_PAIRS = [
    ("pl", "en"),
    ("en", "pl"),
    ("en", "uk"),
    ("uk", "en"),
    ("en", "ru"),
    ("ru", "en"),
]

# Modele bezpośrednie instalujemy, jeśli są dostępne.
OPTIONAL_PAIRS = [
    ("pl", "uk"),
    ("uk", "pl"),
    ("pl", "ru"),
    ("ru", "pl"),
    ("uk", "ru"),
    ("ru", "uk"),
]


def installed_pairs():
    result = set()

    languages = argostranslate.translate.get_installed_languages()

    for source in languages:
        for target in languages:
            if source.code == target.code:
                continue

            try:
                if source.get_translation(target):
                    result.add((source.code, target.code))
            except Exception:
                pass

    return result


def install_pair(source, target, available, installed, required=True):
    pair = (source, target)

    if pair in installed:
        print(f"[OK] {source} -> {target} (już zainstalowany)")
        return True

    matches = [
        package for package in available
        if package.from_code == source
        and package.to_code == target
    ]

    if not matches:
        label = "ERROR" if required else "WARN"
        print(f"[{label}] Brak modelu {source} -> {target}")
        return not required

    package = matches[0]

    print(f"[DOWNLOAD] {source} -> {target}")

    try:
        path = package.download()

        argostranslate.package.install_from_path(path)

        installed.clear()
        installed.update(installed_pairs())

        if pair not in installed:
            print(f"[ERROR] Instalacja nie potwierdziła {source} -> {target}")
            return not required

        print(f"[OK] Zainstalowano {source} -> {target}")
        return True

    except Exception as error:
        print(f"[ERROR] {source} -> {target}: {error}")
        return not required


def main():
    print("=" * 70)
    print("TELEGRAM MONITOR - AUTOMATYCZNA INSTALACJA ARGOS")
    print("=" * 70)

    try:
        print("\n[1/4] Aktualizacja indeksu modeli...")

        argostranslate.package.update_package_index()

        print("[OK] Indeks zaktualizowany")

        print("\n[2/4] Pobieranie listy dostępnych modeli...")

        available = argostranslate.package.get_available_packages()
        installed = installed_pairs()

        print(f"[INFO] Dostępne pakiety: {len(available)}")

    except Exception as error:
        print(f"\n[ERROR] Nie można pobrać indeksu Argos: {error}")
        return 1

    print("\n[3/4] Instalowanie wymaganych modeli...")

    success = True

    for source, target in CORE_PAIRS:
        result = install_pair(
            source,
            target,
            available,
            installed,
            required=True,
        )

        if not result:
            success = False

    print("\n[4/4] Sprawdzanie dodatkowych modeli bezpośrednich...")

    for source, target in OPTIONAL_PAIRS:
        install_pair(
            source,
            target,
            available,
            installed,
            required=False,
        )

    print("\n" + "=" * 70)
    print("PODSUMOWANIE ARGOS")
    print("=" * 70)

    installed = installed_pairs()

    for source, target in CORE_PAIRS:
        if (source, target) in installed:
            print(f"[OK] {source} -> {target}")
        else:
            print(f"[BRAK] {source} -> {target}")
            success = False

    if success:
        print("\n[SUCCESS] Wszystkie wymagane modele są zainstalowane.")
        return 0

    print("\n[ERROR] Nie udało się zainstalować wszystkich wymaganych modeli.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
