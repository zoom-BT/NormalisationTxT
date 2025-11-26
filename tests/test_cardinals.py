"""
Tests unitaires pour la normalisation des nombres cardinaux

Ce fichier contient des tests complets pour valider la normalisation
des nombres cardinaux de 0 à 1000 en français et en anglais.

Usage:
    pytest tests/test_cardinals.py -v

Author: Text Normalization Challenge
Date: 2025
"""

import sys
import os
import pytest

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from grammars.french_cardinals import FrenchCardinalFST
from grammars.english_cardinals import EnglishCardinalFST
from src.text_normalizer import TextNormalizer, normalize_text


class TestFrenchCardinals:
    """Tests pour les nombres cardinaux français."""

    @pytest.fixture
    def fst(self):
        """Fixture pour créer un FST français."""
        return FrenchCardinalFST()

    def test_units_0_to_9(self, fst):
        """Test des unités de 0 à 9."""
        expected = {
            "0": "zéro",
            "1": "un",
            "2": "deux",
            "3": "trois",
            "4": "quatre",
            "5": "cinq",
            "6": "six",
            "7": "sept",
            "8": "huit",
            "9": "neuf"
        }
        for num, word in expected.items():
            assert fst.normalize(num) == word, f"Échec pour {num}"

    def test_teens_10_to_19(self, fst):
        """Test des nombres de 10 à 19."""
        expected = {
            "10": "dix",
            "11": "onze",
            "12": "douze",
            "13": "treize",
            "14": "quatorze",
            "15": "quinze",
            "16": "seize",
            "17": "dix-sept",
            "18": "dix-huit",
            "19": "dix-neuf"
        }
        for num, word in expected.items():
            assert fst.normalize(num) == word, f"Échec pour {num}"

    def test_tens_20_to_60(self, fst):
        """Test des dizaines de 20 à 60."""
        expected = {
            "20": "vingt",
            "21": "vingt-et-un",
            "22": "vingt-deux",
            "30": "trente",
            "31": "trente-et-un",
            "35": "trente-cinq",
            "40": "quarante",
            "41": "quarante-et-un",
            "42": "quarante-deux",
            "50": "cinquante",
            "51": "cinquante-et-un",
            "59": "cinquante-neuf",
            "60": "soixante",
            "61": "soixante-et-un",
            "69": "soixante-neuf"
        }
        for num, word in expected.items():
            assert fst.normalize(num) == word, f"Échec pour {num}"

    def test_seventies_70_to_79(self, fst):
        """Test des nombres de 70 à 79."""
        expected = {
            "70": "soixante-dix",
            "71": "soixante et onze",
            "72": "soixante-douze",
            "75": "soixante-quinze",
            "79": "soixante-dix-neuf"
        }
        for num, word in expected.items():
            assert fst.normalize(num) == word, f"Échec pour {num}"

    def test_eighties_80_to_99(self, fst):
        """Test des nombres de 80 à 99."""
        expected = {
            "80": "quatre-vingts",
            "81": "quatre-vingt-un",
            "85": "quatre-vingt-cinq",
            "90": "quatre-vingt-dix",
            "91": "quatre-vingt-onze",
            "95": "quatre-vingt-quinze",
            "99": "quatre-vingt-dix-neuf"
        }
        for num, word in expected.items():
            assert fst.normalize(num) == word, f"Échec pour {num}"

    def test_hundreds(self, fst):
        """Test des centaines."""
        expected = {
            "100": "cent",
            "101": "cent-un",
            "150": "cent-cinquante",
            "200": "deux-cents",
            "201": "deux-cent-un",
            "300": "trois-cents",
            "500": "cinq-cents",
            "999": "neuf-cent-quatre-vingt-dix-neuf"
        }
        for num, word in expected.items():
            assert fst.normalize(num) == word, f"Échec pour {num}"

    def test_thousand(self, fst):
        """Test de 1000."""
        assert fst.normalize("1000") == "mille"


