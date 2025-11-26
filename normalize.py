#!/usr/bin/env python3
"""
Script principal de normalisation de texte

Ce script fournit une interface en ligne de commande pour normaliser
des textes contenant des nombres cardinaux (0-1000) en français ou en anglais.

Usage:
    # Normaliser un texte directement
    python normalize.py "J'ai 3 chiens" --lang fr

    # Normaliser un fichier
    python normalize.py --input input.txt --output output.txt --lang fr

    # Utiliser la détection automatique de langue
    python normalize.py "I have 42 cats" --lang auto

    # Mode interactif
    python normalize.py --interactive --lang fr

Author: Zoom BT for Text Normalization Challenge
Date: Nov 2025
"""

import argparse
import sys
from pathlib import Path

# Ajouter le répertoire src au path
sys.path.insert(0, str(Path(__file__).parent))

from src.text_normalizer import TextNormalizer, SentenceNormalizer


def normalize_text_cli(text: str, language: str = 'auto') -> str:
    """
    Normalise un texte via l'interface CLI.

    Args:
        text: Texte à normaliser
        language: Langue ('fr', 'en', ou 'auto')

    Returns:
        str: Texte normalisé
    """
    normalizer = TextNormalizer(language=language)
    return normalizer.normalize(text)


def normalize_file(input_path: str, output_path: str, language: str = 'auto') -> None:
    """
    Normalise un fichier complet.

    Args:
        input_path: Chemin du fichier d'entrée
        output_path: Chemin du fichier de sortie
        language: Langue ('fr', 'en', ou 'auto')
    """
    print(f"Normalisation du fichier: {input_path}")
    print(f"Langue: {language}")
    print("-" * 70)

    normalizer = SentenceNormalizer(language=language)
    lines_processed, numbers_normalized = normalizer.normalize_file(
        input_path, output_path
    )

    print(f"\n✓ Normalisation terminée!")
    print(f"  Lignes traitées: {lines_processed}")
    print(f"  Nombres normalisés: {numbers_normalized}")
    print(f"  Fichier de sortie: {output_path}")


def interactive_mode(language: str = 'auto') -> None:
    """
    Mode interactif pour la normalisation.

    Args:
        language: Langue ('fr', 'en', ou 'auto')
    """
    print("=" * 70)
    print("MODE INTERACTIF DE NORMALISATION DE TEXTE")
    print("=" * 70)
    print()
    print(f"Langue: {language}")
    print("Tapez 'quit' ou 'exit' pour quitter")
    print("Tapez 'lang <fr|en|auto>' pour changer de langue")
    print("-" * 70)
    print()

    normalizer = TextNormalizer(language=language)
    current_lang = language

    while True:
        try:
            # Lire l'entrée utilisateur
            text = input("Texte> ").strip()

            if not text:
                continue

            # Commandes spéciales
            if text.lower() in ['quit', 'exit', 'q']:
                print("\nAu revoir!")
                break

            if text.lower().startswith('lang '):
                new_lang = text.split()[1].lower()
                if new_lang in ['fr', 'en', 'auto']:
                    current_lang = new_lang
                    normalizer = TextNormalizer(language=current_lang)
                    print(f"✓ Langue changée: {current_lang}")
                else:
                    print(f"✗ Langue invalide: {new_lang}")
                continue

            # Normaliser le texte
            if current_lang == 'auto':
                detected = normalizer.detect_language(text)
                print(f"[Langue détectée: {detected}]")

            result = normalizer.normalize(text)
            print(f"→ {result}")
            print()

        except KeyboardInterrupt:
            print("\n\nAu revoir!")
            break
        except Exception as e:
            print(f"✗ Erreur: {e}")
            print()


def demo_mode() -> None:
    """Mode démonstration avec des exemples prédéfinis."""
    print("=" * 70)
    print("MODE DÉMONSTRATION")
    print("=" * 70)
    print()

    examples = [
        # Français
        ("fr", "J'ai 3 chiens et 21 chats"),
        ("fr", "Il y a 99 bouteilles de bière sur le mur"),
        ("fr", "Le nombre 42 est la réponse à tout"),
        ("fr", "Elle a gagné 1000 euros à la loterie"),
        ("fr", "Mon grand-père a 75 ans"),

        # Anglais
        ("en", "I have 3 dogs and 21 cats"),
        ("en", "There are 99 bottles of beer on the wall"),
        ("en", "The number 42 is the answer"),
        ("en", "She won 1000 dollars in the lottery"),
        ("en", "My grandfather is 75 years old"),
    ]

    fr_normalizer = TextNormalizer(language='fr')
    en_normalizer = TextNormalizer(language='en')

    for lang, text in examples:
        normalizer = fr_normalizer if lang == 'fr' else en_normalizer
        result = normalizer.normalize(text)

        print(f"[{lang.upper()}] Original: {text}")
        print(f"      Normalisé: {result}")
        print()


def main():
    """Point d'entrée principal du script."""
    parser = argparse.ArgumentParser(
        description="Normalisation de texte pour nombres cardinaux (0-1000)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  # Normaliser un texte directement
  python normalize.py "J'ai 3 chiens" --lang fr

  # Normaliser un fichier
  python normalize.py --input input.txt --output output.txt --lang fr

  # Mode interactif
  python normalize.py --interactive --lang fr

  # Mode démonstration
  python normalize.py --demo
        """
    )

    # Arguments
    parser.add_argument(
        'text',
        nargs='?',
        help='Texte à normaliser (si non spécifié, utiliser --input ou --interactive)'
    )
    parser.add_argument(
        '--lang', '--language',
        choices=['fr', 'en', 'auto'],
        default='auto',
        help='Langue du texte (fr=français, en=anglais, auto=détection automatique)'
    )
    parser.add_argument(
        '--input', '-i',
        type=str,
        help='Fichier d\'entrée à normaliser'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Fichier de sortie (requis si --input est spécifié)'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Mode interactif'
    )
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Mode démonstration avec des exemples'
    )

    args = parser.parse_args()

    # Mode démonstration
    if args.demo:
        demo_mode()
        return

    # Mode interactif
    if args.interactive:
        interactive_mode(language=args.lang)
        return

    # Mode fichier
    if args.input:
        if not args.output:
            parser.error("--output est requis quand --input est spécifié")

        if not Path(args.input).exists():
            print(f"✗ Erreur: Le fichier {args.input} n'existe pas")
            sys.exit(1)

        normalize_file(args.input, args.output, language=args.lang)
        return

    # Mode texte direct
    if args.text:
        result = normalize_text_cli(args.text, language=args.lang)
        print(result)
        return

    # Aucun mode spécifié, afficher l'aide
    parser.print_help()


if __name__ == "__main__":
    main()
