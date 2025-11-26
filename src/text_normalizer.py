"""
Module principal de normalisation de texte

Ce module fournit une API simple pour normaliser les nombres cardinaux
dans un texte en français ou en anglais.

Exemples:
    >>> normalizer = TextNormalizer(language='fr')
    >>> normalizer.normalize("J'ai 3 chiens et 21 chats")
    "J'ai trois chiens et vingt-et-un chats"

Author: Text Normalization Challenge
Date: 2025
"""

import re
import sys
import os
from typing import Optional, Tuple

# Ajouter le répertoire parent au path pour les imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from grammars.french_cardinals import FrenchCardinalFST
from grammars.english_cardinals import EnglishCardinalFST


class TextNormalizer:
    """
    Normaliseur de texte pour les nombres cardinaux.

    Cette classe gère la normalisation des nombres cardinaux (0-1000)
    dans un texte complet, en préservant la ponctuation et la structure.

    Attributes:
        language: Code de langue ('fr' pour français, 'en' pour anglais)
        fst_normalizer: Instance du normaliseur FST approprié
    """

    SUPPORTED_LANGUAGES = {'fr', 'en'}

    def __init__(self, language: str = 'auto'):
        """
        Initialise le normaliseur de texte.

        Args:
            language: Code de langue ('fr', 'en', ou 'auto' pour détection automatique)

        Raises:
            ValueError: Si la langue n'est pas supportée
        """
        if language not in self.SUPPORTED_LANGUAGES and language != 'auto':
            raise ValueError(
                f"Langue non supportée: {language}. "
                f"Langues supportées: {', '.join(self.SUPPORTED_LANGUAGES)}"
            )

        self.language = language
        self.fst_normalizer = None

        if language == 'fr':
            self.fst_normalizer = FrenchCardinalFST()
        elif language == 'en':
            self.fst_normalizer = EnglishCardinalFST()
        # Si 'auto', on attendra de détecter la langue lors de la normalisation

    def detect_language(self, text: str) -> str:
        """
        Détecte automatiquement la langue d'un texte.

        Utilise des heuristiques simples basées sur des mots courants
        pour déterminer si le texte est en français ou en anglais.

        Args:
            text: Texte à analyser

        Returns:
            str: Code de langue détecté ('fr' ou 'en')
        """
        text_lower = text.lower()

        # Mots indicateurs français
        french_indicators = [
            'le', 'la', 'les', 'un', 'une', 'des', 'et', 'est',
            'je', 'tu', 'il', 'elle', 'nous', 'vous', 'ils', 'elles',
            'avoir', 'être', 'dans', 'pour', 'avec', 'sur'
        ]

        # Mots indicateurs anglais
        english_indicators = [
            'the', 'a', 'an', 'and', 'is', 'are',
            'i', 'you', 'he', 'she', 'we', 'they',
            'have', 'has', 'in', 'for', 'with', 'on'
        ]

        # Compter les occurrences
        french_score = sum(1 for word in french_indicators if f' {word} ' in f' {text_lower} ')
        english_score = sum(1 for word in english_indicators if f' {word} ' in f' {text_lower} ')

        # Retourner la langue avec le score le plus élevé (français par défaut si égalité)
        return 'fr' if french_score >= english_score else 'en'

    def normalize(self, text: str, language: Optional[str] = None) -> str:
        """
        Normalise les nombres cardinaux dans un texte.

        Cette méthode identifie tous les nombres de 0 à 1000 dans le texte
        et les convertit en leur forme écrite, tout en préservant le reste
        du texte intact.

        Args:
            text: Texte à normaliser
            language: Code de langue (optionnel, remplace la langue de l'instance)

        Returns:
            str: Texte avec les nombres normalisés

        Examples:
            >>> normalizer = TextNormalizer(language='fr')
            >>> normalizer.normalize("J'ai 3 chiens")
            "J'ai trois chiens"

            >>> normalizer = TextNormalizer(language='en')
            >>> normalizer.normalize("I have 42 cats")
            "I have forty-two cats"
        """
        # Déterminer la langue à utiliser
        if language is None:
            if self.language == 'auto':
                language = self.detect_language(text)
            else:
                language = self.language
        else:
            if language not in self.SUPPORTED_LANGUAGES:
                raise ValueError(f"Langue non supportée: {language}")

        # Charger le normaliseur approprié si nécessaire
        if self.fst_normalizer is None or (
            self.language == 'auto' or
            (language == 'fr' and not isinstance(self.fst_normalizer, FrenchCardinalFST)) or
            (language == 'en' and not isinstance(self.fst_normalizer, EnglishCardinalFST))
        ):
            if language == 'fr':
                self.fst_normalizer = FrenchCardinalFST()
            else:
                self.fst_normalizer = EnglishCardinalFST()
            self.language = language

        # Pattern pour identifier les nombres (0-1000)
        # Matches: nombres isolés entourés de limites de mots
        number_pattern = r'\b([0-9]{1,4})\b'

        def replace_number(match: re.Match) -> str:
            """Fonction de remplacement pour chaque nombre trouvé."""
            number_str = match.group(1)

            # Vérifier que le nombre est dans la plage [0, 1000]
            try:
                number_int = int(number_str)
                if 0 <= number_int <= 1000:
                    # Normaliser avec le FST
                    normalized = self.fst_normalizer.normalize(number_str)
                    return normalized
                else:
                    # Nombre hors plage, conserver tel quel
                    return number_str
            except ValueError:
                # Pas un nombre valide, conserver tel quel
                return number_str

        # Remplacer tous les nombres dans le texte
        normalized_text = re.sub(number_pattern, replace_number, text)

        return normalized_text

    def normalize_batch(self, texts: list) -> list:
        """
        Normalise une liste de textes.

        Args:
            texts: Liste de textes à normaliser

        Returns:
            list: Liste des textes normalisés
        """
        return [self.normalize(text) for text in texts]

    def get_language(self) -> str:
        """
        Retourne la langue actuellement utilisée.

        Returns:
            str: Code de langue ('fr', 'en', ou 'auto')
        """
        return self.language