class TestEnglishCardinals:
    """Tests pour les nombres cardinaux anglais."""

    @pytest.fixture
    def fst(self):
        """Fixture pour créer un FST anglais."""
        return EnglishCardinalFST()

    def test_units_0_to_9(self, fst):
        """Test des unités de 0 à 9."""
        expected = {
            "0": "zero",
            "1": "one",
            "2": "two",
            "3": "three",
            "4": "four",
            "5": "five",
            "6": "six",
            "7": "seven",
            "8": "eight",
            "9": "nine"
        }
        for num, word in expected.items():
            assert fst.normalize(num) == word, f"Échec pour {num}"

    def test_teens_10_to_19(self, fst):
        """Test des nombres de 10 à 19."""
        expected = {
            "10": "ten",
            "11": "eleven",
            "12": "twelve",
            "13": "thirteen",
            "14": "fourteen",
            "15": "fifteen",
            "16": "sixteen",
            "17": "seventeen",
            "18": "eighteen",
            "19": "nineteen"
        }
        for num, word in expected.items():
            assert fst.normalize(num) == word, f"Échec pour {num}"

    def test_tens_20_to_90(self, fst):
        """Test des dizaines de 20 à 90."""
        expected = {
            "20": "twenty",
            "21": "twenty-one",
            "30": "thirty",
            "35": "thirty-five",
            "40": "forty",
            "42": "forty-two",
            "50": "fifty",
            "59": "fifty-nine",
            "60": "sixty",
            "70": "seventy",
            "80": "eighty",
            "90": "ninety",
            "99": "ninety-nine"
        }
        for num, word in expected.items():
            assert fst.normalize(num) == word, f"Échec pour {num}"

    def test_hundreds(self, fst):
        """Test des centaines."""
        expected = {
            "100": "one hundred",
            "101": "one hundred one",
            "150": "one hundred fifty",
            "200": "two hundred",
            "201": "two hundred one",
            "300": "three hundred",
            "500": "five hundred",
            "999": "nine hundred ninety-nine"
        }
        for num, word in expected.items():
            assert fst.normalize(num) == word, f"Échec pour {num}"

    def test_thousand(self, fst):
        """Test de 1000."""
        assert fst.normalize("1000") == "one thousand"


class TestTextNormalizer:
    """Tests pour le normaliseur de texte complet."""

    def test_french_sentences(self):
        """Test de phrases complètes en français."""
        normalizer = TextNormalizer(language='fr')

        test_cases = [
            ("J'ai 3 chiens et 21 chats", "J'ai trois chiens et vingt-et-un chats"),
            ("Il y a 99 bouteilles", "Il y a quatre-vingt-dix-neuf bouteilles"),
            ("Le nombre 42 est spécial", "Le nombre quarante-deux est spécial"),
            ("Elle a 100 euros", "Elle a cent euros"),
        ]

        for input_text, expected in test_cases:
            result = normalizer.normalize(input_text)
            assert result == expected, f"Échec pour: {input_text}"

    def test_english_sentences(self):
        """Test de phrases complètes en anglais."""
        normalizer = TextNormalizer(language='en')

        test_cases = [
            ("I have 3 dogs and 21 cats", "I have three dogs and twenty-one cats"),
            ("There are 99 bottles", "There are ninety-nine bottles"),
            ("The answer is 42", "The answer is forty-two"),
            ("She has 100 dollars", "She has one hundred dollars"),
        ]

        for input_text, expected in test_cases:
            result = normalizer.normalize(input_text)
            assert result == expected, f"Échec pour: {input_text}"

    def test_language_detection(self):
        """Test de la détection automatique de langue."""
        normalizer = TextNormalizer(language='auto')

        # Texte français
        fr_text = "J'ai 5 chiens"
        detected_lang = normalizer.detect_language(fr_text)
        assert detected_lang == 'fr'

        # Texte anglais
        en_text = "I have 5 dogs"
        detected_lang = normalizer.detect_language(en_text)
        assert detected_lang == 'en'

    def test_out_of_range_numbers(self):
        """Test que les nombres hors plage ne sont pas normalisés."""
        normalizer = TextNormalizer(language='fr')

        # Nombres > 1000 ne doivent pas être normalisés
        text = "L'année 2025 est spéciale"
        result = normalizer.normalize(text)
        assert "2025" in result  # Le nombre doit rester intact

    def test_preserve_punctuation(self):
        """Test que la ponctuation est préservée."""
        normalizer = TextNormalizer(language='fr')

        text = "Il a 5 ans, 3 chiens et 2 chats!"
        result = normalizer.normalize(text)
        assert "," in result
        assert "!" in result

    def test_batch_normalization(self):
        """Test de la normalisation par lot."""
        normalizer = TextNormalizer(language='en')

        texts = [
            "I have 1 cat",
            "She has 2 dogs",
            "He owns 3 birds"
        ]

        results = normalizer.normalize_batch(texts)

        assert len(results) == 3
        assert "one" in results[0]
        assert "two" in results[1]
        assert "three" in results[2]


