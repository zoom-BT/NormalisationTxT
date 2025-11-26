"""
Exemples d'utilisation de la bibliothèque de normalisation de texte

Ce fichier démontre différentes façons d'utiliser le système de normalisation.

Author: Text Normalization Challenge
Date: 2025
"""

import sys
from pathlib import Path

# Ajouter le répertoire parent au path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.text_normalizer import TextNormalizer, normalize_text


def example_basic_usage():
    """Exemple 1: Utilisation basique."""
    print("=" * 70)
    print("EXEMPLE 1: Utilisation basique")
    print("=" * 70)
    print()

    # Normalisation simple en français
    result = normalize_text("J'ai 3 chiens et 21 chats", language='fr')
    print(f"Français: J'ai 3 chiens et 21 chats")
    print(f"Résultat: {result}")
    print()

    # Normalisation simple en anglais
    result = normalize_text("I have 3 dogs and 21 cats", language='en')
    print(f"Anglais: I have 3 dogs and 21 cats")
    print(f"Résultat: {result}")
    print()


def example_with_normalizer_class():
    """Exemple 2: Utilisation de la classe TextNormalizer."""
    print("=" * 70)
    print("EXEMPLE 2: Utilisation de la classe TextNormalizer")
    print("=" * 70)
    print()

    # Créer un normaliseur pour le français
    normalizer = TextNormalizer(language='fr')

    texts = [
        "Il y a 99 bouteilles",
        "Mon numéro est le 42",
        "Elle a 100 euros",
        "Il habite au 75 rue de la Paix"
    ]

    print("Normalisation de plusieurs textes:")
    for text in texts:
        result = normalizer.normalize(text)
        print(f"  {text:40} → {result}")
    print()


def example_auto_detection():
    """Exemple 3: Détection automatique de langue."""
    print("=" * 70)
    print("EXEMPLE 3: Détection automatique de langue")
    print("=" * 70)
    print()

    # Créer un normaliseur avec détection automatique
    normalizer = TextNormalizer(language='auto')

    texts = [
        "Le chat a 7 vies",
        "The cat has 7 lives",
        "J'ai 5 doigts",
        "I have 5 fingers"
    ]

    print("Normalisation avec détection automatique:")
    for text in texts:
        detected = normalizer.detect_language(text)
        result = normalizer.normalize(text)
        print(f"  [{detected}] {text:30} → {result}")
    print()


def example_batch_processing():
    """Exemple 4: Traitement par lots."""
    print("=" * 70)
    print("EXEMPLE 4: Traitement par lots")
    print("=" * 70)
    print()

    normalizer = TextNormalizer(language='en')

    # Liste de phrases à normaliser
    sentences = [
        "I have 1 cat",
        "She has 2 dogs",
        "He owns 3 birds",
        "They bought 10 fish",
        "We saw 100 stars"
    ]

    print("Normalisation par lots:")
    results = normalizer.normalize_batch(sentences)
    for original, normalized in zip(sentences, results):
        print(f"  {original:25} → {normalized}")
    print()


def example_special_numbers():
    """Exemple 5: Nombres spéciaux en français."""
    print("=" * 70)
    print("EXEMPLE 5: Nombres spéciaux en français")
    print("=" * 70)
    print()

    normalizer = TextNormalizer(language='fr')

    # Nombres avec des règles spéciales en français
    special_numbers = [
        ("Nombre 70", "70 est un nombre spécial"),
        ("Nombre 71", "71 s'écrit différemment"),
        ("Nombre 80", "80 prend un 's'"),
        ("Nombre 81", "81 ne prend pas de 's'"),
        ("Nombre 90", "90 est comme 80 + 10"),
        ("Nombre 100", "100 s'écrit cent"),
        ("Nombre 200", "200 prend un 's'"),
    ]

    print("Nombres avec règles spéciales:")
    for label, text in special_numbers:
        result = normalizer.normalize(text)
        print(f"  {label:15} {text:35} → {result}")
    print()


def example_edge_cases():
    """Exemple 6: Cas limites."""
    print("=" * 70)
    print("EXEMPLE 6: Cas limites")
    print("=" * 70)
    print()

    normalizer = TextNormalizer(language='fr')

    edge_cases = [
        ("Zéro", "Il a 0 pomme"),
        ("Un", "Elle a 1 chat"),
        ("Mille", "C'est 1000 fois mieux"),
        ("Hors plage", "L'année 2025 est spéciale"),  # Ne sera pas normalisé
        ("Plusieurs nombres", "Il a 3 chats, 5 chiens et 10 oiseaux"),
    ]

    print("Cas limites:")
    for label, text in edge_cases:
        result = normalizer.normalize(text)
        print(f"  {label:20} {text:40} → {result}")
    print()


def example_real_world():
    """Exemple 7: Cas d'utilisation réels."""
    print("=" * 70)
    print("EXEMPLE 7: Cas d'utilisation réels (TTS)")
    print("=" * 70)
    print()

    normalizer_fr = TextNormalizer(language='fr')
    normalizer_en = TextNormalizer(language='en')

    # Phrases réalistes pour la synthèse vocale
    real_world_fr = [
        "Prenez la sortie 15 sur l'autoroute",
        "Il reste 3 minutes avant la fin",
        "Vous avez 42 nouveaux messages",
        "La température est de 20 degrés",
    ]

    real_world_en = [
        "Take exit 15 on the highway",
        "There are 3 minutes left",
        "You have 42 new messages",
        "The temperature is 20 degrees",
    ]

    print("Français (pour TTS):")
    for text in real_world_fr:
        result = normalizer_fr.normalize(text)
        print(f"  {text}")
        print(f"  → {result}")
        print()

    print("Anglais (pour TTS):")
    for text in real_world_en:
        result = normalizer_en.normalize(text)
        print(f"  {text}")
        print(f"  → {result}")
        print()


def example_performance_test():
    """Exemple 8: Test de performance."""
    print("=" * 70)
    print("EXEMPLE 8: Test de performance")
    print("=" * 70)
    print()

    import time

    normalizer = TextNormalizer(language='fr')

    # Générer beaucoup de phrases
    num_sentences = 1000
    sentences = [f"J'ai {i % 100} chats" for i in range(num_sentences)]

    start_time = time.time()
    results = normalizer.normalize_batch(sentences)
    end_time = time.time()

    elapsed = end_time - start_time
    throughput = num_sentences / elapsed

    print(f"Nombre de phrases: {num_sentences}")
    print(f"Temps total: {elapsed:.3f}s")
    print(f"Débit: {throughput:.1f} phrases/seconde")
    print(f"Temps moyen par phrase: {elapsed / num_sentences * 1000:.2f}ms")
    print()


def main():
    """Exécute tous les exemples."""
    examples = [
        example_basic_usage,
        example_with_normalizer_class,
        example_auto_detection,
        example_batch_processing,
        example_special_numbers,
        example_edge_cases,
        example_real_world,
        example_performance_test,
    ]

    for i, example_func in enumerate(examples, 1):
        example_func()
        if i < len(examples):
            input("Appuyez sur Entrée pour continuer...")
            print("\n\n")


if __name__ == "__main__":
    main()