class SentenceNormalizer:
    """
    Normaliseur spécialisé pour les phrases complètes.

    Cette classe étend TextNormalizer avec des fonctionnalités
    supplémentaires pour gérer les phrases complètes, incluant
    la gestion de la ponctuation et des cas spéciaux.
    """

    def __init__(self, language: str = 'auto'):
        """
        Initialise le normaliseur de phrases.

        Args:
            language: Code de langue ('fr', 'en', ou 'auto')
        """
        self.normalizer = TextNormalizer(language=language)

    def normalize(self, sentence: str, preserve_case: bool = True) -> str:
        """
        Normalise une phrase complète.

        Args:
            sentence: Phrase à normaliser
            preserve_case: Si True, préserve la casse originale autant que possible

        Returns:
            str: Phrase normalisée
        """
        # Normaliser les nombres
        normalized = self.normalizer.normalize(sentence)

        # Options supplémentaires pour préserver la casse peuvent être ajoutées ici

        return normalized

    def normalize_file(self, input_path: str, output_path: str) -> Tuple[int, int]:
        """
        Normalise toutes les lignes d'un fichier.

        Args:
            input_path: Chemin du fichier d'entrée
            output_path: Chemin du fichier de sortie

        Returns:
            Tuple[int, int]: (nombre de lignes traitées, nombre de nombres normalisés)
        """
        lines_processed = 0
        numbers_normalized = 0

        with open(input_path, 'r', encoding='utf-8') as f_in, \
             open(output_path, 'w', encoding='utf-8') as f_out:

            for line in f_in:
                # Compter les nombres avant normalisation
                numbers_before = len(re.findall(r'\b[0-9]{1,4}\b', line))

                # Normaliser la ligne
                normalized_line = self.normalize(line.strip())

                # Compter les nombres après normalisation
                numbers_after = len(re.findall(r'\b[0-9]{1,4}\b', normalized_line))

                numbers_normalized += (numbers_before - numbers_after)
                lines_processed += 1

                f_out.write(normalized_line + '\n')

        return lines_processed, numbers_normalized


def normalize_text(text: str, language: str = 'auto') -> str:
    """
    Fonction utilitaire pour normaliser rapidement un texte.

    Args:
        text: Texte à normaliser
        language: Code de langue ('fr', 'en', ou 'auto')

    Returns:
        str: Texte normalisé

    Examples:
        >>> normalize_text("J'ai 3 chiens", language='fr')
        "J'ai trois chiens"
    """
    normalizer = TextNormalizer(language=language)
    return normalizer.normalize(text)


if __name__ == "__main__":
    # Tests de démonstration
    print("=" * 70)
    print("TESTS DE NORMALISATION DE TEXTE")
    print("=" * 70)

    # Test français
    print("\n1. Tests en français:")
    print("-" * 70)
    fr_normalizer = TextNormalizer(language='fr')

    fr_tests = [
        "J'ai 3 chiens et 21 chats",
        "Il y a 99 bouteilles sur le mur",
        "Mon code postal est 75001",
        "Elle a 100 euros dans sa poche",
        "Le nombre 42 est la réponse",
    ]

    for test in fr_tests:
        result = fr_normalizer.normalize(test)
        print(f"Entrée:  {test}")
        print(f"Sortie:  {result}")
        print()

    # Test anglais
    print("\n2. Tests en anglais:")
    print("-" * 70)
    en_normalizer = TextNormalizer(language='en')

    en_tests = [
        "I have 3 dogs and 21 cats",
        "There are 99 bottles on the wall",
        "The answer is 42",
        "She has 100 dollars",
    ]

    for test in en_tests:
        result = en_normalizer.normalize(test)
        print(f"Entrée:  {test}")
        print(f"Sortie:  {result}")
        print()

    # Test détection automatique
    print("\n3. Tests avec détection automatique:")
    print("-" * 70)
    auto_normalizer = TextNormalizer(language='auto')

    auto_tests = [
        ("fr", "Le chat a 7 vies"),
        ("en", "The cat has 7 lives"),
    ]

    for expected_lang, test in auto_tests:
        detected = auto_normalizer.detect_language(test)
        result = auto_normalizer.normalize(test)
        print(f"Texte:    {test}")
        print(f"Langue:   {detected} (attendu: {expected_lang})")
        print(f"Résultat: {result}")
        print()