class TestEdgeCases:
    """Tests des cas limites."""

    def test_zero_french(self):
        """Test du zéro en français."""
        fst = FrenchCardinalFST()
        assert fst.normalize("0") == "zéro"

    def test_zero_english(self):
        """Test du zéro en anglais."""
        fst = EnglishCardinalFST()
        assert fst.normalize("0") == "zero"

    def test_multiple_numbers_in_sentence(self):
        """Test de plusieurs nombres dans une phrase."""
        normalizer = TextNormalizer(language='en')

        text = "I have 3 cats, 5 dogs, and 10 birds"
        result = normalizer.normalize(text)

        assert "three" in result
        assert "five" in result
        assert "ten" in result

    def test_empty_string(self):
        """Test avec une chaîne vide."""
        normalizer = TextNormalizer(language='fr')
        result = normalizer.normalize("")
        assert result == ""

    def test_no_numbers(self):
        """Test avec un texte sans nombres."""
        normalizer = TextNormalizer(language='fr')

        text = "Il fait beau aujourd'hui"
        result = normalizer.normalize(text)
        assert result == text  # Doit rester inchangé


def run_comprehensive_test():
    """Execute tous les tests et génère un rapport."""
    print("=" * 70)
    print("TESTS COMPLETS DE NORMALISATION")
    print("=" * 70)
    print()

    # Test de tous les nombres de 0 à 1000 pour le français
    print("Test français (0-1000)...")
    fr_fst = FrenchCardinalFST()
    fr_errors = []

    for i in range(0, 1001):
        try:
            result = fr_fst.normalize(str(i))
            if not result or result == str(i):
                fr_errors.append(i)
        except Exception as e:
            fr_errors.append((i, str(e)))

    if fr_errors:
        print(f"  ✗ Erreurs trouvées: {len(fr_errors)}")
        print(f"    Premiers échecs: {fr_errors[:10]}")
    else:
        print(f"  ✓ Tous les nombres (0-1000) normalisés avec succès")

    # Test de tous les nombres de 0 à 1000 pour l'anglais
    print("\nTest anglais (0-1000)...")
    en_fst = EnglishCardinalFST()
    en_errors = []

    for i in range(0, 1001):
        try:
            result = en_fst.normalize(str(i))
            if not result or result == str(i):
                en_errors.append(i)
        except Exception as e:
            en_errors.append((i, str(e)))

    if en_errors:
        print(f"  ✗ Erreurs trouvées: {len(en_errors)}")
        print(f"    Premiers échecs: {en_errors[:10]}")
    else:
        print(f"  ✓ Tous les nombres (0-1000) normalisés avec succès")

    print()
    print("=" * 70)
    print("RÉSUMÉ")
    print("=" * 70)
    print(f"Français: {1001 - len(fr_errors)}/1001 succès ({(1001 - len(fr_errors)) / 1001 * 100:.2f}%)")
    print(f"Anglais: {1001 - len(en_errors)}/1001 succès ({(1001 - len(en_errors)) / 1001 * 100:.2f}%)")
    print()


if __name__ == "__main__":
    # Exécuter les tests complets
    run_comprehensive_test()

    # Exécuter les tests pytest
    print("\nExécution des tests pytest...")
    print("=" * 70)
    pytest.main([__file__, "-v"])
