"""
Démonstration rapide du système de normalisation

Ce script montre l'utilisation basique du système sans nécessiter
l'installation complète de Pynini (utilise des mappings directs).

Author: Text Normalization Challenge
Date: 2025
"""

# Mappings simples pour la démonstration (sans FST)
FRENCH_NUMBERS = {
    "0": "zéro", "1": "un", "2": "deux", "3": "trois", "4": "quatre",
    "5": "cinq", "6": "six", "7": "sept", "8": "huit", "9": "neuf",
    "10": "dix", "21": "vingt-et-un", "42": "quarante-deux",
    "75": "soixante-quinze", "80": "quatre-vingts", "99": "quatre-vingt-dix-neuf",
    "100": "cent", "200": "deux-cents", "1000": "mille"
}

ENGLISH_NUMBERS = {
    "0": "zero", "1": "one", "2": "two", "3": "three", "4": "four",
    "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine",
    "10": "ten", "21": "twenty-one", "42": "forty-two",
    "75": "seventy-five", "99": "ninety-nine",
    "100": "one hundred", "200": "two hundred", "1000": "one thousand"
}


def simple_normalize(text, language='fr'):
    """Normalisation simple sans FST (pour démonstration)."""
    mapping = FRENCH_NUMBERS if language == 'fr' else ENGLISH_NUMBERS

    result = text
    for num, word in mapping.items():
        result = result.replace(f" {num} ", f" {word} ")
        # Cas début/fin de phrase
        if result.startswith(f"{num} "):
            result = f"{word} " + result[len(num)+1:]
        if result.endswith(f" {num}"):
            result = result[:-len(num)-1] + f" {word}"

    return result


def main():
    """Démonstration simple."""
    print("=" * 70)
    print("DÉMONSTRATION RAPIDE - NORMALISATION DE TEXTE")
    print("=" * 70)
    print()
    print("Note: Cette démonstration utilise des mappings simples.")
    print("Pour la version complète avec FST, installer Pynini et exécuter:")
    print("  python normalize.py --demo")
    print()
    print("-" * 70)
    print()

    # Exemples français
    print("FRANÇAIS:")
    print("-" * 70)

    fr_examples = [
        "J'ai 3 chiens et 21 chats",
        "Il y a 99 bouteilles",
        "Le nombre 42 est spécial",
        "Elle a 100 euros"
    ]

    for text in fr_examples:
        normalized = simple_normalize(text, 'fr')
        print(f"Original:   {text}")
        print(f"Normalisé:  {normalized}")
        print()

    # Exemples anglais
    print("ANGLAIS:")
    print("-" * 70)

    en_examples = [
        "I have 3 dogs and 21 cats",
        "There are 99 bottles",
        "The number 42 is special",
        "She has 100 dollars"
    ]

    for text in en_examples:
        normalized = simple_normalize(text, 'en')
        print(f"Original:   {text}")
        print(f"Normalisé:  {normalized}")
        print()

    print("=" * 70)
    print("Pour voir tous les exemples et capacités, installez les dépendances:")
    print("  pip install -r requirements.txt")
    print("  python normalize.py --demo")
    print("=" * 70)


if __name__ == "__main__":
    main()
